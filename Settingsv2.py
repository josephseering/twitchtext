# IRC Chat address
HOST = "irc.chat.twitch.tv"

#PORT = 443
PORT = 6667

### THIS NEEDS YOU TO ADD IT ###
# oauth token text for the account you're using as a bot. Get (currently) at https://twitchapps.com/tmi/. Format "oauth:ab12cd34etc"
PASS = ""

### THIS NEEDS YOU TO ADD IT ###
# the account username for whatever account you're using as a bot. Format "username"
IDENT = ""

# the scraper will create this many files. I mostly just use this because if I put all of the output into a single file it becomes to big to manage, so I separate it into multiple files. 
ROUNDS = 2

# how long it will scrape for in each file (in seconds)
ROUNDLENGTH = 28800

# With the numbers I've entered here (in ROUNDS and ROUNDLENGTH), it'll scrape into one file for 28800 seconds then create a second file and scrape into it for 28800 seconds. These obviously can be changed.
