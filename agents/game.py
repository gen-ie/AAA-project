'''
Genevie Caraan - 23070605
Daniel Loo - 23157127
'''
#%%
import random
import sys
import csv
import matplotlib.pyplot as plt
from pathlib import Path

sys.path.append(".")
from green import green
from red import *
from blue import *
from gray import *

# CREATE VISUALS
def plot_green(green_nodes):
    green_unc = [g.uncertainty for g in green_nodes]
    plt.hist(green_unc)
    plt.show()


# CREATION OF GRAPH/NODES
def create_nodes(num_nodes, vote_percent, intervals): # returns an array of green nodes
    voting = round(num_nodes*vote_percent)
    opinions = ([1]*voting) + ([0]*(num_nodes-voting))
    random.shuffle(opinions)
    op_array = opinions

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
def greenpercentstats(greenarray): #returns the percentage of greens that want to vote
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
    #print(f"number of green nodes: {len(greenarray)}")
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

def isStalemate(green_nodes, intervals):
    for g in green_nodes:
        if g.uncertainty not in intervals:
            return False
    return True

def count_followers(red, green_nodes):
    count = 0
    for g in green_nodes:
        if abs(red.uncertainty) > g.uncertainty:
            count += 1
    return count

def minimax(green_nodes, graph, num_rounds, agent, opp_ply, gray_percent, intervals):
    # end game condition: if all rounds have been iterated, or red has lost all followers, or red has full control of the population
    # return message type and overall opinion

    # check if winning/losing
    if (greenpercentstats(green_nodes) == 0):
        # everyone does not want to vote, red wins
        return None, 0
    elif (greenpercentstats(green_nodes) == 100):
        # everyone wants to vote, blue wins
        return None, 100
    elif isinstance(agent, red) and ((abs(agent.uncertainty) < get_most_uncertain(green_nodes)) or (agent.uncertainty >= 0) ): 
        # red loses all followers, blue wins
        #print(agent.uncertainty)
        return None, 100
    elif isinstance(agent, blue) and (agent.energy < 0):
        # blue loses all of its energy, red wins
        return None, 0
    elif (num_rounds == 0) or (isStalemate(green_nodes, intervals)):
        return None, greenpercentstats(green_nodes)

    # recursion starts here
    if isinstance(agent, red):
        overall_opinion = 100
        propaganda_types = [agent.create_propaganda(1), agent.create_propaganda(2), agent.create_propaganda(3), agent.create_propaganda(4), agent.create_propaganda(5)]
        msg_type = random.choice(propaganda_types)

        for p in propaganda_types:
            green_node_copy = green_nodes.copy()
            updated_nodes = agent.spread_misinformation(green_node_copy, p, intervals[0])[0]
            opinion_post_spread = minimax(updated_nodes, graph, num_rounds-1, opp_ply, agent, gray_percent, intervals)[1]
            # print(type(opinion_post_spread))
            #print("red change:", opinion_post_spread[0], opinion_post_spread[1])
            if opinion_post_spread < overall_opinion:
                msg_type = p
                overall_opinion = opinion_post_spread

    elif isinstance(agent, blue):
        overall_opinion = 0
        uncertainty, allegiance = agent.create_gray(gray_percent)
        message_types = [agent.create_counterargument(1),agent.create_counterargument(2),agent.create_counterargument(3),agent.create_counterargument(4),agent.create_counterargument(5), gray(uncertainty, allegiance)]
        msg_type = random.choice(message_types)

        # if energy insufficient, spam gray
        messageinvalid = []
        for i in range(len(message_types)):
            if isinstance(message_types[i], counterargument):
                if message_types[i].energy_cost >= agent.energy:
                    messageinvalid.append(message_types[i]) 
        for mes in messageinvalid:
            message_types.remove(mes)

        for m in message_types:
            # copies of the graph
            green_node_copy = green_nodes.copy()
            gray_p = 0

            # gray agent
            if isinstance(m, gray):
                updated_nodes, gray_p = m.deploy_grey(green_node_copy, gray_percent, intervals)[:2]
            # blue message
            elif isinstance(m, counterargument):
                updated_nodes = agent.spread_message(green_node_copy, m, intervals[1])
            # green interaction after blue's turn
            updated_nodes = interact(graph, updated_nodes)
            opinion_post_spread = minimax(updated_nodes, graph, num_rounds-1, opp_ply, agent, gray_p, intervals)[1]
            # print(type(opinion_post_spread))
            # print("blue change:", opinion_post_spread[0], opinion_post_spread[1])
            if opinion_post_spread > overall_opinion:
                msg_type = m
                overall_opinion = opinion_post_spread
    # print(f"{overall_opinion}")
    return msg_type, overall_opinion



