import json
import logging
import os
import discord
import asyncio
import pygame.midi
import time
from midiutil.MidiFile import MIDIFile
import os
from midi2audio import FluidSynth

from discord.ext import commands

client = discord.Client()
TOKEN = "MzE5NzMzMDU1MjQzODEyODc3.DBFUcA.8dg_jrHERZbG17sjetKMwqhUmNA"

bot = commands.Bot(command_prefix= '?', description='');
pygame.midi.quit()
pygame.midi.init()
global player
player = pygame.midi.Output(0)
player.set_instrument(0)
global ton
ton = 64
global sleeptime
sleeptime = 120
global chords
global isTierce
isTierce = False
global song
song = {}
global construction
global midiCounter
global midifile

construction = ['INTRO', 'COU', 'REF','COU','REF','PONT','REF']

@bot.event
async def on_ready():
    global song
    global construction
    global chords
    song = {}
    construction = ['INTRO', 'COU', 'REF','COU','REF','PONT','REF']
    chords = []
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def version ():
    """-0 Arguments - Give the version"""
    await bot.say("Version 0.2")

@bot.command()
async def newsong (myTon : int, myTempo : int, tierce : bool):
    """-3 Arguments : (int)Tone (int)Tempo (Bool)Chord mode - set the settings"""
    global ton
    global sleeptime
    global isTierce
    global song
    ton=myTon
    sleeptime=60.0/myTempo
    isTierce=tierce
    await bot.say("tempo : " + str(60.0/sleeptime))
    await bot.say("tone : " + str(ton))
    await bot.say("Chord mode (is tierce) : " + str(isTierce))

@bot.command()
async def playall ():
    """-0 Arguments - Play all the song"""
    global song
    global player
    global construction
    global midiCounter
    global midifile
    mf = MIDIFile(1)
    midiCounter = 0
    await bot.say("player ready")
    for part in construction:
        await bot.say(str(part) + "...")
        if part in song:
            playChordList(song[part],isTierce,mf)
    midifile = mf
    path = os.path.abspath("output.mid")
    with open("output.mid", 'wb') as outf:
        mf.writeFile(outf)
	#fs = FluidSynth()
    #with open(path, 'rb+') as inf:    
    #    with open("output.wav", 'wb+') as wavf: 
    #        fs.midi_to_audio(inf, wavf)
    
    #path = str(os.getcwd()) + str(os.sep)
    #pathMidi = path + "output.mid"
    #pathWav = path + "out.wav"
    
    #await bot.say("midi Path : " + pathMidi)
    #await bot.say("wav path : " + pathWav)
    
    #fs = FluidSynth()
    #fs.midi_to_audio(pathMidi, pathWav)
    
    await bot.say("song played")

@bot.command()
async def chords(s):
    """-1 Argument : (string)Chords [format : c1/t1-c2/t2 - The c are the chord progression, t are they length ]- Play all the song"""
    global chords
    chords=[]
    group = s.split('-')
    for ch in group:
        a=ch.split('/')
        chords.append([int(a[0]),int(a[1])])
    await bot.say("Chords loaded :" + str(chords))

@bot.command()
async def savechords(s):
    """-1 Argument : (string)Part must be REF, COU, PREREF, PONT or INTRO - save the loaded chords in the part"""
    global song
    global chords
    
    if(s=="REF" or s=="COU" or s=="PREREF" or s=="PONT" or s=="INTRO"):
        song[s] = chords
        await bot.say("Chords : " + str(song))
    else:
        await bot.say("Arguments not aviable, must be REF, COU, PREREF, PONT or INTRO")

@bot.command()
async def clearall():
    """-0 Arguments : clear the chords and the song"""
    global chords
    global  song
    chords = []
    song = {}

@bot.command()
async def clearpart(s):
    """-1 Argument : (string)Part must be REF, COU, PREREF, PONT of INTRO - : clear the chords and the part"""
    global  song
    if (s == "REF" or s == "COU" or s == "PREREF" or s == "PONT" or s == "INTRO"):
        song[s] = []
        await bot.say(song)
    else:
        await bot.say("Arguments not aviable, must be REF, COU, PREREF, PONT or INTRO")

