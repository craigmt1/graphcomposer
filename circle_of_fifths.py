#!/usr/bin/env python

#Luke Rosenfeld, Craig Tateronis, Sridevi Suresh
#CS591 Professor Chin
#Final Project

import networkx as nx
import numpy
import random
from midiutil.MidiFile import MIDIFile


G=nx.Graph()

major = ["C","G","D","A","E","B","Gb","Db","Ab","Eb","Bb","F"]
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
major_chords[0][0] = "C"
major_chords[1][0] = "a"
major_chords[2][0] = "F"

major_chords[0][1] = "G"
major_chords[1][1] = "d"

major_chords[0][2] = "C"
major_chords[1][2] = "a"
major_chords[2][2] = "e"

major_chords[0][3] = "F"
major_chords[1][3] = "d"
major_chords[2][3] = "G"

major_chords[0][4] = "G"
major_chords[1][4] = "e"
major_chords[2][4] = "C"

major_chords[0][5] = "F"
major_chords[1][5] = "a"
major_chords[2][5] = "d"

major_chords[0][6] = "G"
major_chords[1][6] = "e"

melody = ("C", "major", [60,62,64,65,67])

midi_notes = {0:"C",1:"C#",2:"D",3:"D#",4:"E",5:"F",6:"F#",7:"G",8:"G#",9:"A",10:"A#",11:"B"}


def create_winsound(melody):
    key, maj_min, notes = melody
    MyMIDI = MIDIFile(1)
    track = 0   
    time = 0

    # Add track name and tempo.
    MyMIDI.addTrackName(track,time,"Sample Track")
    MyMIDI.addTempo(track,time,120)

    # Add a note. addNote expects the following information:
    counter = 0
    for note in notes:
        track = 0
        channel = 0
        pitch = note
        duration = 1
        volume = 100
        time = time + 4

        note_letter = midi_notes[pitch%12]

        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        if counter == 0:
            MyMIDI.addNote(track,channel,pitch-12,time,duration,volume)
            MyMIDI.addNote(track,channel,pitch-8,time,duration,volume)
            MyMIDI.addNote(track,channel,pitch-5,time,duration,volume)
        else:
            #stuff

        counter = counter + 1


        

    binfile = open("output2.mid", 'wb')
    MyMIDI.writeFile(binfile)
    binfile.close()

create_winsound(melody)




            