# WINNING/LOSING 
def winning(greenarray, red_agent, blue_agent):
    # if swapped...
    if isinstance(red_agent, blue):
        temp = blue_agent
        blue_agent = red_agent
        red_agent = temp    
    # abs(red_agent.uncertainty) returns the maximum uncertainty red can interact with
    return (greenpercentstats(greenarray) == 100) or (greenpercentstats(greenarray) == 0) or ((abs(red_agent.uncertainty) < get_most_uncertain(greenarray)) or (red_agent.uncertainty >= 0)) or (blue_agent.energy < 0)

def greenabsolutemajoritycheck(greenarray):
    if (greenpercentstats(greenarray) == 100):
        return 1
    elif(greenpercentstats(greenarray) == 0):
        return 0

def bluedeathcheck(player, ai):
    if isinstance(player, blue):
        return player.energy < 0
    elif isinstance(ai, blue):
        return ai.energy < 0

def reddeathcheck(player, ai, greenarray):
    if isinstance(player, red):
        return abs(player.uncertainty) < get_most_uncertain(greenarray) or (player.uncertainty >= 0 )
    elif isinstance(ai, red):
        return abs(ai.uncertainty) < get_most_uncertain(greenarray) or (ai.uncertainty >= 0 )




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
    value_change = abs(first - second)*0.2
    if influencer.opinion == 1:
        influenced = influenced.change_uncertainty(influenced, value_change)
    elif influencer.opinion == 0:
        influenced = influenced.change_uncertainty(influenced, value_change * -1)
    return influenced, influencer

def interact(graph, green_array):    #Acts as green's "turn" when all adjacent green nodes interact with one another [0 1,2,3,4,8] 0-1 0-2 0-3 0-4 [5,6,7]
    #DFS through the graph
    visited = []
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

def spreads_message(greenarray, message, agent, intervals):
    for node in greenarray:
        if isinstance(agent, red) and (abs(agent.uncertainty) >= node.uncertainty):
            # print("red uncertainty:", agent.uncertainty)
            node.uncertainty += message.potency   
            if node.uncertainty < intervals[0]:
                node.uncertainty = intervals[0]  
            if node.uncertainty > 0:
                node.opinion = 1
            elif node.uncertainty <= 0:
                node.opinion = 0
            
        elif isinstance(agent, blue) and ((agent.unsureness * -1) <= node.uncertainty):
            #print("blue uncertainty:", agent.unsureness)
            node.uncertainty += message.strength
            if node.uncertainty > intervals[1]:
                node.uncertainty = intervals[1]     
            if node.uncertainty > 0:
                node.opinion = 1
            elif node.uncertainty <= 0:
                node.opinion = 0

    if isinstance(agent, red):           
        agent.uncertainty += message.follower_lose
    elif isinstance(agent, blue):
        agent.energy -= message.energy_cost
    return greenarray




