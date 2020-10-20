import os
import requests
import sys

# Update the directory permissions

# Choose a server
server_url = input("Server URL: ")
# Choose a username
while True:
    username = input("Your username: ")
    # Check that the username isn't already taken
    username_taken = False
    if not username_taken:
        break
    print("That username has already been taken, please choose another.")

print("The server will use these letters: \n{} \nas "
      "a 1-letter abbreviation in order to represent you."
      .format(', '.join([str(c).lower() for c in username if c.isalpha()])))
# Register the client with the server.
r = requests.post(server_url, json={})
if r.ok:
    print('Done\nGo to {} to see the current battle'.format(server_url))
else:
    print('Error\nError posting to network. Status code=' + str(r.status_code))
# Update the config.json file

# Provide feedback that the registration was successful



d = os.path.dirname(os.path.abspath(__file__))
darr = d.split('/')[-3:]
darr.remove('public_html')
root_url = 'https://people.cs.uct.ac.za/~' + '/'.join(darr)
os.chmod(os.path.join(d, 'bot.py'), 0o755)
os.chmod(os.path.join(d, 'template_battleground.txt'), 0o755)
print('Attempting to add bot at \n\t{}\nto network at\n\t{}'.format(root_url, sys.argv[1]))
r = requests.post(sys.argv[1], json={'root': root_url})
if r.ok:
    print('Done\nGo to https://people.cs.uct.ac.za/~KNXBOY001/gm/ to see the current battle')
else:
    print('Error\nError posting to network. Status code=' + str(r.status_code))
