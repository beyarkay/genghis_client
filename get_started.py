import os
import requests
import sys
DEBUG = True

# Update the directory permissions

if len(sys.argv) > 1:
    server_url = sys.argv[1]
    username = sys.argv[2]
else:
    # Choose a server
    server_url = input("Server URL: ")
    # Choose a username
    username = input("Your username: ")

while True:
    # Check that the username isn't already taken
    username_taken = False
    if DEBUG: print("POST to {}".format(server_url + "/check_username.php"))
    r = requests.post(
        server_url + "/check_username.php",
        json={'username': username}
    )
    if DEBUG: print(r.url)
    if DEBUG: print(r.status_code)
    if DEBUG: print(r.text)
    if DEBUG: print(r.json())
    if not username_taken:
        break
    print("That username has already been taken, please choose another.")
    username = input("Your username: ")
abbreviations = [str(c).lower() for c in username if c.isalpha()][0:1]
print("The server will use these letters: \n{} \nas "
      "a 1-letter abbreviation in order to represent you."
      .format( abbreviations))
# Register the client with the server.
json = {"username":username, "abbreviations": abbreviations}
print("POST to {} with '{}'".format(server_url, json))
r = requests.post(server_url, json=json)
if r.ok:
    print('Done\nGo to {} to see the current battle'.format(server_url))
else:
    print('Error\nError posting to network. Status code=' + str(r.status_code))
# Update the config.json file

# Provide feedback that the registration was successful
