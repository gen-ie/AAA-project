class propaganda:
    def __init__(self, interval, potency, message):
        self.interval = interval
        self.potency = potency
        self.message = message

class red:
    '''actions for red agent'''
    def __init__(self, uncertainty):
        self.uncertainty = uncertainty
    
    def spread_misinformation(array_green, agent, message):
        '''
        for green in nodes (loop through all the nodes):
            #effectiveness - if random number is smaller than uncertainty value of agent, spread message to them 
            eff = round(random.uniform(-0.7, -1), 2)

            if eff > agent:
                #change the uncertainty of node
                green.uncertainty = green.uncertainty + message.potency
                if green.uncertainty > 1:
                    green.uncertainty = 1
            else:
                do nothing, move to next node
        '''

    def minimax():