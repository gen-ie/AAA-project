from gray import *
import random

class counterargument:
    def __init__(self, strength, energy_cost, type):
            self.strength = strength
            self.energy_cost = energy_cost
            self.type = type

class blue:
    #actions for blue agent
    def __init__(self, energy, unsureness, gray_percent):
        self.energy = energy
        self.unsureness = unsureness
        self.gray_percent = gray_percent

    def blue_player(self, greens, gray_percent, intervals):
        while True:
            condition = input("would you like to send a direct message or use a gray agent (direct or gray)? ")
            if condition.strip().lower() in ['direct', 'gray']:
                break
            print("Invalid input")
        if (condition == 'direct'):
            #choose message level
            #spread message
            print("Choose:\n")

            print("1: Unifying Speech  (Remind people of the truth and democratic values) - tame message") 
            print("2: Mass-reporting (Reporting of social media accounts that deliberately spread misinformation) - moderately tame message") 
            print("3: Debunking and Fact-checking (Calling out false information with information from proper sources) - moderately effective message") 
            print("4: Law implementation on misinformation") 
            print("5: Democratic rallies (Peaceful protests for preserving democratic values) - powerful message") 
            print("\n")

            print(f"Current energy: {self.energy}\n")

            while True:
                choice = input("Please type the number of your choice (between 1 to 5): ")
                try:
                    if  int(choice) >= 1 and  int(choice) <= 5:
                        break
                    print("Invalid message. Try again. \n")
                except ValueError:
                    print("Invalid output. Please try again\n")
            
            message = self.create_counterargument(choice)
            print(f"You have chosen {message.type}!\n")
            
            if message.energy_cost >= self.energy :
                x = self.check()
                if(x == 1):
                    self.energy = 0
                    return greens,gray_percent
                else:
                    updated_recursive_greens = self.blue(greens, gray_percent, intervals)
                    return updated_recursive_greens

            else: # spread message
                updated_greens = self.spread_message(greens, message, intervals[1])
                self.energy = self.energy - message.energy_cost
                print(f"Your message has been received. Your remaining energy is {self.energy}")
                # for u in updated_greens:
                #     print("after blue:", u.unsureness, u.opinion)
                return updated_greens, gray_percent
                # print stats of overall opinion(?)
        else:
            unsureness, allegiance = self.create_gray(gray_percent)
            gray_agent = gray(unsureness, allegiance)
            greens, gray_p, msg = gray_agent.deploy_grey(greens, gray_percent, intervals) 
            print("\nBlue chose to deploy Gray!")
            if gray_agent.allegiance == "red":
                print(f"Unfortanetly, it was a spy! It has spread {msg}!")
            elif gray_agent.allegiance == "blue":
                print(f"Gray gave blue team a hand! It has carried out {msg}!")
            return greens, gray_p 

    def create_gray(self, gray_percent):
        stance = ['blue', 'red']
        allegiance = random.choices(stance, weights=[gray_percent*10, (1-gray_percent)*10], k=10)
        unsureness = round(random.uniform(0.95, 1), 2)
        if allegiance[0] == "red":
            unsureness *= -1
        return unsureness, allegiance[0]

    def create_counterargument(self, choice):
        energy_cost = 0
        strength = 0
        
        if int(choice) == 1:
            energy_cost = 2
            strength = 0.05
            type = "Unifying Speech"
        elif int(choice) == 2:
            energy_cost = 4
            strength = 0.1
            type = "Mass-reporting"
        elif int(choice) == 3:
            energy_cost = 6
            strength = 0.15
            type = "Debunking and Fact-checking"
        elif int(choice) == 4:
            energy_cost = 8
            strength = 0.2
            type = "Law implementation on misinformation"
        elif int(choice) == 5:
            energy_cost = 10
            strength = 0.25
            type = "Democratic rallies"
        
        # create message
        message = counterargument(strength, energy_cost, type)
        return message

    def check(self):
        z = 0
        while True:
            condition = input("Insufficient energy, continue?(Y or N)")
            if condition.strip().lower() in ['y', 'n']:
                break
            print("Invalid input")
        if (condition.strip().lower() == 'y'):
            z = 1
            # print("Blue died. Red wins!")
            return z
        else:
            z = 2
            return z

    def spread_message(self, greenarray, counterargument, extrm_interval):
        for node in greenarray:
            # unsureness of blue: blue can only shift nodes that have (self.unsureness * -1) or more
            # Example: lets say blue has an unsureness of 0.99, it can only persuade nodes with uncertainties -0.99 and above
            if (self.unsureness * -1) <= node.uncertainty:
                node.uncertainty += counterargument.strength
                if node.uncertainty > extrm_interval:
                    node.uncertainty = extrm_interval    
                if node.uncertainty > 0:
                    node.opinion = 1
                elif node.uncertainty <= 0:
                    node.opinion = 0
        return greenarray
    
    def deploy_grey(self, gray_percent, greens):
        print(f"Grey agent has been deployed")
        return self.graymove(gray_percent, greens)        
