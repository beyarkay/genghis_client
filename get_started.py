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
    # Check that the username isn't already taken
    if DEBUG: print(server_url + "/check_username.php")
    r = requests.post(
        server_url + "/check_username.php",
        json={'username': username}
    )
    return_data = r.json()
    if return_data['status'] == 'good':
        break
    print("That username has already been taken, please choose another.")
    username = input("Choose a username: ")

abbreviations = [str(c).lower() for c in username if c.isalpha()][0:1]

print("The server will use these letters: {} as "
      "a 1-letter abbreviation in order to represent you."
      .format(abbreviations))
# TODO ask the user if they want to change this

# Register the client with the server.
json = {
    "username": username,
    "abbreviations": abbreviations,
    "url": client_url,
}
if DEBUG: print("POST to {} with '{}'".format(server_url + "/register_client.php", json))
r = requests.post(server_url + "/register_client.php", json=json)
if DEBUG: print(r.text)
return_data = r.json()
if not return_data['status'] == 'good':
    # Update the config.json file
    with open(CONFIG_FILE, 'r') as config_file:
        config = json.load(config_file)
    config['username'] = username
    config['abbreviations'] = abbreviations
    config['url'] = client_url
    config['server_url'] = server_url
    with open(CONFIG_FILE, 'w+') as config_file:
        json.dump(config, config_file, indent=2)

    print("All Complete.\nGo to {} to see the server".format(server_url))
else:
    print("Error occured during client registration: {}".format(return_data))
