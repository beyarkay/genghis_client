# Genghis Competitive Bot System - Client
## A bot-battling game system for coders
Genghis is a framework that allows bots built by Computer Science 
students compete for resources, trade, and fight each other across 
multiple different battlegrounds.

## Get started - Make Your Own Bot
To get started, you will need to copy some code from this GitHub repository into an 
internet-connected sever (like UCT's nightmare server that all second-year students 
have access to).

1. `ssh` into the UCT server:

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
7. and what you want your (one word) username to be:

    ```Username: <CHOOSE A USERNAME>```
    
    
All done! Your bot will be included in the next game. Email KNXBOY001 at myuct dot ac dot za 
with questions.

## Actually coding your bot

Once you've downloaded the git repository (see the steps above) then you'll
have a ```genghis_client``` directory, with some files inside:
* ```get_started.py``` - This script will register you with a genghis server, so that
you can fight against the other bots on that server (you've already done this)
* ```config.json``` - Tells the server where to find your bot script (and other things)
* ```template_bot.py``` - This is where you code your bot!
* ```template_battleground.py``` - You can also customise a battleground, which defines
the terrain that your bot will fight on.

So, to code your bot you need to edit the ```template_bot.py``` file. The
Genghis server will run your bot (and others) over and over again, providing
you with information about the game (like the battlegrounds available, where
the other bots are, where the coins are, etc). 

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
 For now, just walk in a random direction, either left `'l'`, right
 `'r'`, up `'u'` or down `'d'`.

Finally, actually write our move to a json file 
(setting indent=2 gives it nice formatting):

```python
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

Now save the code to a file called `hello_genghis.py` in the 
`genghis_client` directory. That's your bot done! Except the server
doesn't know that the script exists yet. To fix this, we need to 
edit `config.json`.

We want to add the path to `hello_genghis.py` inside 
`config.json` so that the server can read `config.json`, and then find
our script. To do this, open `config.json` and change 
```
...
  "bots": [
    {
      "path": "template_bot.py",
      "name": "template bot"
    }
  ],
...
```
to look like
```
...
  "bots": [
    {
      "path": "template_bot.py",
      "name": "template bot"
    }, {
      "path": "hello_genghis.py",
      "name": "my first bot"
    }
  ],
...
```
So now the full `config.json` file looks something like this (yours might 
look slightly different):
```
{
  "bots": [
    {
      "path": "template_bot.py",
      "name": "template bot"
    }, {
      "path": "hello_genghis.py",
      "name": "my first bot"
    }
  ],
  "battlegrounds": [
    {
      "path": "template_battleground.txt",
      "name": "template battleground"
    }
  ],
  "username": "<MY USERNAME>",
  "abbreviations": [
    "a"
  ],
  "url": "https://people.cs.uct.ac.za/~<MY STUDENT NUMBER>/genghis_client",
  "server_url": "https://people.cs.uct.ac.za/~KNXBOY001/genghis_server/"
}
```
That's it! go to [https://people.cs.uct.ac.za/~KNXBOY001/genghis_server/](https://people.cs.uct.ac.za/~KNXBOY001/genghis_server/)
to watch your bot in the next battle.

However, your bot isn't very smart. To get it doing something fancier, 
we need to learn about our options for what to put in `move.json`:

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
 
## A slightly improved `hello_genghis.py`

With our newfound knowledge, we can update `hello_genghis.py` to either
make a random move, or a random attack, or randomly drop a coin:

```python
import json
import random
with open('move.json',  'w+') as json_file:
    my_move_dictionary = {
        "action": random.choice(['walk', 'attack', 'drop']),        
        "direction": random.choice(['l', 'r', 'u', 'd', 'lu', 'ru', 'ld', 'rd'])    
        # 'type' will be ignored if action != 'drop'
        "type": random.choice([chr(i) for i in range(ord('a'), ord('z') + 1)])    
    }
    json.dump(my_move_dictionary, json_file, indent=2)
```

This is all well and good, but our bot still isn't *smart*. For this, we need to
know about our surroundings, like where the other bots / coins / ports are, and
how to get to them:

## Figuring out your move




