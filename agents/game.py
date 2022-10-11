import random
import sys
import csv

sys.path.append(".")
from green import green
from red import *
from blue import *

# CREATION OF GRAPH/NODES
def create_nodes(num_nodes, vote_percent, intervals): # returns an array of green nodes
    voting = round(num_nodes*vote_percent)
    opinions = [1, 0]
    op_array = random.choices(opinions, weights=[voting, num_nodes-voting], k=num_nodes)

    nodes = []
    for i in range(num_nodes):
        if op_array[i] == 0:
            uncertainty = round(random.uniform(intervals[0], 0), 2)
            nodes.append(green(i, uncertainty, op_array[i]))
        elif op_array[i] == 1:
            uncertainty = round(random.uniform(0.01, intervals[1]), 2)
            nodes.append(green(i, uncertainty, op_array[i]))
    return nodes


def create_graph(network_file):
    # create a adjacency lists of green nodes
    unique_nodes_num = []
    graph = {}
    with open(network_file) as network:
        connection = csv.reader(network)

        for c in connection:
            if ("node" not in c[0]):
                # counting unique nodes
                if (int(c[0]) not in unique_nodes_num):
                    unique_nodes_num.append(int(c[0]))
                if (int(c[1]) not in unique_nodes_num):
                    unique_nodes_num.append(int(c[1]))

                if (int(c[0]) not in graph):
                    graph[int(c[0])] = [int(c[1])]
                elif (int(c[0]) in graph)  and (int(c[1]) not in graph[int(c[0])]):
                    adj = graph[int(c[0])]
                    adj.append(int(c[1]))
                    graph[int(c[0])] = adj
    network.close()
    return graph, sorted(unique_nodes_num)




# HELPER FUNCTIONS
def greenpercentstats(greenarray): 
    voting = 0
    for g in range(len(greenarray)):
        if greenarray[g].opinion == 1:
            voting += 1
    votepercent = (voting/len(greenarray))*100
    return votepercent

def greenstats(greenarray):
    voting = 0
    for g in range(len(greenarray)):
        if greenarray[g].opinion == 1:
            voting += 1
    print(f"number of green nodes: {len(greenarray)}")
    votepercent = (voting/len(greenarray))*100
    print(f"Voting: {votepercent}%")
    print(f"Not voting: {100 - votepercent}%\n")
    return votepercent

def get_most_uncertain(greenarray):
    uncertain = 1
    for g in greenarray:
        if g.uncertainty < uncertain:
            uncertain = g.uncertainty
    return uncertain

def minimax(green_nodes, num_rounds, agent, opp_ply, initialgreens):
    # end game condition: if all rounds have been iterated, or red has lost all followers, or red has full control of the population
    # return message type and overall opinion

    # check if winning/losing
    if (greenpercentstats(green_nodes) == 0):
        # everyone does not want to vote, red wins
        return None, 0
    elif (greenpercentstats(green_nodes) == 100):
        # everyone wants to vote, blue wins
        return None, 100
    elif isinstance(agent, red) and (abs(agent.uncertainty) < get_most_uncertain(green_nodes)):
        # red loses all followers, blue wins
        return None, 100
    elif isinstance(agent, blue) and (agent.energy == 0):
        # blue loses all of its energy, red wins
        return None, 0
    elif num_rounds == 0:
        return None, greenpercentstats(green_nodes)

    # recursion starts here
    if isinstance(agent, red):
        overall_opinion = 100
        propaganda_types = [agent.create_propaganda(1), agent.create_propaganda(2), agent.create_propaganda(3), agent.create_propaganda(4), agent.create_propaganda(5)]
        msg_type = agent.create_propaganda(1)#random.choice(propaganda_types)

        for p in propaganda_types:
            green_node_copy = green_nodes.copy()
            greensconstant = initialgreens.copy()
            updated_nodes = agent.spread_misinformation(green_node_copy, p)[0]
            opinion_post_spread = minimax(updated_nodes, num_rounds-1, opp_ply, agent, greensconstant)[1]
            # print("red change:", opinion_post_spread)
            if opinion_post_spread < overall_opinion:
                msg_type = p
                overall_opinion = opinion_post_spread

    elif isinstance(agent, blue):
        overall_opinion = 0
        message_types = [agent.create_counterargument(1),agent.create_counterargument(2),agent.create_counterargument(3),agent.create_counterargument(4),agent.create_counterargument(5)]
        msg_type = agent.create_counterargument(4)#random.choice(message_types)

        for m in message_types:
            if m.energy_cost >= agent.energy:
                message_types.remove(m)
            green_node_copy = green_nodes.copy()
            greensconstant = initialgreens.copy()
            updated_nodes = agent.spread_message(green_node_copy, m)
            opinion_post_spread = minimax(updated_nodes, num_rounds-1, opp_ply, agent, greensconstant)[1]
            # print("blue change:", opinion_post_spread)
            if opinion_post_spread > overall_opinion:
                msg_type = m
                overall_opinion = opinion_post_spread
    # print(f"{overall_opinion}")
    return msg_type, overall_opinion, initialgreens


