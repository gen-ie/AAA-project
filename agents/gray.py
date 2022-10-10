from random import randint
from red import *
from blue import *

class message:
    def __init__(self, allegiance, potency, type) -> None:
        self.allegiance = allegiance
        self.potency = potency
        self.type = type
        
class gray:
    '''subclass of blue / actions of gray agent'''
    #number of gray nodes is expressed as PERCENTAGE in a parameter
    number = 0 #fix this later by adding parameter that allows the player/similuation to determin amt
    gray_type = randint(0,1)
    if gray_type == 0:
    #red gets to deploy a campaign WITHOUT red team losing followers

        print("gray is red")
        
    elif gray_type == 1:
        print("gray is blue")
    #blue gets another turn without losing life, lets gray agent out into network
    #gray agents know the amount of people who do/dont want to vote