from random import randint
class gray:
    '''subclass of blue / actions of gray agent'''
    #number of gray nodes is expressed as PERCENTAGE in a parameter
    def initialise(self, number):
        self.number=  number
    #fix this later by adding parameter that allows the player/similuation to determin amt
    def gray(self,):
    gray_type = randint(0,1)
    if gray_type == 0:
    #red gets to deploy a campaign WITHOUT red team losing followers

        print("gray is red")
        
    elif gray_type == 1:
        print("gray is blue")
    #blue gets another turnh without losing life, lets gray agent out into network
    #gray agents know the amount of people who do/dont want to vote