# WINNING/LOSING 
def winning(greenarray, red_agent, blue_agent):
    # if swapped...
    if isinstance(red_agent, blue):
        temp = blue_agent
        blue_agent = red_agent
        red_agent = temp    
    # abs(red_agent.uncertainty) returns the maximum uncertainty red can interact with
    return (greenpercentstats(greenarray) == 100) or (greenpercentstats(greenarray) == 0) or (abs(red_agent.uncertainty) < get_most_uncertain(greenarray)) or (blue_agent.energy == 0)

def greenabsolutemajoritycheck(greenarray):
    if (greenstats(greenarray) == 100):
        return 1
    elif(greenstats(greenarray) == 0):
        return 0

def bluedeathcheck(player, ai):
    if isinstance(player, blue):
        return player.energy==0
    elif isinstance(ai, blue):
        return ai.energy==0

def reddeathcheck(player, ai, greenarray):
    if isinstance(player, red):
        return abs(player.uncertainty) < get_most_uncertain(greenarray)
    elif isinstance(ai, red):
        return abs(ai.uncertainty) < get_most_uncertain(greenarray)




# GREEN NODE INTERACTION
def influence(node1, node2):    #Takes a node pair instance and causes an interaction
        # node that is furthest away from zero influences the other node
        first = abs(node1.uncertainty)
        second = abs(node2.uncertainty)

        influencer = node1
        influenced = node2
        if first <= second:
            influencer = node2
            influenced = node1
        
        # value change 
        value_change = abs(first - second)*0.333
        
        if influencer.opinion == 1:
            influenced = influenced.change_uncertainty(influenced, value_change)
        elif influencer.opinion == 0:
            influenced = influenced.change_uncertainty(influenced, value_change * -1)
        # print(node1.uncertainty, node2.uncertainty)
        # print(influenced.uncertainty, influencer.uncertainty)
        return influenced, influencer

def interact(graph, green_array):    #Acts as green's "turn" when all adjacent green nodes interact with one another [0 1,2,3,4,8] 0-1 0-2 0-3 0-4 [5,6,7]
    #DFS through the graph
    visited = []
    # greenpairs = self.DFS(graph, visited, 0, green_array)
    #node pairs influence each other
    for n1 in graph:
        visited.append(n1) 
        for n2 in graph[n1]:
            if n2 not in visited:
                # print(n1, n2)
                # minus one as index started with zero (the first node was labled 1)
                updated_node, influencer = influence(green_array[n1-1], green_array[n2-1])
                # update green_array
                green_array[updated_node.id] = updated_node
                green_array[influencer.id] = influencer
    return green_array

def spreads_message(greenarray, potency):
    for node in greenarray:
        # print(node.uncertainty)
        # print(f"potency = {potency}")
        node.uncertainty += potency
        if node.uncertainty > 1:
            node.uncertainty = 1    
        if node.uncertainty < -1:
            node.uncertainty = -1   
        if node.uncertainty > 0:
            node.opinion = 1
        elif node.uncertainty <= 0:
            node.opinion = 0
    return greenarray




