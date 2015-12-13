#!/usr/bin/env python

#Luke Rosenfeld, Craig Tateronis, Sridevi Suresh
#CS591 Professor Chin
#Final Project

# To run this program, type in a command line: python circle_of_fifths.py <note>
# where <note> is either "C" or "a". This program works in one key, that is, C (diatonic) major, which is 
# equivalent to A minor. By entering "C" or "a", the user can choose whether the output should be in a minor
# or major key. The output of this program is a file named "harmony.mid", so any user will need an application that can
# open this type of file. I personally recommend GarageBand from iTunes, but there are many on the web. 
# This program uses an external open source library called MIDIUtil (not written by Luke Craig or Sridevi).
# Note: please be sure to look at the comments next to "melody" below for legal input values. 

import networkx as nx
import numpy
import random
from midiutil.MidiFile import MIDIFile
import math
import sys


G=nx.Graph()

major = ["C","G","D","A","E","B","Gb","Db","Ab","Eb","Bb","F"]
minor = ["a","e","b","gb","db","ab","eb","bb","f","c","g","d"]

for chord in major:
    G.add_node(chord)

for chord in minor:
    G.add_node(chord)

for i in range(0, len(major)):
    G.add_edge(major[i], minor[i])

for i in range(0, len(minor)-1):
    G.add_edge(minor[i], minor[i+1])
G.add_edge("d","a")

for i in range(0, len(major)-1):
    G.add_edge(major[i], major[i+1])
G.add_edge("F","C")


chords_matrix = [[0 for x in range(12)] for x in range(3)] 
chords_matrix[0][0] = "C"
chords_matrix[1][0] = "a"
chords_matrix[2][0] = "F"

chords_matrix[0][2] = "G"
chords_matrix[1][2] = "d"
chords_matrix[2][2] = 0 # 0's are for the two notes (in a given key) that only can result in two 
                        # chords, rather than three. 

chords_matrix[0][4] = "C"
chords_matrix[1][4] = "a"
chords_matrix[2][4] = "e"

chords_matrix[0][5] = "F"
chords_matrix[1][5] = "d"
chords_matrix[2][5] = "G"

chords_matrix[0][7] = "G"
chords_matrix[1][7] = "e"
chords_matrix[2][7] = "C"

chords_matrix[0][9] = "F"
chords_matrix[1][9] = "a"
chords_matrix[2][9] = "d"

chords_matrix[0][11] = "G"
chords_matrix[1][11] = "e"
chords_matrix[2][11] = 0

melody = [60,64,67,69,74,76,72] # some sample inputs that work in C major or A minor: [60,64,67,72] [60,64,67,69,74,76,72] [60,62,65,64,62,60,64,65,69,71,72] [60,64,67,64,60] [60,62,67,55,60] [60,62,67,71,72,79]
# melody notes must be in the C major or A minor diatonic scale. That means, all input notes must be in the a congruence class equal to:
# 60 mod 12, 62 mod 12, 64 mod 12, 65 mod 12, 67 mod 12, 69 mod 12, or 71 mod 12 
# The first chord is assumed to be the root chord. Therefore, the first melody node that you input must
# be a proper note for the key that you input, either "C" or "a". To simplify, I will show the possibilities for the first note:
# If you enter 'python circle_of_fifths.py "C"': the first melody note must be in a C major chord: any number in a congruence class of 60 mod 12, 64 mod 12, or 67 mod 12
# If you enter 'python circle_of_fifths.py "a"': the first melody note must be in an A minor chord: any number in a congruence class of 57 mod 12, 60 mod 12, or 64 mod 12
# having input notes in the 50-80 range is a good, medium range of notes

num_to_note = {0:"C",1:"C#",2:"D",3:"D#",4:"E",5:"F",6:"F#",7:"G",8:"G#",9:"A",10:"A#",11:"B"}
note_to_num = {"C":0,"C#":1,"D":2,"D#":3,"E":4,"F":5,"F#":6,"G":7,"G#":8,"A":9,"A#":10,"B":11}

