'''
Genevie Caraan - 23070605
Daniel Loo - 23157127
'''

class propaganda:
    def __init__(self, follower_lose, potency, type):
        '''
        follower_lose = how much would the uncertainty of red will shift to the RIGHT (becomes more positive)after spreading the message; the more right on the scale red agent is, the less persuasive it is
        potency = how much the uncertainty of green nodes will change after the propaganda has been spread; aims to shift the nodes LEFT 
        type = displays the level of message
        '''
        self.follower_lose = follower_lose
        self.potency = potency
        self.type = type

class red:
    '''actions for red agent'''
    def __init__(self, uncertainty):
        self.uncertainty = uncertainty
    
    def spread_misinformation(self, array_green, message, extrm_interval):
        num_interact = 0
        for green in array_green:
            # to determine which nodes red can interact with: take the absolute value of red as maximum uncertainty red can interact with
            # example: let red have an uncertainty of -0.91; taking the absolute value, red can interact with green nodes with uncertainty 0.91 and below
            # red cannot gain back its persuasive power 
            if abs(self.uncertainty) >= green.uncertainty:
                num_interact += 1
                #change the uncertainty of node
                green.uncertainty +=  message.potency
                if green.uncertainty < extrm_interval:
                    green.uncertainty = extrm_interval
            # check updated opinion
            if green.uncertainty <= 0:
                green.opinion = 0
        # decrease red's persuasive power
        self.uncertainty += message.follower_lose
        if self.uncertainty > 0:
            self.uncertainty = 0

        return array_green, num_interact

    def create_propaganda(self, choice):
        persuasiveness_decrease = 0
        potency = 0
        type = ""
         
        if int(choice) == 1:
            persuasiveness_decrease = 0.05 
            potency = -0.05
            type = "Speech of Patriotism"
        elif int(choice) == 2:
            persuasiveness_decrease = 0.01
            potency = -0.1
            type = "Propaganda"
        elif int(choice) == 3:
            persuasiveness_decrease = 0.15
            potency = -0.15
            type = "Conspiracy"
        elif int(choice) == 4:
            persuasiveness_decrease = 0.2
            potency = -0.2
            type = "Fake News"
        elif int(choice) == 5:
            persuasiveness_decrease = 0.25
            potency = -0.25
            type = "Fear mongering"

        # create message
        message = propaganda(persuasiveness_decrease, potency, type)
        return message

    def red_player(self, green_nodes, intervals):
        print("You have a choice of five types of messages to send out:\n")
        print("1: Speech of Patriotism (Showcase your loyalty to sway people) - tame message") 
        print("2: Propaganda (Boast your accomplisments) - moderately tame message. Can affect a lot of people") 
        print("3: Conspiracy (Suggest ideas to unspecting citizens) - moderately effective message. Can affect some people") 
        print("4: Fake News (Fabricate evidence in order to succeed) - highly effective message. Can affect only a handful of certain people") 
        print("5: Fear mongering (Indoctrinate the people through scare tactics) - heavily potent message. Can only affect uncertain people") 
        print("\n")

        print(f"Current uncertainty: {self.uncertainty}")
        print(f"Current number of followers: {len(green_nodes)}\n")

        while True:
            try:
                message_choice = input("Please type the number of your choice (between 1 to 5): ")
                if int(message_choice) >= 1 and int(message_choice) <= 5:
                    break
                print("Invalid message type.\n")
            except ValueError:
                print("Invalid message type.\n")

        message = self.create_propaganda(message_choice)
        print(f"You have chosen {message.type}!\n")

        # spread message
        updated_nodes, num_interact = self.spread_misinformation(green_nodes, message, intervals[0])
        print(f"You have interacted with {num_interact} nodes")
        print(f"Updated uncertainty: {self.uncertainty}\n")
        return updated_nodes




        