# GAME START-UP
def initialise():
    # welcome message
    print("insert welcome message\n")

    while True:
        player_agent = input("Please choose an agent (r or b): ")
        if player_agent.strip().lower() in ["r", "b"]:
            break
        print("Invalid output. Please try again\n")
    
    ai_agent = "b"  
    if player_agent.strip().lower() == "r":
        print("\nrole of red\n")
    if player_agent.strip().lower() == "b":
        ai_agent = "r"
        print("\ninsert role of blue\n")

    # validation of inputs
    print("\nPlease state the following parameters")
    while True:
        grayPercent = input("Percentage of gray working for blue (between 0-1): ")
        if float(grayPercent.strip().lower()) >= 0 and float(grayPercent.strip().lower()) <= 1:
            break
        print("Invalid output. Please try again\n")
    
    while True:
        min_interval = input("Minimum interval (between -1 and 0): ")
        max_interval = input("Maximum interval (between 0 and 1): ")

        if (float(min_interval.strip().lower()) >= -1) and (float(min_interval.strip().lower()) <= 0) and (float(max_interval.strip().lower()) >= 0) and (float(max_interval.strip().lower()) <= 1):
            if (float(min_interval.strip().lower()) < float(max_interval.strip().lower())):
                break
        print("Invalid output. Please try again\n")
    
    while True:
        vote_percent = input("Percentage of people willing to vote (between 0-1): ")
        if float(vote_percent.strip().lower()) >= 0 and float(vote_percent.strip().lower()) <= 1:
            break
        print("Invalid output. Please try again\n")
    while True:
        num_rounds = input("Number of days before election day (positive numbers only): ")
        if int(num_rounds.strip().lower()) > 0:
            break
        print("Invalid output. Please try again\n")

    # start simulation
    # player and ai will have their own colors
    simulation(float(grayPercent), [float(min_interval), float(max_interval)], int(num_rounds), float(vote_percent), player_agent, ai_agent)


