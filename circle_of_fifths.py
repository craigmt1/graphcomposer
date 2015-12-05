#!/usr/bin/env python

#Luke Rosenfeld, Craig Tateronis, Sridevi Suresh
#CS591 Professor Chin
#Final Project

import networkx as nx
import numpy
import random
from midiutil.MidiFile import MIDIFile
import math


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


major_chords = [[0 for x in range(12)] for x in range(3)] 
major_chords[0][0] = "C"
major_chords[1][0] = "a"
major_chords[2][0] = "F"

major_chords[0][2] = "G"
major_chords[1][2] = "d"
major_chords[2][2] = 0

major_chords[0][4] = "C"
major_chords[1][4] = "a"
major_chords[2][4] = "e"

major_chords[0][5] = "F"
major_chords[1][5] = "d"
major_chords[2][5] = "G"

major_chords[0][7] = "G"
major_chords[1][7] = "e"
major_chords[2][7] = "C"

major_chords[0][9] = "F"
major_chords[1][9] = "a"
major_chords[2][9] = "d"

major_chords[0][11] = "G"
major_chords[1][11] = "e"
major_chords[2][11] = 0


melody = [60,62,67,71,72,79] # [60,64,67,69,74,76,72] [60,62,65,64,62,60,64,65,69,71,72] [60,64,67,64,60] [60,62,67,55,60] [60,62,67,71,72,79]

num_to_note = {0:"C",1:"C#",2:"D",3:"D#",4:"E",5:"F",6:"F#",7:"G",8:"G#",9:"A",10:"A#",11:"B"}
note_to_num = {"C":0,"C#":1,"D":2,"D#":3,"E":4,"F":5,"F#":6,"G":7,"G#":8,"A":9,"A#":10,"B":11}

def create_harmony(melody):
    notes = melody
    MyMIDI = MIDIFile(1)
    track = 0   
    time = 0

    # Add track name and tempo.
    MyMIDI.addTrackName(track,time,"Sample Track2")
    MyMIDI.addTempo(track,time,120)

    # Add a note. addNote expects the following information:
    counter = 0
    nextChord = "C"

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
        chords = []
        for x in range(0,3):
            chords.append(major_chords[x][pitch%12])

        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        if counter == 0: # first chord is always root chord
            MyMIDI.addNote(track,channel,pitch-12,time,duration,volume)
            MyMIDI.addNote(track,channel,pitch-8,time,duration,volume)
            MyMIDI.addNote(track,channel,pitch-5,time,duration,volume)
        else: 
            path1 = nx.shortest_path(G, source=nextChord, target=chords[0]) # find shortest path to next possible chords and pick the one with shortest distance
            path2 = nx.shortest_path(G, source=nextChord, target=chords[1]) # could use shortest_path_length instead
            path3 = [0]*20
            if major_chords[2][notes[counter]%12] != 0: path3 = nx.shortest_path(G, source=nextChord, target=chords[2])
            chords_list = [(path1, len(path1)), (path2, len(path2)), (path3, len(path3))]
            chords_list.sort(key=lambda tup: tup[1])
            l, length = chords_list[0]
            if length != 1:
                nextChord = l[length - 1]
            else:
                l, length = chords_list[1]
                nextChord = l[length - 1]
            if nextChord.isupper(): # is it's uppercase, then it's a major chord
                if note_letter == nextChord: # root inversion
                    MyMIDI.addNote(track,channel,pitch-12,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-8,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-5,time,duration,volume)
                if math.fabs(note_to_num[note_letter] - note_to_num[nextChord]) == 5: # second inversion
                    MyMIDI.addNote(track,channel,pitch-12,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-3,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-7,time,duration,volume)
                if math.fabs(note_to_num[note_letter] - note_to_num[nextChord]) == 4: #first inversion
                    MyMIDI.addNote(track,channel,pitch-12,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-4,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-9,time,duration,volume)
            else: # if it's lowercase, then it's a minor chord
                if note_letter == nextChord.upper(): # root inversion
                    MyMIDI.addNote(track,channel,pitch-12,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-9,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-5,time,duration,volume)
                if math.fabs(note_to_num[note_letter] - note_to_num[nextChord.upper()]) == 5: # second inversion
                    MyMIDI.addNote(track,channel,pitch-12,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-4,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-7,time,duration,volume)
                if math.fabs(note_to_num[note_letter] - note_to_num[nextChord.upper()]) == 3: #first inversion
                    MyMIDI.addNote(track,channel,pitch-12,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-3,time,duration,volume)
                    MyMIDI.addNote(track,channel,pitch-8,time,duration,volume)

        print(nextChord)

        counter = counter + 1

    binfile = open("harmony.mid", 'wb')
    MyMIDI.writeFile(binfile)
    binfile.close()

create_harmony(melody)