# GAME START-UP
def initialise():
    # welcome message
    print("\nWelcome to Red and Blue teams simulator. Both team's goal is to influence the opinions of the Green population, to either vote or not vote, before election day arrives. \n")
     
    while True:
        path = input("Please insert node network csv file: ")
        if "csv" in path:
            path_f = Path(path)
            if path_f.is_file():
                break
        print("No file found")      
    
    while True:
        game = input("Do you want to participate as one of the groups in this game (y or n): ")
        if game.strip().lower() in ["y", "n"]:
            break
        print("Invalid output. Please try again\n")

    # if player wants to get involved
    player_a = ""
    player_b = ""

    if game.strip().lower()  == "y":
        while True:
            player_a = input("Please choose an agent (r or b): ")
            if player_a.strip().lower() in ["r", "b"]:
                break
            print("Invalid output. Please try again\n")
      
        if player_a.strip().lower() == "r":
            player_b = "b"
            print("\nYou are a red agent! Your job is to spread chaos.\n")
            print("You have a choice of five types of messages to send out:\n")
            print("1: Speech of Patriotism (Showcase your loyalty to sway people) - tame message") 
            print("2: Propaganda (Boast your accomplisments) - moderately tame message. Can affect a lot of people") 
            print("3: Conspiracy (Suggest ideas to unspecting citizens) - moderately effective message. Can affect some people") 
            print("4: Fake News (Fabricate evidence in order to succeed) - highly effective message. Can affect only a handful of certain people") 
            print("5: Fear mongering (Indoctrinate the people through scare tactics) - heavily potent message. Can only affect uncertain people") 
            print("To win the game, you have to make sure that everyone is confused and do not want to vote due to conflicting information.\n")
            print("\n")

        if player_a.strip().lower() == "b":
            player_b = "r"
            print("\nYou are a blue agent! Your job is stop red from doing its nefarious schemes. To win the game, you must fight back red's\nadvances. Make sure everyone knows the truths.Make sure everyone knows the truth, and are confindent of their votes.\n")
            print("1: Unifying Speech  (Remind people of the truth and democratic values) - tame message") 
            print("2: Mass-reporting (Reporting of social media accounts that deliberately spread misinformation) - moderately tame message") 
            print("3: Debunking and Fact-checking (Calling out false information with information from proper sources) - moderately effective message") 
            print("4: Law implementation on misinformation") 
            print("5: Democratic rallies (Peaceful protests for preserving democratic values) - powerful message") 
            print("\n")

    # if player does not want to get involved
    elif game.strip().lower()  == "n":
        player_a = "r_ai"
        player_b = "b_ai"

    # validation of inputs     
    print("\nPlease state the following parameters")
    while True:
        grayPercent = input("Percentage of gray working for blue (between 0-1): ")
        # if isinstance(grayPercent, "int"):
        try:
            float(grayPercent.strip().lower())
            if float(grayPercent.strip().lower()) >= 0 and float(grayPercent.strip().lower()) <= 1:
                break
            print("Invalid output. Please try again\n")
        except ValueError:
            print("Invalid output. Please try again\n")
            
    while True:
        min_interval = input("Minimum interval (between -1 and 0): ")
        max_interval = input("Maximum interval (between 0 and 1): ")
        
        try:
            if (float(min_interval.strip().lower()) >= -1) and (float(min_interval.strip().lower()) <= 0) and (float(max_interval.strip().lower()) >= 0) and (float(max_interval.strip().lower()) <= 1):
                if (float(min_interval.strip().lower()) < float(max_interval.strip().lower())):
                    break
            print("Invalid output. Please try again\n")
        except ValueError:
            print("Invalid output. Please try again\n")
    
    while True:
        try: 
            vote_percent = input("Percentage of people willing to vote (between 0-1): ")
            if float(vote_percent.strip().lower()) >= 0 and float(vote_percent.strip().lower()) <= 1:
                break
            print("Invalid output. Please try again\n")
        except ValueError:
            print("Invalid output. Please try again\n")
        
    while True:
        try:
            num_rounds = input("Number of days before election day (positive numbers only): ")
            if int(num_rounds.strip().lower()) > 0:
                break
            print("Invalid output. Please try again\n")
        except ValueError:
            print("Invalid output. Please try again\n")
            
    # start simulation
    # player and ai will have their own colors
    simulation(path_f, float(grayPercent), [float(min_interval), float(max_interval)], int(num_rounds), float(vote_percent), player_a, player_b)


