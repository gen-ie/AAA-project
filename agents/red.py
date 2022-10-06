import random

class propaganda:
    def __init__(self, interval, potency, type):
        self.interval = interval
        self.potency = potency
        self.type = type

class red:
    '''actions for red agent'''
    def __init__(self, opinion, uncertainty):
        self.opinion = opinion
        self.uncertainty = uncertainty
    
    def spread_misinformation(self, array_green, message):
        for green in array_green:
            #effectiveness - if random number is smaller than uncertainty value of agent, spread message to them 
            # eff = round(random.uniform(-0.7, -1), 2)

            if message.max_interval > green.uncertainty:
                #change the uncertainty of node
                green.uncertainty = green.uncertainty + message.potency
                if green.uncertainty < -1:
                    green.uncertainty = -1

    def num_followers(self, message, green_nodes):
        followers = 0
        max_interval = message.max_interval
        for g in green_nodes:
            if g.uncertainty < max_interval:
                followers += 1
        return followers

    def red_player(self, green_nodes):
        print("You have a choice of five types of messages to send out:\n")

        print("1: Speech of Patriotism (Showcase your loyalty to sway people) - tame message. Can affect most people (uncertainty below 0.8)") 
        print("2: Propaganda (Boast your accomplisments) - moderately tame message. Can affect a lot of people (uncertainty below 0.6)") 
        print("3: Conspiracy (Suggest ideas to unspecting citizens) - moderately effective message. Can affect some people (uncertainty below 0.4)") 
        print("4: Fake News (Fabricate evidence in order to succeed) - highly effective message. Can affect only a handful of certain people (uncertainty below 0.2)") 
        print("5: Fear mongering (Indoctrinate the people through scare tactics) - heavily potent message. Can only affect uncertain people (uncertainty of below 0)") 
        print("\n")

        print(f"Current number of followers: {len(green_nodes)}\n")

        while True:
            message_choice = input("Please type the number of your choice (between 1 to 5): ")
            if message_choice >= 1 and message_choice <= 5:
                break
            print("Invalid message type.\n")
        
        max_interval = 0
        potency = 0
        type = ""
         
        if int(message_choice) == 1:
            max_interval = 0.8
            potency = -0.05
            type = "Speech of Patriotism"
        elif int(message_choice) == 2:
            max_interval = 0.6
            potency = -0.1
            type = "Propaganda"
        elif int(message_choice) == 3:
            max_interval = 0.4
            potency = -0.15
            type = "Conspiracy"
        elif int(message_choice) == 4:
            max_interval = 0.2
            potency = -0.2
            type = "Fake News"
        elif int(message_choice) == 5:
            max_interval = 0
            potency = -0.25
            type = "Fear mongering"
        
        # create message
        message = propaganda(max_interval, potency, type)
        print(f"You have chosen {message.type}!\n")
        # number of interacted followers
        num_follow = self.num_followers(message, green_nodes)

        # spread message
        self.spread_misinformation(green_nodes, message)
        print(f"You have interacted with {num_follow} nodes")
        # print stats of overall opinion
 
    def red_ai(green_nodes):
        # minimax
        # scoring system: number of nodes that do not want to vote
        # depth; 2-player
        return 1