def simulation(grayPercent, intervals, num_rounds, vote_percent, player, ai): 
    rounds = ["red", "blue", "green"] * num_rounds
    # create graph
    graph, num_nodes = create_graph("network-2.csv")

    # create array of green nodes
    green_nodes = create_nodes(len(num_nodes), vote_percent, intervals)
    for g in green_nodes:
        print('initial:', g.uncertainty, g.opinion)
    greenstats(green_nodes)
    # for g in green_nodes:
    #     print(g.uncertainty, g.opinion)

    # create agents
    if player == "r":
        player = red(0, round(random.uniform(-0.95, -1), 2))
        ai = blue(70, grayPercent)
    else:
        player = blue(70, grayPercent)
        ai = red(0, round(random.uniform(-0.95, -1), 2))
    
    if isinstance(player,blue):
        print(f"player is blue")
    elif isinstance(ai,blue):
        print(f"ai is blue")

    for r in rounds:
        # check if blue ran out of energy or red ran out of followers
        if winning(green_nodes, player, ai):
            # return name of winning agent 
            break
            
        # else:
        if r == "red":
            if isinstance(player, red):
                # execute player interactive function
                green_nodes = player.red_player(green_nodes)
                # print number of followers
                greenstats(green_nodes)
                # for node in green_nodes:
                #     print(f"should be {node.uncertainty}")
            elif isinstance(ai, red):
                greenforever = []
                for node in green_nodes:
                    greenforever.append(node.uncertainty)
                bestmessage, value, greensconstant = minimax(green_nodes, num_rounds//2, ai, player, green_nodes)
                print(f"Opponent chose {bestmessage.type}")
                for i in range(len(green_nodes)):
                    green_nodes[i].uncertainty = greenforever[i]  
                    if green_nodes[i].uncertainty > 0:
                        green_nodes[i].opinion = 1
                    elif green_nodes[i].uncertainty <= 0:
                        green_nodes[i].opinion = 0
                green_nodes = spreads_message(green_nodes, bestmessage.potency)
                # execute minimax(?) function 
                
                for g in green_nodes:
                    print('after red:', g.uncertainty, g.opinion)
                greenstats(green_nodes)
            # print percentage of people wanting to vote/ against voting
        
        elif r == "blue":
            if isinstance(player, blue):
                # execute player interactive function
                green_nodes, updated_gray = player.blue_playe(green_nodes, grayPercent)
                # if gray was used, update the gray perblue(grcentages (chances of realising a spy increases)
                grayPercent = updated_gray
                for g in green_nodes:
                    print('after blue/gray:', g.uncertainty, g.opinion)
                #print remaining energy
                greenstats(green_nodes)
            elif isinstance(ai, blue):
                greenforever = []
                for node in green_nodes:
                    greenforever.append(node.uncertainty)
                bestmessage, value, greensconstant = minimax(green_nodes, num_rounds//2, ai, player, green_nodes)
                print(f"Opponent chose {bestmessage.type}")
                ai.energy -= bestmessage.energy_cost
                for i in range(len(green_nodes)):
                    green_nodes[i].uncertainty = greenforever[i]  
                    if green_nodes[i].uncertainty > 0:
                        green_nodes[i].opinion = 1
                    elif green_nodes[i].uncertainty <= 0:
                        green_nodes[i].opinion = 0
                green_nodes = spreads_message(green_nodes, bestmessage.strength)

                # for node in green_nodes:
                #     print(f"greennodes {node.uncertainty}")
                #print(f"type = {bestmessage.type}")
                # green_nodes, updated_gray = ai.blue(green_nodes, grayPercent)
                # # if gray was used, update the gray percentages (chances of realising a spy increases)
                # grayPercent = updated_gray
                for g in green_nodes:
                    print('after blue/gray:', g.uncertainty, g.opinion)
                greenstats(green_nodes)
                # execute minimax(?) function 
                # print percentage of people wanting to vote/ against voting 
        elif r == "green":
            green_nodes = interact(graph, green_nodes)
            for g in green_nodes:
                print('after interaction:', g.uncertainty, g.opinion)
            greenstats(green_nodes)
            
    if bluedeathcheck(player,ai):
        print(f"Blue has lost all hope to combat red. Red wins!!\n")
        return
    elif reddeathcheck(player, ai, green_nodes):
        print(f"No one wants to listen to red anymore. Blue wins!!\n")
        return
    elif greenabsolutemajoritycheck(green_nodes)==1:
        print(f"Blue has gained absolute control. Blue wins!")
        return
    elif greenabsolutemajoritycheck(green_nodes)==0:
        print(f"Red has gained absolute control. Red wins!")
        return

    # else: # election day 
    votepercent = greenstats(green_nodes)
    print(f"!!ELECTION DAY!!\n")
    if votepercent > 50:
        print(f"Blue has won the game\n")
    elif votepercent < 50:
        print(f"Red has won the game\n")
    else:
        print(f"It's a draw\n")





    '''
    winner = max(for_voting, against_voting)
    if winner == for_voting:
        print("Blue wins!!\n")
    elif winner == against_voting:
        print("Red wins!!\n")
    else:
        print("It's a draw\n")'''
    '''runs the game until either a) win condition is met or b) all rounds have been executed'''
    
    '''
    winning conditions
    if blue can no longer act (lost all energy), red wins
    if red can no longer act (lost all followers), blue wins
    election day (set simulation rounds)
    '''

    '''
    winning_conditions = false
    sim_counter = 0
    winner = 

    while (winning conditions are not true) or sim_counter < number of rounds:
        #create red agent object 
        red = Red(round(random.uniform(0.7, 1), 2))

        #ask player to choose message

        #make red agent interact with greens with message of choice / returns a counter of green agents it has interacted with
        red_progress = spread_misinformation(graph, agent, message chosen by player)
        if red_progress == 0 (if red ran out of followers):
            winner = blue
            winning_conditions = true

        run blue interact with all green with a counter / deploy a gray agent
    initialise
        blue = BlueAgent(energy)
        action : select either deploy gray agent of directly from blue
        if (direct)
            if(countmessage.energy >= energy)
                print("insufficient energy, your game loss if this message is chosen")
                if (continue chosen)
                    #red is winner
                    winner = red
                    game end() #return winner and final state(?)
                else
                    back to action
            counterpropaganda(population, countermessage) #interact with all green population
            energy -= countermessage.energycost
        else
            deploy_gray_agent(message, countermessage, probability) #message from red, countermessage from blue, chance of grey being red/blue
 
        run green to interact with other greens

        #if (sim_counter == number of rounds - 1 (if last round has been reached -> election day):
        check the state of the graph (iterate through the graph and count how many greens want to vote or abstain from voting)
        if (vote > abstain):
            winner = blue
        elif (vote < abstain):
            winner = red
        else:
            winner = there is no clear winner

        sim_counter += 1
     
     return winner
    '''

# create_graph("network-2.csv", [*range(25)])
initialise()

