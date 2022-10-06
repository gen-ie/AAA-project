class counterargument:
    def intialise(self, strength, energycost, type):
            self.strength = strength
            self.energycost = energycost
            self.type = type

class blue:
    #actions for blue agent
    def initialise(self, energy):
        self.energy = energy

    def blue(self, greens, grey_interval):
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

                print(f"Energy remaining: {self.energy}\n")

                while True:
                    choice = input("Please type the number of your choice (between 1 to 5): ")
                    if  choice >= 1 and  choice <= 5:
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
                message = counterargument(energy_cost, strength, type)
                print(f"You have chosen {message.type}!\n")
                '''if message.energy_cost > self.energy:
                    while True:
                        condition = input("insufficient energy, continue?(Y or N)")
                        if condition.strip().lower() in ['Y', 'N']:
                            break
                        print("Invalid input")
                    if (condition.strip().lower() == 'Y')
                        #red is winner
                        winner = red
                        game end() #return winner and final state(?)
                    else
                        BlueAction()
                        break'''

                # spread message
                self.spread_message(greens, message)
                print(f"Your message has been received. Your remaining energy is {self.energy}")
                # print stats of overall opinion
            else:
                self.deploy_grey()           

    def spread_message(self, greenarray, counterargument):
        for node in greenarray:
            node.uncertainty += counterargument.strength
            if node.uncertainty > 1:
                node.uncertainty = 1
    
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
