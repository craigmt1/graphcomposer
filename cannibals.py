import networkx as nx 
import itertools as it


#create all the possible combinations
num_veg = 2
num_can = 2

if num_can > num_veg:
    print "There are more cannibals than vegetarians!"
    quit()
    
c = ['v']*num_veg
c += ['c']*num_can
c += ['b']

combos = []
for subset in it.permutations(c,len(c)):
    combos.append(list(subset))


set_combos = []
for item in combos:
    if item not in set_combos:
        set_combos.append(item)


veg_before = 0
can_before = 0
veg_after = 0
can_after = 0
valid = [] 


#retrieve a subset of the combinations that are valid. Valid if there aren't more cannibals than vegans before or after the boat, b.


#check island on the other side 
def check_other(combo_after):
    global veg_after
    global can_after
    for c in combo_after:
        if c == 'v':
            veg_after += 1
        if c == 'c':
            can_after += 1
    cont = False
    if veg_after >= can_after or veg_after == 0:
        cont = True
    veg_after = 0
    can_after = 0
    return cont 
    
def check_list_validity(combo):
    global veg_before
    global can_before
    for c in combo:
        if c == 'v':
            veg_before += 1
        if c == 'c':
            can_before += 1
        if c == 'b':
            if veg_before >= can_before or veg_before == 0: #check other side if this one is valid
                cont = check_other(combo[combo.index(c):])
            else:
                cont = False
            veg_before = 0
            can_before = 0
            if cont:
                valid.append(combo)
            break 
 
for combo in set_combos:
    check_list_validity(combo)



nodes = []

for v in valid:
    nodes.append("".join(v))

print nodes