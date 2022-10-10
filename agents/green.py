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
    
    
    ''' 
    def DFS(self, graph, visited, currentnode, green_array):     #Navigates through graph and returns an array of node pairs
        neighbours = graph[currentnode]
        v = visited
        
        for n in neighbours:
            if (n not in visited):
                # update the array
                v.append(n)
                self.DFS(graph, v, n)
        return (node1, node2)
        '''
    # def find_path(dictionary, start_word, end_word):
    # '''
    # returns a list of the word in the shortest path 
    # from start_word to end_word, 
    # where successive words are different in only one letter.
    # '''
    #     adj_lists = createGraph(dictionary)
    #     visited = []
    #     shortest_seq = [start_word]
    #     return dfs(adj_lists, start_word, visited, shortest_seq, end_word)


    # def dfs(dictionary, word, visited, sequence, target):
    #     print(sequence)
    #     if (target in sequence):
    #         return sequence
    #     if word not in visited:
    #         #counter
    #         # child_added = 0
    #         #add the children 
    #         for adj in dictionary[word]:
    #             if (adj not in visited) and (adj not in sequence) and (target not in sequence):
    #                 sequence.append(adj)
    #                 dfs(dictionary, adj, visited, sequence, target)
    #                 # child_added += 1
    #                 visited.append(adj)

    #     if (sequence[-1] != target):
    #         sequence.remove(word)
    #     return sequence

    '''
    Import random module
    Initialise()
    Initalise uncertainy RANGE of the green agents VIA INPUTS by using random e.g. (-0.5 to 0.5)
    Initalise opinion RANGE of the green agents similar to uncertainty range constraints 
    [All the green agents will be within this interval at the START of the game
    as rounds progress the uncertainty of green players will slowly shift away from the range]
    Initalise visited status

    Interact(graph,start)
    Nodes can only interact with neighbouring nodes they share an edge with
    NOTe: If a neutral node interacts with a node with an opinion (e.g. one more swayed by red team's message), its uncertainty level will go up(towards red).
    
    Undirected 
    
    In graph, we loop through each node DFS STACK
        For each node, we will loop through ALL of their adjacent neighbours 
        Change the node's visited status to visited
        abs(x) and abs(y)
        if x < y:
            y affects x's opinion and uncertainty changes 
            add to visisted array

        Elif x > y:
            x affects y's opinion and uncertainty changes 
            Add to visited array
        Else:
        nothing
        If there are any more adjacent neighbours that hasnt been visited, loop continues to next node thats connected
        If there are no more neighbours that isnt in array; go onto the onto the next node
    
    Once every node is in the visited array:
    End of round, ALL visited status gets reset to unvisited, array is reset
    '''

    #potential internet literacy, a probability(?) that affects whether or not theyre affected by the red team's message
    ''' 
    
    Other method: We compare the uncertainty value of each one(all values have +1)
    If  current node(x) is (((0-X) < (0-Y)) < ((2-X) < (2-Y)))   [more closer to 0 or closer to 2 than the other node]:
         Then the other node's(Y) opinion becomes swayed to more certain to vote(blue side)
    Elif same thing but other direction: X opionion has changed
    else: nothing changed
    (whichever one is on the further end, add one to every value) when changing the undercertainty, you change the stance/opinion
    (two red nodes = more certain, less certain one becomes more red)
    only one node gets influenced'''