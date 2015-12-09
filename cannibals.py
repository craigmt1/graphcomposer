

#http://www-formal.stanford.edu/jmc/elaboration/node2.html
class vector(object):
    def __init__(self, missionaries, cannibals, boats):
        self.missionaries = missionaries
        self.cannibals = cannibals
        self.boats = boats
    def __repr__(self):
        return str((self.missionaries, self.cannibals, self.boats))
    def __str__(self):
        return str((self.missionaries, self.cannibals, self.boats))
    def __sub__(self, other):
        return vector(self.missionaries - other.missionaries,\
                      self.cannibals - other.cannibals,\
                      self.boats - other.boats)
    def __add__(self, other):
        return vector(self.missionaries + other.missionaries,\
                      self.cannibals + other.cannibals,\
                      self.boats + other.boats)
    def __eq__(self, other):
        return self.missionaries == other.missionaries and self.cannibals == other.cannibals and self.boats == other.boats
    def move(self, other):
        if self.boats == 0: return self.__add__(other)
        else: return self.__sub__(other)
    def isGoal(self):
        return self.missionaries == 0 and self.cannibals == 0
    def isValid(self, total):
        if self.cannibals < 0 or self.missionaries < 0: return False
        if self.cannibals > total or self.missionaries > total: return False
        if self.cannibals > self.missionaries and self.missionaries > 0 : return False #check that there aren't more cannibals on left side 
        if (total - self.cannibals) > (total - self.missionaries) and (total - self.missionaries > 0): return False #right side 
        return True
    def display(self, total):
        return 'M' * self.missionaries + \
               'C' * self.cannibals + \
               '|' + str(self.boats) + '|' + \
               'M' * (total - self.missionaries) + \
               'C' * (total - self.cannibals)

class tree(object):
    def __init__(self, v, children, total, parent=None):
        self.v = v
        self.children = children
        self.winningPaths = []
        self.parent = parent
        self.total = total

    def __str__(self, level=0):
        out = '   '*level + str(self.v) + '\n'
        for child in self.children:
            if type(child) == tree:
                out += child.__str__(level + 1)
        return out

    def __repr__(self):
        return '<tree node representation>'

    def addWinningPath(self, moves=[]):
        #recursively generate path list back to starting node
        moves = [self.v] + moves
        if self.parent == None: self.winningPaths += [moves]
        else: self.parent.addWinningPath(moves)

    def inPath(self, v):
        #check to see if potential move has already been done (to avoid looping)
        if self.v == v: return True
        else:
            if self.parent == None: return False
            else: return self.parent.inPath(v)

    def genTree(self, movelist, level=0):
        #recursively generate children given list of permissible moves
        if self.v.isGoal(): self.addWinningPath()
        else:
            for m in movelist:
                nextv = self.v.move(m)
              #  print "NEXT V IS ", nextv
                if nextv.isValid(self.total) and not self.inPath(nextv):
                    nextTree = tree(nextv, [], self.total, self)
                    nextTree.genTree(movelist, level + 1)
                    self.children += [nextTree]

    def displayWinningPaths(self):
        print("Number of Complete Paths: " + str(len(self.winningPaths)))
        for path in self.winningPaths:
            print("\nPATH")
            for v in path:
                print(' ' + v.display(self.total))



def getPaths(numMC):
    if numMC <= 3:
        movelist = [vector(1,0,1), vector(2,0,1), vector(0,1,1), vector(0,2,1), vector(1,1,1)]
    else:
        movelist = [vector(i, j, 1) for i in range(numMC) for j in range(numMC) if (i, j) != (0,0) and (i + j) < numMC]
    start = vector(numMC,numMC,1)
    moveTree = tree(start, [], numMC)
    moveTree.genTree(movelist)
    print(moveTree)
    moveTree.displayWinningPaths()
    return moveTree
    