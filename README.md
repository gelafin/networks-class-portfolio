# Super LAN Multiplayer Rock-Paper-Scissors
## How to Play
This game has the same rules as rock-paper-scissors, except your uses of each move are limited. You get more uses when you start to run out. The game only ends when either player quits.

### Requires Python
1. Install Python (version >= 3.8) if you don't have it

### (optional) Enable multiplayer with another computer on your network
1. Find your **local** IP address (don't just search "what's my IP" and use that--that's likely your router's IP address, not yours)
   1. If this is hard, search "how to find local ip address"
   2. On Windows, run the terminal command ipconfig and get your computer's IPv4 address for the network you're using
2. Open socket_constants.py in any text editor, and change `SERVER_NAME` to your IPv4 address
3. Get a copy of all the repo files on any other computer connected to the same network
   1. Fun fact: you don't need to copy both of the client/server files!
   2. Make sure the `SERVER_NAME` in socket_constants.py on this computer has the same IPv4 address; don't change it

### Start Playing
1. Whoever wants to be Player 2
   1. Open a terminal and run `python http_server.py`
2. Whoever wants to be Player 1
   1. If you followed the steps above to play with another computer on your network, have the other computer run `python http_client.py`
   2. If you didn't follow the above steps, open a second terminal and run `python http_client.py`
3. You're playing