def simulation(csv_file, grayPercent, intervals, num_rounds, vote_percent, player_a, player_b): 
    print(f"\nPercentage of gray agents allied to blue: {grayPercent}")
    print(f"Intervals: {intervals[0]} to {intervals[1]}")
    print(f"Number of days before Election day: {num_rounds}")
    print(f"Percentage of green who want to vote: {vote_percent}\n")

    rounds = ["red", "blue", "green"] * num_rounds
    # create graph
    graph, num_nodes = create_graph(csv_file)

    # create array of green nodes
    green_nodes = create_nodes(len(num_nodes), vote_percent, intervals)
    # for g in green_nodes:
    #     print('Initial:', g.uncertainty, g.opinion)
    # print("\n")
    plot_green(green_nodes)
    greenstats(green_nodes)

    # create agents
    if player_a == "r":
        player_a = red(round(random.uniform(-0.95, -1), 2))
        player_b = blue(30, round(random.uniform(0.95, 1), 2), grayPercent)
        non_player = False

    elif player_a == "b":
        player_a = blue(30, round(random.uniform(0.95, 1), 2), grayPercent)
        player_b = red(round(random.uniform(-0.95, -1), 2))
        non_player = False

    elif (player_a == "r_ai") and (player_b == "b_ai"):
        player_a = red(round(random.uniform(-0.95, -1), 2))
        player_b = blue(30, round(random.uniform(0.95, 1), 2), grayPercent)
        non_player = True

    # THE ACTUAL SIMULATION
    curr_round = 0
    for r in rounds:
        # check if blue ran out of energy or red ran out of followers
        if winning(green_nodes, player_a, player_b) or isStalemate(green_nodes, intervals):
            if isStalemate(green_nodes, intervals):
                print("\nBoth red and blue are in stalemate!\n")
            break
            
        print(f"ROUND {curr_round} - {r}\n")
        if r == "red":
            if (isinstance(player_a, red) and (non_player == False)):
                # execute player interactive function
                #print("red before:", player.uncertainty)
                green_nodes = player_a.red_player(green_nodes, intervals)
                # print number of followers
                print("STATE OF NODES AFTER RED TURN")
                # for g in green_nodes:
                #     print(round(g.uncertainty, 2), "\t", g.opinion)
                # print("\n")
                plot_green(green_nodes)
                greenstats(green_nodes)

            elif (isinstance(player_b, red) and (non_player == False)) or (isinstance(player_a, red) and (non_player == True)):
                # copies of the agent for minimax
                if (isinstance(player_b, red) and (non_player == False)):
                    ai_copy = red(player_b.uncertainty)
                    player_copy = blue(player_a.energy, player_a.unsureness, player_a.gray_percent)
                    print(f"Current uncertainty: {player_b.uncertainty}")
                    count = count_followers(player_b, green_nodes)
                    print(f"Current number of followers: {count}\n")

                elif  (isinstance(player_a, red) and (non_player == True)):
                    ai_copy = red(player_a.uncertainty)
                    player_copy = blue(player_b.energy, player_b.unsureness, player_b.gray_percent)
                    print(f"Current uncertainty: {player_a.uncertainty}")
                    count = count_followers(player_a, green_nodes)
                    print(f"Current number of followers: {count}\n")

                # print(player_a.uncertainty)
                greenforever = []
                for node in green_nodes:
                    greenforever.append(node.uncertainty)
                bestmessage_r = minimax(green_nodes, graph, num_rounds, ai_copy, player_copy, grayPercent, intervals)[0]
                # print(player_b.uncertainty)
                print(f"Red chose: {bestmessage_r.type}\n")
                for i in range(len(green_nodes)):
                    green_nodes[i].uncertainty = greenforever[i]  
                    if green_nodes[i].uncertainty > 0:
                        green_nodes[i].opinion = 1
                    elif green_nodes[i].uncertainty <= 0:
                        green_nodes[i].opinion = 0
                # print(player_b.uncertainty)
                if (isinstance(player_b, red) and (non_player == False)):
                    green_nodes = spreads_message(green_nodes, bestmessage_r, player_b, intervals)
                elif  (isinstance(player_a, red) and (non_player == True)):
                    green_nodes = spreads_message(green_nodes, bestmessage_r, player_a, intervals)

                print("STATE OF NODES AFTER RED TURN")
                # for g in green_nodes:
                #     print(round(g.uncertainty, 2), "\t", g.opinion)
                # print("\n")
                plot_green(green_nodes)
                greenstats(green_nodes)
        
        elif r == "blue":
            if (isinstance(player_a, blue) and (non_player == False)):
                # execute player interactive function
                green_nodes, updated_gray = player_a.blue_player(green_nodes, grayPercent, intervals)
                # if gray was used, update the gray perblue(grcentages (chances of realising a spy increases)
                grayPercent = updated_gray

                print("STATE OF NODES AFTER BLUE/GRAY TURN")
                # for g in green_nodes:
                #     print(round(g.uncertainty,2),"\t", g.opinion)
                # print("\n")
                plot_green(green_nodes)
                greenstats(green_nodes)

            elif isinstance(player_b, blue):
                # copies of the agent for minimax
                ai_copy = blue(player_b.energy, player_b.unsureness, player_b.gray_percent)
                player_copy = red(player_a.uncertainty)

                # print(f"Current energy: {player_b.energy}")
                print(f"Blue's unsureness: {player_b.unsureness}")
                print(f"Blue's energy: {player_b.energy}\n")

                greenforever = []
                for node in green_nodes:
                    greenforever.append(node.uncertainty)
                bestmessage_b = minimax(green_nodes, graph, num_rounds, ai_copy, player_copy, grayPercent, intervals)[0]
                # print("red:", player.uncertainty)
                if isinstance(bestmessage_b, counterargument):
                    print(f"Blue chose: {bestmessage_b.type}\n")
                    # ai.energy -= bestmessage.energy_cost
                    for i in range(len(green_nodes)):
                        green_nodes[i].uncertainty = greenforever[i]  
                        if green_nodes[i].uncertainty > 0:
                            green_nodes[i].opinion = 1
                        elif green_nodes[i].uncertainty <= 0:
                            green_nodes[i].opinion = 0
                    green_nodes = spreads_message(green_nodes, bestmessage_b, player_b, intervals)

                elif isinstance(bestmessage_b, gray):
                    print(f"Opponent chose to deploy a Gray agent!")
                    for i in range(len(green_nodes)):
                        green_nodes[i].uncertainty = greenforever[i]  
                        if green_nodes[i].uncertainty > 0:
                            green_nodes[i].opinion = 1
                        elif green_nodes[i].uncertainty <= 0:
                            green_nodes[i].opinion = 0
                    green_nodes, updated_gray, msg = bestmessage_b.deploy_grey(green_nodes, grayPercent, intervals)
                    if bestmessage_b.allegiance == "red":
                        print(f"Unfortunately it was a spy! It sent out {msg}\n")
                    else:
                        print(f"Gray gives blue a hand! It carried out {msg}\n")

                print("STATE OF NODES AFTER BLUE/GRAY TURN")
                # for g in green_nodes:
                #     print(round(g.uncertainty, 2), "\t", g.opinion)
                # print("\n")
                plot_green(green_nodes)
                greenstats(green_nodes)

        elif r == "green":
            green_nodes = interact(graph, green_nodes)
            print("STATE OF NODES AFTER GREEN INTERACTIONS")
            # for g in green_nodes:
            #     print(round(g.uncertainty, 2), "\t", g.opinion)
            # print("\n")
            print(f"STATE OF NODES AFTER ROUND {curr_round}")
            plot_green(green_nodes)
            greenstats(green_nodes)

            # increment round
            curr_round += 1
            
    if bluedeathcheck(player_a, player_b):
        print(f"Blue has lost all hope to combat red. Red wins!!\n")
        return
    elif reddeathcheck(player_a, player_b, green_nodes):
        print(f"No one wants to listen to red anymore. Blue wins!!\n")
        return
    elif greenabsolutemajoritycheck(green_nodes)==1:
        print(f"Blue has gained absolute control. Blue wins!")
        return
    elif greenabsolutemajoritycheck(green_nodes)==0:
        print(f"Red has gained absolute control. Red wins!")
        return

    # else: # election day 
    votepercent = greenpercentstats(green_nodes)
    print(f"!!ELECTION DAY!!\n")
    if votepercent > 50:
        print(f"Blue has won the game\n")
    elif votepercent < 50:
        print(f"Red has won the game\n")
    else:
        print(f"It's a draw\n")

initialise()

# %%
