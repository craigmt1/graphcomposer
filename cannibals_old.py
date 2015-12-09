#import networkx as nx 
import itertools as it
from operator import sub

def getWeight(s):
    #find distribution of cannibals and missionaries
    b_ind = s.index('b')
    s1, s2, = s[:b_ind], s[b_ind:]
    return (s1.count('v'), s1.count('c'), s2.count('v'), s2.count('c'))

def isValid(s):
    (v1, c1, v2, c2) = getWeight(s)
    if v1 and c1 > v1: return False
    if v2 and c2 > v2: return False
    return True

def getValidPermutations(start):
    #generate list of permutations that pass validity check
    return [''.join(subset) for subset in it.permutations(start,len(start)) if isValid(''.join(subset))]

#checks if s2 is possible next move for s1
def isNext(s1, s2):
    mask = tuple(map(sub, s1, s2))
    validMasks = [(1,0,-1,0), (0,1,0,-1)]
    if mask in validMasks: return True
    else: return False

def isValidPath(path):
    for i in range(len(path) - 1):
        if not isNext(path[i], path[i + 1]):
            return False
    return True

def weightToStr(w):
    (v1, c1, v2, c2) = w
    return 'v' * v1 + 'c' * c1 + 'b' + 'v' * v2 + 'c' * c2

def main(num, verbose = False):
    c = 'v' * num + 'c' * num + 'b'
    #get all valid permutations
    combos = getValidPermutations(c)

    #generate sets of moves at all stages
    movesets = [set() for i in c]
    for combo in combos:
        i = combo.index('b')
        movesets[i] |= {getWeight(combo)}

    #reverse movesets
    movesets = movesets[::-1]
    
    if verbose:
        #print all movesets
        print("Sets of possible moves at each stage.")
        i = 1
        for moveset in movesets:
            print('Move ' + str(i) + ': ' + str({w for w in moveset}))
            i+=1

    #generate all combinations of paths with movesets
    paths = list(it.product(*movesets))
    if verbose:
        #print them
        print("\nAll path combinations")
        for path in paths:
            print('Path: ' + str([step for step in path]))

    #check if paths are valid (every subsequent move for each path is possible)
    paths = [path for path in paths if isValidPath(path)]

    if verbose:
        #print remaining
        print("\nVALID:")
        for path in paths:
            print('Path: ' + str([step for step in path]))

    return paths
                
