'''
Genevie Caraan - 23070605
Daniel Loo - 23157127
'''

class green:

    def __init__(self, id, uncertainty, opinion):   #Initialises green node
        self.id = id
        self.uncertainty = uncertainty
        self.opinion = opinion

    def change_uncertainty(self, node, value_change):     #Modifies the uncertainty value of a node
        node.uncertainty += value_change
        # check opinion
        if node.uncertainty > 0:
            #wanting to vote, positive = for voting
            node.opinion = 1
        else:
            node.opinion = 0
        return self
    