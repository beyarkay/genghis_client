import os
import requests
import sys
import json

DEBUG = True
CONFIG_FILE = 'config.json'

# Update the directory permissions

if len(sys.argv) > 1:
    server_url = sys.argv[1]
    client_url = sys.argv[2]
    username = sys.argv[3]
else:
    # Choose a server
    server_url = input("Server URL: ")
    # Give your URL
    client_url = input("Client URL: ")
    # Choose a username
    username = input("Your username: ")

while True:
    abbreviations = [str(c).lower() for c in username if c.isalpha()][0:1]
    # Register the client with the server.
    new_client = {
        "username": username,
        "abbreviations": abbreviations,
        "url": client_url,
    }
    r = requests.post(server_url + "/register_client.php", json=new_client )
    if DEBUG: print(r.text)
    return_data = r.json()
    if return_data['status'] == 'good':
        # Update the config.json file
        with open(CONFIG_FILE, 'r') as config_file:
            config = json.load(config_file)
        config['username'] = username
        config['abbreviations'] = abbreviations
        config['url'] = client_url
        config['server_url'] = server_url
        with open(CONFIG_FILE, 'w+') as config_file:
            json.dump(config, config_file, indent=2)
        
        if DEBUG: print("Config file updated: " + str(config))

        print("All Complete.\nGo to {} to see the server".format(server_url))
        break
    elif return_data['cause'] == 'username':
        print("That username has already been taken, please choose another.")
        username = input("Choose a username: ")
        continue
    else:
        print("Error occured during client registration: {}".format(return_data))
        break
