import random
import sys
import csv

sys.path.append(".")
from green import green
from red import *
from blue import *

def create_nodes(num_nodes): # returns an array of green nodes
    green_array = []
    for i in range(num_nodes):
        uncertainty = round(random.uniform(-1, 1), 2)
        opinion = 1 if uncertainty > 0 else 0
        green_array.append(green(i, uncertainty, opinion))
    return green_array


def create_graph(network_file):
    # create a adjacency lists of green nodes
    graph = {}
    with open(network_file) as network:
        connection = csv.reader(network)

        for c in connection:
            if ("node" not in c[0]):
                if (int(c[0]) not in graph):
                    graph[int(c[0])] = [int(c[1])]
                elif (int(c[0]) in graph)  and (int(c[1]) not in graph[int(c[0])]):
                    adj = graph[int(c[0])]
                    adj.append(int(c[1]))
                    graph[int(c[0])] = adj
    network.close()
    return graph


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
        min_interval = input("Minimum interval (between -1 and 1): ")
        max_interval = input("Maximum interval (between -1 and 1): ")

        if (float(min_interval.strip().lower()) >= -1) and (float(min_interval.strip().lower()) <= 1) and (float(max_interval.strip().lower()) >= -1) and (float(max_interval.strip().lower()) <= 1):
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
    simulation(grayPercent, [min_interval, max_interval], vote_percent, num_rounds, player_agent, ai_agent)

def greenstats(greenarray): 
    voting = 0
    for index in greenarray:
        if greenarray[index].opinion == 1:
            voting += 1
    votepercent = (voting/len(greenarray))*100
    print(f"The current percent of the population that wants to vote is {votepercent}%")
    print(f"The current percent of the population that do not want to vote is {100 - votepercent}%\n")
    return votepercent

def winning(greenarray, red_agent, blue_agent):
    # if swapped...
    if isinstance(red_agent, blue):
        temp = blue_agent
        blue_agent = red_agent
        red_agent = temp    
    # tamest possible propaganda tactic
    min_message = propaganda(0.8, -0.05, "Speech of Patriotism")
    return (greenstats(greenarray) == 100) or (greenstats(greenarray) == 0) or (red_agent.num_followers(min_message, greenarray) == 0) or (blue_agent.energy == 0)


def simulation(grayPercent, interval, num_rounds, vote_percent, player, ai): 
    rounds = ["red", "blue", "green"] * num_rounds
    # create graph
    graph = create_graph("network-2.csv")
    # create array of green nodes
    green_nodes = create_nodes(len(graph))
    # create agents
    if player == "r":
        player = red(0, round(random.uniform(-0.95, -1), 2))
        ai = blue(200)
    else:
        player = blue(200)
        ai = red(0, round(random.uniform(-0.95, -1), 2))

    for r in rounds:
        # check if blue ran out of energy or red ran out of followers
        if winning(green_nodes, player, ai):
            # return name of winning agent 
            break
        else:
            if r == "red":
                if player == "r":
                    # execute player interactive function
                    # print number of followers
                    return None
                elif ai == "r":
                    # execute minimax(?) function 
                # print percentage of people wanting to vote/ against voting 
                    return None
            
            elif r == "blue":
                if player == "b":
                    # execute player interactive function
                    # print remaing energy amount 
                    return None
                elif ai == "b":
                    # execute minimax(?) function 
                    # print percentage of people wanting to vote/ against voting 
                    return None
            
            elif r == "green":
                # interaction function (dfs?)
                # print percentage of people wanting to vote/ against voting 
                return None
    votepercent = greenstats(green_nodes)
    if votepercent > 50:
        print(f"Blue has won the game\n")
    elif votepercent < 50:
        print(f"Red has won the game\n")
    else:
        print(f"It's a draw\n")
    

    # # election day 
    # winner = max(for_voting, against_voting)
    # if winner == for_voting:
    #     print("Blue wins!!\n")
    # elif winner == against_voting:
    #     print("Red wins!!\n")
    # else:
    #     print("It's a draw\n")
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

