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

def weightToStr(w):
    (v1, c1, v2, c2) = w
    return 'v' * v1 + 'c' * c1 + 'b' + 'v' * v2 + 'c' * c2

def main(num):
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
    #print all movesets
    i = 1
    for moveset in movesets:
        print('Move ' + str(i) + ': ' + str({weightToStr(w) for w in moveset}))
        i+=1
