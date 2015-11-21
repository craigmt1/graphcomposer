#!/usr/bin/env python

#Luke Rosenfeld, Craig Tateronis, Sridevi Suresh
#CS591 Professor Chin
#Final Project

import networkx as nx
import numpy

G=nx.Graph()

major = ["C","G","D","A","E","B","Gb","Db","Ab","Eb","Bb","F"]

major_dict = {"C":523.25,"G":783.99,"D":587.33,"A":880.00,"E":659.25,"B":987.77,"Gb":739.99,"Db":554.37,"Ab":830.61,"Eb":622.25,"Bb":932.33,"F":698.46}
minor = ["a","e","b","gb","db","ab","eb","bb","f","c","g","d"]

for chord in major:
    G.add_node(chord)

for chord in minor:
    G.add_node(chord)

for i in range(0, len(major)):
    G.add_edge(major[i], minor[i])
G.add_edge("F","C")

for i in range(0, len(minor)-1):
    G.add_edge(minor[i], minor[i+1])
G.add_edge("d","a")


major_chords = [[0 for x in range(7)] for x in range(3)] 
major_chords[0][0] = "I"
major_chords[1][0] = "vi"
major_chords[2][0] = "IV"

major_chords[0][1] = "V"
major_chords[1][1] = "ii"

major_chords[0][2] = "I"
major_chords[1][2] = "vi"
major_chords[2][2] = "iii"

major_chords[0][3] = "IV"
major_chords[1][3] = "ii"
major_chords[2][3] = "V"

major_chords[0][4] = "V"
major_chords[1][4] = "iii"
major_chords[2][4] = "I"

major_chords[0][5] = "IV"
major_chords[1][5] = "vi"
major_chords[2][5] = "ii"

major_chords[0][6] = "V"
major_chords[1][6] = "iii"

melody = ("C", "major", [3,5,7,1,2,3])


def create_winsound(melody):
    key, maj_min, notes = melody
    output = []

    for note in notes:
        










for x in major_chords:
    print(x)

