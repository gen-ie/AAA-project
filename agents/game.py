import random
import sys
import csv

sys.path.append(".")
from green import green
from red import *
from blue import *

# CREATION OF GRAPH/NODES
def create_nodes(num_nodes, vote_percent): # returns an array of green nodes
    voting = round(num_nodes*vote_percent)
    opinions = [1, 0]
    op_array = random.choices(opinions, weights=[voting, num_nodes-voting], k=num_nodes)

    nodes = []
    for i in range(num_nodes):
        if op_array[i] == 0:
            uncertainty = round(random.uniform(-1, 0), 2)
            nodes.append(green(i, uncertainty, op_array[i]))
        elif op_array[i] == 1:
            uncertainty = round(random.uniform(0.01, 1), 2)
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


# WINNING/LOSING 
def winning(greenarray, red_agent, blue_agent):
    # if swapped...
    if isinstance(red_agent, blue):
        temp = blue_agent
        blue_agent = red_agent
        red_agent = temp    
    # tamest possible propaganda tactic
    # min_message = propaganda(0.8, -0.05, "Speech of Patriotism")
    print(f"Blue agent energy {blue_agent.energy}")
    return (greenpercentstats(greenarray) == 100) or (greenpercentstats(greenarray) == 0) or (red_agent.uncertainty < get_most_uncertain(greenarray)) or (blue_agent.energy == 0)

def greenabsolutemajoritycheck(greenarray):
    if (greenstats(greenarray) == 100):
        return 1
    elif(greenstats(greenarray) == 0):
        return 0

def bluedeathcheck(player, ai):
    if isinstance(player, blue):
        player.energy=0
        return True
    elif isinstance(ai, blue):
        ai.energy=0
        print(f"ai energy = {ai.energy}")
        return True
    return False

def reddeathcheck(player, ai, greenarray):
    if isinstance(player, red):
        player.uncertainty < get_most_uncertain(greenarray)
        return True
    elif isinstance(ai, red):
        ai.uncertainty < get_most_uncertain(greenarray)
        return True
    return False


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
    
    # while True:
    #     min_interval = input("Minimum interval (between -1 and 1): ")
    #     max_interval = input("Maximum interval (between -1 and 1): ")

    #     if (float(min_interval.strip().lower()) >= -1) and (float(min_interval.strip().lower()) <= 1) and (float(max_interval.strip().lower()) >= -1) and (float(max_interval.strip().lower()) <= 1):
    #         if (float(min_interval.strip().lower()) < float(max_interval.strip().lower())):
    #             break
    #     print("Invalid output. Please try again\n")
    
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
    simulation(float(grayPercent), int(num_rounds), float(vote_percent), player_agent, ai_agent)

def simulation(grayPercent, num_rounds, vote_percent, player, ai): 
    rounds = ["red", "blue", "green"] * num_rounds
    # create graph
    graph, num_nodes = create_graph("network-2.csv")

    # create array of green nodes
    green_nodes = create_nodes(len(num_nodes), vote_percent)
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

    for r in rounds:
        # check if blue ran out of energy or red ran out of followers
        # if winning(green_nodes, player, ai):
        #     # return name of winning agent 
        #     print(winning(green_nodes, player, ai))
        #     break
            
        # else:
        if r == "red":
            if isinstance(player, red):
                # execute player interactive function
                green_nodes = player.red_player(green_nodes)
                # print number of followers
                greenstats(green_nodes)
            elif ai == "r":
                continue
                # execute minimax(?) function 
            # print percentage of people wanting to vote/ against voting
        
        elif r == "blue":
            if isinstance(player, blue):
                # execute player interactive function
                green_nodes = player.blue(green_nodes, grayPercent)
                for g in green_nodes:
                    print('after gray:', g.uncertainty, g.opinion)
                #print remaining energy
                greenstats(green_nodes)
            elif isinstance(ai, blue):
                green_nodes = ai.blue(green_nodes, grayPercent)
                #print remaining energy
                greenstats(green_nodes)
                # execute minimax(?) function 
                # print percentage of people wanting to vote/ against voting 
        elif r == "green":
            green_nodes = interact(graph, green_nodes)
            for g in green_nodes:
                print('after interaction:', g.uncertainty, g.opinion)
            greenstats(green_nodes)
            
    # if bluedeathcheck(player,ai):
    #     print(f"Blue has lost all hope to combat red. Red wins!!\n")
    # elif reddeathcheck(player, ai, green_nodes):
    #     print(f"No one wants to listen to red anymore. Blue wins!!\n")
    # elif greenabsolutemajoritycheck(green_nodes)==1:
    #     print(f"Blue has gained absolute control. Blue wins!")
    # elif greenabsolutemajoritycheck(green_nodes)==0:
    #     print(f"Red has gained absolute control. Red wins!")

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