def create_harmony(nextChord, melody):
    notes = melody
    MyMIDI = MIDIFile(1)
    track = 0   
    time = 0

    # Add track name and tempo.
    MyMIDI.addTrackName(track,time,"Sample Track2")
    MyMIDI.addTempo(track,time,120)

    # Add a note. addNote expects the following information:
    counter = 0

    for note in notes: #play the melody alone first
        track = 0
        channel = 0
        pitch = note
        duration = 2
        volume = 100
        time = time + 3
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)

    time = time + 3

    for note in notes: #now add harmonies
        track = 0
        channel = 0
        pitch = note
        duration = 2
        volume = 100
        time = time + 3

        note_letter = num_to_note[pitch%12]
        print "note letter: " + note_letter
        chords = []
        for x in range(0,3):
            chords.append(chords_matrix[x][pitch%12])

        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        if counter == 0: # first chord is always root chord by default
            if nextChord.isupper(): # is it's uppercase, then it's a major chord
                if note_letter == nextChord: # root inversion
                    MyMIDI.addNote(track,channel,pitch-12,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-8,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-5,time,duration,volume)
                if math.fabs(note_to_num[note_letter] - note_to_num[nextChord]) == 5 or math.fabs(note_to_num[note_letter] - note_to_num[nextChord]) == 7: #second inversion
                    MyMIDI.addNote(track,channel,pitch-12,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-3,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-7,time,duration,volume)
                if math.fabs(note_to_num[note_letter] - note_to_num[nextChord]) == 4 or math.fabs(note_to_num[note_letter] - note_to_num[nextChord]) == 8: #first inversion
                    MyMIDI.addNote(track,channel,pitch-12,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-4,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-9,time,duration,volume)
            else: # if it's lowercase, then it's a minor chord
                if note_letter == nextChord.upper(): # root inversion
                    MyMIDI.addNote(track,channel,pitch-12,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-9,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-5,time,duration,volume)
                if math.fabs(note_to_num[note_letter] - note_to_num[nextChord.upper()]) == 5 or math.fabs(note_to_num[note_letter] - note_to_num[nextChord.upper()]) == 7: #second inversion
                    MyMIDI.addNote(track,channel,pitch-12,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-4,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-7,time,duration,volume)
                if math.fabs(note_to_num[note_letter] - note_to_num[nextChord.upper()]) == 3 or math.fabs(note_to_num[note_letter] - note_to_num[nextChord.upper()]) == 9: #first inversion
                    MyMIDI.addNote(track,channel,pitch-12,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-3,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-8,time,duration,volume)

        else: 
            path1 = nx.shortest_path(G, source=nextChord, target=chords[0]) # find shortest path to next possible chords and pick the one with shortest distance
            path2 = nx.shortest_path(G, source=nextChord, target=chords[1]) 
            path3 = [0]*20
            if chords_matrix[2][notes[counter]%12] != 0: path3 = nx.shortest_path(G, source=nextChord, target=chords[2])
            chords_list = [(path1, len(path1)), (path2, len(path2)), (path3, len(path3))]
            chords_list.sort(key=lambda tup: tup[1]) # sort them so it's easy to find which chord has the shortest path
            l, length = chords_list[0]
            if length != 1: # make sure it's not the same chord that was just played
                nextChord = l[length - 1]
            else:
                l, length = chords_list[1]
                nextChord = l[length - 1]
            if nextChord.isupper(): # is it's uppercase, then it's a major chord
                if note_letter == nextChord: # root inversion
                    MyMIDI.addNote(track,channel,pitch-12,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-8,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-5,time,duration,volume)
                if math.fabs(note_to_num[note_letter] - note_to_num[nextChord]) == 5 or math.fabs(note_to_num[note_letter] - note_to_num[nextChord]) == 7: #second inversion
                    MyMIDI.addNote(track,channel,pitch-12,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-3,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-7,time,duration,volume)
                if math.fabs(note_to_num[note_letter] - note_to_num[nextChord]) == 4 or math.fabs(note_to_num[note_letter] - note_to_num[nextChord]) == 8: #first inversion
                    MyMIDI.addNote(track,channel,pitch-12,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-4,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-9,time,duration,volume)
            else: # if it's lowercase, then it's a minor chord
                if note_letter == nextChord.upper(): # root inversion
                    MyMIDI.addNote(track,channel,pitch-12,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-9,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-5,time,duration,volume)
                if math.fabs(note_to_num[note_letter] - note_to_num[nextChord.upper()]) == 5 or math.fabs(note_to_num[note_letter] - note_to_num[nextChord.upper()]) == 7: #second inversion
                    MyMIDI.addNote(track,channel,pitch-12,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-4,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-7,time,duration,volume)
                if math.fabs(note_to_num[note_letter] - note_to_num[nextChord.upper()]) == 3 or math.fabs(note_to_num[note_letter] - note_to_num[nextChord.upper()]) == 9: #first inversion
                    MyMIDI.addNote(track,channel,pitch-12,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-3,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-8,time,duration,volume)

        print "chord: " + nextChord

        counter = counter + 1

    binfile = open("harmony.mid", 'wb')
    MyMIDI.writeFile(binfile)
    binfile.close()

nextChord = sys.argv[1]
create_harmony(nextChord, melody)

