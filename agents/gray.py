import random
from red import *
from blue import *

class message:
    def __init__(self, allegiance, potency, type):
        self.allegiance = allegiance
        self.potency = potency
        self.type = type
        
class gray:
    '''subclass of blue / actions of gray agent'''
    #number of gray nodes is expressed as PERCENTAGE in a parameter
    # number = 0 #fix this later by adding parameter that allows the player/similuation to determin amt
    # gray_type = randint(0,1)
    # if gray_type == 0:
    # #red gets to deploy a campaign WITHOUT red team losing followers
    #     print("gray is red")
        
        
    # elif gray_type == 1:
    #     print("gray is blue")
    #blue gets another turn without losing life, lets gray agent out into network
    #gray agents know the amount of people who do/dont want to vote
    def __init__(self, uncertainty, allegiance):
        self.uncertainty = uncertainty
        self.allegiance = allegiance

    def deploy_grey(self, gray_percent, greens):
        MAX_POTENCY = 0.25
        if self.allegiance == "red":
            propaganda = message("red", MAX_POTENCY * -1, "Fear Mongering")
            greens = self.spread_misinformation(greens, propaganda)
            return greens[0]
            
        elif self.allegiance == "blue":
            propaganda = message("blue", MAX_POTENCY, "ANTIFEAR")
            greens = self.spread_misinformation(greens, propaganda)
            return greens

    def spread_message(self, greenarray, message):
        for node in greenarray:
            node.uncertainty += message.potency
            if node.uncertainty > 1:
                node.uncertainty = 1
            elif node.uncertainty < 0:
                node.uncertainty = 0  
            if node.uncertainty > 0:
                node.opinion = 1
            elif node.uncertainty <= 0:
                node.opinion = 0
        return greenarray