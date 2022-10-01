import random
import csv

def create_graph(network_file, green_array):
    '''
    create a adjacency lists of green nodes
    '''
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
    print("insert welcome message")

    while True:
        player_agent = input("Please choose an agent (r or b):")
        if player_agent.strip().lower() in ["r", "b"]:
            break
        print("Invalid output. Please try again")
    
    ai_agent = "b"    
    if player_agent.lower() == "b":
        ai_agent = "a"

    # validation of inputs
    print("Please state the following parameters")
    while True:
        grayPercent = input("Percentage of gray working for blue (between 0-1): ")
        if grayPercent >= 0 and grayPercent <= 1:
            break
        print("Invalid output. Please try again")
    
    while True:
        min_interval = input("Please enter the minimum interval (between -1 and 1): ")
        max_interval = input("Please enter the minimum interval (between -1 and 1): ")

        if (min_interval >= -1) and (min_interval <= 1) and (max_interval >= 1) and (max_interval <= 1):
            if (min_interval < max_interval):
                break
        print("Invalid output. Please try again")
    
    while True:
        vote_percent = input("Please enter of people willing to vote (0-1): ")
        if vote_percent >= 0 and vote_percent <= 1:
            break
        print("Invalid output. Please try again")

    # start simulation
    # player and ai will have their own colors
    simulation(grayPercent, [min_interval, max_interval], vote_percent, player_agent, ai_agent)

def simulation(grayPercent, interaval, vote_percent, player, ai): #params - probability intervals (? uncertainty, gray agent distribution), number of rounds
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

create_graph("network-2.csv", [*range(25)])

