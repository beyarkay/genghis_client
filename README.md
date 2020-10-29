# Genghis Competitive Bot System - Client
## A bot-battling game system for coders
Genghis is a framework that allows bots built by Computer Science 
students compete for resources, trade, and fight each other across 
multiple different battlegrounds.

## Get started - Make Your Own Bot
To get started, you will need to copy some code from a GitHub repository into an 
internet-connected sever (like UCT's nightmare server that all second-year students 
have access to).

1. ssh into the UCT server:

    ```ssh <YOUR_STUDENT_NUMBER>@nightmare.cs.uct.ac.za```
2. Make a public directory to host the bot script, and change into it:

    ```mkdir ~/public_html && cd ~/public_html```
3. Get a copy of the scripts needed to setup your bot, and then change into the newly created directory:

    ```git clone https://github.com/beyarkay/genghis_client.git && cd genghis_client```
4. Run a script to get you started (see next step about the prompts):

    ```python3 get_started.py```
5. At the prompts, enter the server's URL:

    ```https://people.cs.uct.ac.za/~KNXBOY001/genghis_server```
6. your (Client) URL:

    ```https://people.cs.uct.ac.za/~<YOUR_STUDENT_NUMBER>/genghis_client```
7. and what you want your username to be:

    ```Username: <CHOOSE A USERNAME>```
    
    
All done! Your bot will be included in the next game. Email KNXBOY001 at myuct dot ac dot za 
with questions.

## Actually coding your bot

Once you've downloaded the git repository (see the steps above) then you'll
have a ```genghis_client``` directory, with some files inside:
* ```get_started.py``` - This script will register you with a genghis server, so that
you can fight against the other bots on that server (you've already done this)
* ```config.json``` - Tells the server where to find your bot script (and other things)
* ```template_bot.py``` - This is your bot! It's not much just yet though...
* ```template_battleground.py``` - You can also customise a battleground, which defines
the terrain that your bot will fight on.
* ```and some other, less important files...```

So, to code your bot you need to edit the ```template_bot.py``` file. At a high
level, the Genghis server will run your bot (and others) once a round, providing
you with information about the game (like the battlegrounds available, where
the other bots are, etc). 

The Genghis Server expects your script to take this 
information, calculate a move, and then write that move to a file called 
```move.json```. 

Let's make a simple bot. We'll need the ```json``` python library for writing to a 
[JSON](https://www.programiz.com/python-programming/json) file, and the ```random```
python library will let us choose a direction to move at random:
```python
import json
import random
```
Next we're going to open our `move.json` file in `w+` (write) mode:
```python
with open('move.json',  'w+') as json_file:
    ...
```
Now create a python dictionary to hold our move:
```python
    my_move_dictionary = {
        "action": "walk",        
        "direction": random.choice(['l', 'r', 'u', 'd'])    
    }
```
The 'action' item specifies if you're walking, attacking, etc. 
The 'direction' item specifies in which direction you want to walk, attack, etc.
 
For now, just walk in a random direction, either left, right, up or down.

Finally, actually write our move to a json file 
(setting indent=2 gives it nice formatting):

```python
    # )
    json.dump(my_move_dictionary, json_file, indent=2)
```
And that's it! The full code is here:
```python
import json
import random
with open('move.json',  'w+') as json_file:
    my_move_dictionary = {
        "action": "walk",        
        "direction": random.choice(['l', 'r', 'u', 'd'])    
    }
    json.dump(my_move_dictionary, json_file, indent=2)
```

## Options for bot actions
### `"action": "walk"`
Causes your bot to walk into one of the 8 cells adjacent to it, 
as specified by `'direction'` which can be one of `l, r, u, d, ul, ur, dl, dr`
(order doesn't matter). 

Attempting to move into a wall (`#`) or another bot (`A` through to `Z`) 
will result in a null move (nothing happening).

Walking into a port (`1` through to `9`) will cause your bot to be 
moved through the port to the battleground on the other side of the port.
Every battleground can be reached from every other battleground, although
some routes may be faster than others.
   
Walking into a coin (`a` through to `z`) will add that coin to your
bots inventory. Coins are a measure of success, so collect them all.

### `"action": "attack"`
Causes your bot to attack one of the 8 cells adjacent to it, 
as specified by `'direction'` which can be one of `l, r, u, d, ul, ur, dl, dr`
(order doesn't matter). You can only attack other 
bots (`A` through to `Z`), attempting to attack anything else will result
in a null move (nothing happening).

When your bot makes a legal attack on a bot, the attack can either hit or miss 
(50% chance either way).

If an attack misses, nothing happens and your turn is over. If the 
attack hits, then your opponent will instantly drop one coin (chosen 
at random) onto an adjacent block to itself. 

This block must either be
another bot (such as yourself), or be an air block. If the block is a bot,
then that coin is immediately added to that bot's inventory.

### `"action": "drop"`
Causes your bot to drop a coin onto one of the 8 cells adjacent to it, 
as specified by `'direction'` which can be one of `l, r, u, d, ul, ur, dl, dr`, 
and `'type'` which defines which coin to drop, and must be one of `a` through `z`. 

You may only drop coins you have, and you may only drop onto other bots 
 (`A` through to `Z`) or onto empty air blocks `' '`. Anything else 
will result in a null move (nothing happening).

## Figuring out your move


