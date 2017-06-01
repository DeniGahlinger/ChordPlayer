# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
#import mido

#msg = mido.Message('note_on', note=80)
#msg.note
#msg.bytes()
#msg.copy(channel=2)
#msg.time = 1000
#msg.channel = 1
#print(msg)
#port = mido.set_backend('mido.backends.pygame')
#port = mido.set_backend('mido.backends.rtmidi')
#outport = mido.open_output(port)
#outport.send(msg)
#outport.close()

#winsound.Beep(440, 200)

#for i in range(10):
#    winsound.Beep(448, 200)
#import pygame
#import pygame.midi
#import time

import pygame.midi
import time
#import discord

from discord.ext.commands import Bot
my_bot = Bot(command_prefix="!")

@my_bot.event
async def on_read():
    print("Client logged in")
    
@my_bot.command()
async def hello(*args):
    return await my_bot.say("Hello, world!")
my_bot.run("{bot token}")

pygame.midi.init()
global player
player = pygame.midi.Output(0)
player.set_instrument(127)
#player.note_on(64, 127)
#player.note_on(67, 67)
#time.sleep(1)
#player.note_off(64, 127)
#player.note_off(67, 67)

#player.note_on(65, 127)
#player.note_on(69, 67)
#time.sleep(1)
#player.note_off(64, 127)
#player.note_off(69, 67)


def acc15(progression,length):
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
    
def acc3(progression,length):
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
            
    playChord(notes,length)
    print("acc3")
    
def playChord(notes,length):
    player.set_instrument(instrCHRDS)
    for note in notes:
        player.note_on(note, 100)
        
        
    time.sleep(sleeptime * length)
    
    for note in notes:
        player.note_off(note, 100)
    print("playChord")

global ton
ton = 64
global chrd
chrd = 1
global instrPERC
instrPERC = 5
global instrCHRDS
instrCHRDS = 0
tempo=120
global sleeptime
sleeptime=60.0/tempo

acc15(6,2)
acc15(4,2)
acc15(1,2)
acc15(5,2)

acc3(2,2)
acc3(1,6)
acc3(6,2)
acc3(5,6)
acc3(3,2)
acc3(4,6)
acc3(3,2)
acc3(6,6)

del player
#pygame.midi.quit()

        
    