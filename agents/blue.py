from gray import *
import random

class counterargument:
    def __init__(self, strength, energy_cost, type):
            self.strength = strength
            self.energy_cost = energy_cost
            self.type = type

class blue:
    #actions for blue agent
    def __init__(self, energy, gray_percent):
        self.energy = energy
        self.gray_percent = gray_percent

    def blue(self, greens, gray_percent):
        while True:
            condition = input("would you like to send a direct message or use a gray agent? (direct or gray)")
            if condition.strip().lower() in ['direct', 'gray']:
                break
            print("Invalid input")
        if (condition == 'direct'):
            #choose message level
            #spread message
            print("Choose:\n")

            print("1: Weak") 
            print("2: Moderately Weak") 
            print("3: Good") 
            print("4: Moderately Strong") 
            print("5: Strong") 
            print("\n")

            print(f"Current energy: {self.energy}\n")

            while True:
                choice = input("Please type the number of your choice (between 1 to 5): ")
                if  int(choice) >= 1 and  int(choice) <= 5:
                    break
                print("Invalid message. Try again. \n")
            
            energy_cost = 0
            strength = 0
            
            if int(choice) == 1:
                energy_cost = 2
                strength = 0.05
                type = "weak"
            elif int(choice) == 2:
                energy_cost = 4
                strength = 0.1
                type = "moderately weak"
            elif int(choice) == 3:
                energy_cost = 6
                strength = 0.15
                type = "good"
            elif int(choice) == 4:
                energy_cost = 8
                strength = 0.2
                type = "moderately strong"
            elif int(choice) == 5:
                energy_cost = 10
                strength = 0.25
                type = "strong"
            
            # create message
            message = counterargument(strength, energy_cost, type)
            print(f"You have chosen {message.type}!\n")
            if message.energy_cost >= self.energy :
                x = self.check()
                if(x == 1):
                    self.energy = 0
                    return greens
                else:
                    updated_recursive_greens = self.blue(greens)
                    return updated_recursive_greens

            else: # spread message
                updated_greens = self.spread_message(greens, message)
                self.energy = self.energy - message.energy_cost
                print(f"Your message has been received. Your remaining energy is {self.energy}")
                for u in updated_greens:
                    print("after blue:", u.uncertainty, u.opinion)
                return updated_greens
                # print stats of overall opinion(?)
        else:
            stance = ['blue', 'red']
            allegiance = random.choices(stance, weights=[gray_percent*10, (1-gray_percent)*10], k=10)
            print(allegiance)
            uncertainty = round(random.uniform(0.95, -1), 2)
            if allegiance[0] == "red":
                uncertainty *= -1
            print(gray_percent, "%")
            print(allegiance[0])
            gray_agent = gray(uncertainty, allegiance[0])
            greens = gray_agent.deploy_grey(greens) 
            return greens       

    def check(self):
        z = 0
        while True:
            condition = input("Insufficient energy, continue?(Y or N)")
            if condition.strip().lower() in ['y', 'n']:
                break
            print("Invalid input")
        if (condition.strip().lower() == 'y'):
            z = 1
            print("Blue died. Red wins!")
            return z
        else:
            z = 2
            return z

    def spread_message(self, greenarray, counterargument):
        for node in greenarray:
            node.uncertainty += counterargument.strength
            if node.uncertainty > 1:
                node.uncertainty = 1    
            if node.uncertainty > 0:
                node.opinion = 1
            elif node.uncertainty <= 0:
                node.opinion = 0
        return greenarray
    
    def deploy_grey(self, gray_percent, greens):
        print(f"Grey agent has been deployed")
        return self.graymove(gray_percent, greens)        

    def blue_ai(self, green):
        #bayesian
        return None
