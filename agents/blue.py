class counterargument:
    def __init__(self, strength, energy_cost, type):
            self.strength = strength
            self.energy_cost = energy_cost
            self.type = type

class blue:
    #actions for blue agent
    def __init__(self, energy):
        self.energy = energy

    def blue(self, greens):
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
                while True:
                    condition = input("Insufficient energy, continue?(Y or N)")
                    if condition.strip().lower() in ['y', 'n']:
                        break
                    print("Invalid input")
                if (condition.strip().lower() == 'y'):
                    #red is winner
                    '''winner = red
                    game end() #return winner and final state(?)'''
                    print("Blue died. Red wins!")
                    return 
                else:
                    self.blue(greens)
                    return

            else: # spread message
                updated_greens = self.spread_message(greens, message)
                self.energy = self.energy - message.energy_cost
                print(f"Your message has been received. Your remaining energy is {self.energy}")
                for u in updated_greens:
                    print("after blue:", u.uncertainty, u.opinion)
                return updated_greens
                # print stats of overall opinion(?)
        '''else:
            self.deploy_grey()'''           

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
    
    def deploy_grey(self):
        gray = gray()
        gray.function
        #if grey is blue
            #spread blue message(max)
        #if grey is red
            #spread red message(max)
        print(f"Grey agent has been deployed and finished spreading its message.")

    def blue_ai(self, green):
        #bayesian
        return None
