#!/usr/bin/python3
"""
Date: 2020-11-15
Author: Boyd Kane: https://github.com/beyarkay
This is the bare-minimum bot for the Genghis Bot Battle System. (https://github.com/beyarkay/genghis_client)
Use this script as a starting point from which to build your own bot.
"""

import json
import pickle
import os
import sys
import random
# IMPORTANT: add the server directory to the PATH so we can import the utilities file
sys.path.append(sys.argv[1])
import util

def main():
    move_dict = {
        "action": "",
        "direction": ""
    }
    # Go through each motion type. If that motion type can't be completed, move on to the next motion type.
    # Read in the Game object from game.pickle
    with open("game.pickle", "rb") as gamefile:
        game = pickle.load(gamefile)
    # Figure out which bot in the Game object represents this script
    this_bot = None
    for game_bot in game.bots:
        if game_bot.bot_icon == sys.argv[2]:
            this_bot = game_bot
            break

    # Figure out which battleground in the Game the bot is on
    this_battleground = None
    for bg in game.battlegrounds:
        if bg.port_icon == sys.argv[3]:
            this_battleground = bg
            break
    bot_x, bot_y = this_battleground.find_icon(this_bot.bot_icon)[0]

    # TODO: YOUR BOT LOGIC GOES HERE, AND PUTS YOUR MOVE INTO THE DICTIONARY 'move_dict'

    
    with open("move.json", "w+") as movefile:
        json.dump(move_dict, movefile)



def get_dist(here, there):
   """
    A helper method to get the distance between two points
    here: a 2-element list (or tuple) containing the x,y coordinates of the first location
    there: a 2-element list (or tuple) containing the x,y coordinates of the second location
    returns: a number that is the distance between here and there
   """
   delta_x = abs(there[0] - here[0])
   delta_y = abs(there[1] - here[1])
   return max(delta_x, delta_y)

def get_direction(here, there):
   """
    A helper method to get the Genghis-compatible direction string from one point to the other
    here: a 2-element list (or tuple) containing the x,y coordinates of the first location
    there: a 2-element list (or tuple) containing the x,y coordinates of the second location
    returns: a string that can be passed to the Genghis 'move_dict' in order to walk/attack/etc
    in the direction of 'there'
    
    
   """
   delta_x = min(1, max(-1, there[0] - here[0]))
   delta_y = min(1, max(-1, there[1] - here[1]))
   move_array = [
       ['lu', 'u', 'ru'],
       ['l', '', 'r'],
       ['ld', 'd', 'rd']
   ]
   return move_array[delta_y + 1][delta_x + 1]


if __name__ == '__main__':
    main()
