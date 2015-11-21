import networkx as nx 
import itertools as it

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

def main(num):
    c = 'v' * num + 'c' * num + 'b'
    #get all valid permutations
    combos = getValidPermutations(c)
    #generate sets of moves at all stages
    movepositions = [set() for i in c]
    for combo in combos:
        i = combo.index('b')
        movepositions[i] |= {combo}

    #print all movesets (reversed)
    i = 1
    for moveset in movepositions[::-1]:
        print('Move ' + str(i) + ': ' + str(moveset))
        i+=1