@bot.command()
async def savesong(s):
    """-1 Argument : (string)SongName - Save the song on files with the songname"""
    global song
    global construction
    global sleeptime
    global ton
    global isTierce
    global midifile
    a = [ton, sleeptime, isTierce]
    if not os.path.exists(str(s)):
        os.makedirs(str(s))
    json.dump(song, open(str(s) + "/" + str(s)+".txt", 'w'))
    json.dump(construction, open(str(s) + "/" + str(s)+"__construc.txt", 'w'))
    json.dump(a, open(str(s) + "/" + str(s)+"__datas.txt", 'w'))
    with open(str(s) + "/" + str(s)+".mid", 'wb') as outf:
        midifile.writeFile(outf)
    #fs = FluidSynth()
    #fs.midi_to_audio(str(s) + "/" + str(s)+".mid", str(s) + "/" + str(s)+".wav")

@bot.command()
async def opensong(s):
    """-1 Argument : (string)SongName - Open the song on files with the songname"""
    global song
    global construction
    global sleeptime
    global ton
    global isTierce
    if not os.path.exists(str(s)):
        await bot.say("Song not found")
    else:
        song = json.load(open(str(s) + "/" + str(s)+".txt"))
        construction = json.load(open(str(s) + "/" + str(s)+"__construc.txt"))
        a = json.load(open(str(s) + "/" + str(s)+"__datas.txt"))
        ton = a[0]
        sleeptime = a[1]
        isTierce = a[2]
        await bot.say("name of the song : " + str(s))
        await bot.say("tempo : " + str(60.0/sleeptime))
        await bot.say("tone : " + str(ton))
        await bot.say("Chord mode (is tierce) : " + str(isTierce))
        await bot.say("Song construction : " + str(construction))
        await bot.say("Chords : " + str(song))
    
@bot.command()
async def construction():
    """-0 Arguments - Bot say the construction"""
    global construction
    await bot.say("Song construction : " + str(construction))

@bot.command()
async def setconstruction(s):
    """-1 Argument : (string)PARTS [format : PART1-PART2-PART3 the parts must be REF, COU, PREREF, PONT or INTRO] - Set the construction"""
    global construction
    construction=[]
    group = s.split('-')
    for part in group:
        construction.append(str(part))
    await bot.say("Song construction : " + str(construction))

@bot.command()
async def song():
    """-0 Arguments - Bot say all the song informations"""
    global song
    global construction
    global sleeptime
    global ton
    global isTierce
    await bot.say("tempo : " + str(60.0/sleeptime))
    await bot.say("tone : " + str(ton))
    await bot.say("Chord mode (is tierce) : " + str(isTierce))
    await bot.say("Song construction : " + str(construction))
    await bot.say("Chords : " + str(song))

@bot.command()
async def getSong():
    await bot.say("Chords : ")
    
def acc15(progression,length,mf):
    notes = []
    if(progression == 1):
        notes.append(ton)
        notes.append(ton - 12)
    elif(progression == 2):
        notes.append(ton + 2)
        notes.append(ton - 10)
    elif(progression == 3):
        notes.append(ton - 8)
        notes.append(ton + 4)
    elif(progression == 4):
        notes.append(ton - 7)
        notes.append(ton + 5)
    elif(progression == 5):
        notes.append(ton - 5)
        notes.append(ton + 7)
    elif(progression == 6):
        notes.append(ton - 3)
        notes.append(ton + 9)
    notes.append(ton+12)
    notes.append(ton+7)
    playChord(notes,length)
    print("acc15")
    
def acc3(progression,length,mf):
    global midiCounter
    notes = []
    if(progression == 1):
        notes.append(ton)
        notes.append(ton + 16)
    elif(progression == 2):
        notes.append(ton + 2)
        notes.append(ton + 17)
    elif(progression == 3):
        notes.append(ton - 8)
        notes.append(ton + 7)
    elif(progression == 4):
        notes.append(ton - 7)
        notes.append(ton + 9)
    elif(progression == 5):
        notes.append(ton - 5)
        notes.append(ton + 11)
    elif(progression == 6):
        notes.append(ton - 3)
        notes.append(ton + 12)
            
    playChord(notes,length,mf)
    midiCounter += length
    print("acc3")
    
def playChord(notes,length,mf):
    #player.set_instrument(instrCHRDS)
    global sleeptime
    global midiCounter
    for note in notes:
        player.note_on(note, 100)
        mf.addNote(0, 0, note, midiCounter, length, 100)
        
        
    time.sleep(sleeptime * length)
    
    for note in notes:
        player.note_off(note, 100)
    print("playChord")
    
def playChordList(chords, is3,mf):
    for chord in chords:
        if(is3 == True):
            acc3(chord[0],chord[1],mf)
        else:
            acc15(chord[0],chord[1],mf)

bot.run(TOKEN)
