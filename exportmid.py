from midiutil.MidiFile import MIDIFile

def writeNotes(midobj, notes):
	for note in notes:
		# Add a note. addNote expects the following information:
		(track, channel, pitch, time, duration, volume) = note
		# Now add the note.
		midobj.addNote(track,channel,pitch,time,duration,volume)

def writeMID(filename, tempo, notes):
	# Create the MIDIFile Object with 1 track
	MyMIDI = MIDIFile(1)

	# Tracks are numbered from zero. Times are measured in beats.
	track = 0   
	time = 0

	# Add track name and tempo.
	MyMIDI.addTrackName(track,time,"Sample Track")
	MyMIDI.addTempo(track,time,tempo)

	# And write it to disk.
	binfile = open(filename, 'wb')
	MyMIDI.writeFile(binfile)
	binfile.close()

def test():
	filename = "test.mid"
	tempo = 120
	notes = [(0,0,60,0,1,100),(0,0,64,0,1,100)]
	writeMID(filename, tempo, notes)