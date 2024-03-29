'''
Genevie Caraan - 23070605
Daniel Loo - 23157127
'''

import random

class message:
    def __init__(self, allegiance, potency, type):
        self.allegiance = allegiance
        self.potency = potency
        self.type = type
        
class gray:
    def __init__(self, uncertainty, allegiance):
        self.uncertainty = uncertainty
        self.allegiance = allegiance

    def deploy_grey(self, greens, gray_percent, intervals):
        potencies = [0.025, 0.05, 0.075, 0.1, 0.125]
        chosen_message = random.choice(potencies)

        if self.allegiance == "red":
            msg_types = ["Speech of Patriotism", "Propaganda", "Conspiracy", "Fake News", "Fear mongering"]
            propaganda = message("red", chosen_message * -1, msg_types[potencies.index(chosen_message)])
            # print(f"Gray is red team spy! It has chosen to spread {propaganda.type}\n")
            greens = self.spread_misinformation_gr(greens, propaganda, intervals[0])
            return greens[0], gray_percent, propaganda.type 
            
        elif self.allegiance == "blue":
            msg_types = ["Unifying Speech", "Mass-reporting", "Debunking and Fact-checking", "Law implementation on misinformation", "Democratic rallies"]
            counter = message("blue", chosen_message, msg_types[potencies.index(chosen_message)])
            # print(f"Gray gives blue team a hand! It chose to carry out {counter.type}\n")
            greens = self.spread_message_gr(greens, counter, intervals[1])
            return greens, gray_percent, counter.type

    def spread_misinformation_gr(self, array_green, message, min_interval):
        num_interact = 0
        for green in array_green:
            # to determine which nodes red can interact with: take the absolute value of red as maximum uncertainty red can interact with
            # example: let red have an uncertainty of -0.91; taking the absolute value, red can interact with green nodes with uncertainty 0.91 and below
            # red cannot gain back its persuasive power
            if abs(self.uncertainty) >= green.uncertainty:
                num_interact += 1
                #change the uncertainty of node
                green.uncertainty +=  message.potency
                if green.uncertainty < min_interval:
                    green.uncertainty = min_interval
            # check updated opinion
            if green.uncertainty <= 0:
                green.opinion = 0
        return array_green, num_interact

    def spread_message_gr(self, greenarray, message, max_interval):
        for node in greenarray:
            if (self.uncertainty * -1) <= node.uncertainty:
                node.uncertainty += message.potency
                if node.uncertainty > max_interval:
                    node.uncertainty = max_interval
                elif node.uncertainty < -1:
                    node.uncertainty = -1  
                if node.uncertainty > 0:
                    node.opinion = 1
                elif node.uncertainty <= 0:
                    node.opinion = 0
        return greenarray