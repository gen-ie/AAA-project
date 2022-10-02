import random
import csv

def create_graph(network_file, green_array):
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



def simulation(grayPercent, interval, num_rounds, vote_percent, player, ai): 
    rounds = ["red", "green", "blue"] * num_rounds

    # create array of green nodes
    # create graph

    # counters
    for_voting = 0
    against_voting = 0 

    for r in rounds:
        # check if blue ran out of energy or red ran out of followers
        if winning():
            # return name of winning agent 
            break

        else:
            if r == "red":
                if player == "r":
                    # execute player interactive function
                    # print number of followers
                elif ai == "r":
                    # execute minimax(?) function 
                # print percentage of people wanting to vote/ against voting 
            
            elif r == "blue":
                if player == "b":
                    # execute player interactive function
                    # print remaing energy amount 
                elif ai == "b":
                    # execute minimax(?) function 
                # print percentage of people wanting to vote/ against voting 
            
            elif r == "green":
                # interaction function (dfs?)
                # print percentage of people wanting to vote/ against voting 
        
    # election day 
    winner = max(for_voting, against_voting)
    if winner == for_voting:
        print("Blue wins!!\n")
    elif winer == against_voting:
        print("Red wins!!\n")
    else:
        print("It's a draw\n")


    
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

