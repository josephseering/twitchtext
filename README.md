# Twitch IRC scraping bot

#### Note: This scraper bot was created by and is maintained by Joseph Seering (me), jseering@andrew.cmu.edu. I am happy to share this code with you to help you gather data, but I'd appreciate it if you let me know who you are and roughly what you plan to do with it.

#### Also note that there are of course some privacy concerns to be considered here; in part because of Twitch's openness to third-party bot/tool developers, it's quite easy to gather a whole lot of data about what users are saying, but I would suggest that researchers should be careful not to abuse or take advantage of this access. 

#### If you do use this bot or a modified version of it, I would appreciate it if you would cite my [Shaping Pro and Anti-Social Behavior on Twitch Through Moderation and Example-Setting](https://dl.acm.org/citation.cfm?id=2998277) paper, as it was the first paper to use this bot.  

\
\
**File descriptions:**
- Runv3.py: when you've set up the scraper and you're ready to go, run this.
- Socketv2.py: Joins the channels you want to scrape.
- getchannellist.py: Called by Socketv2.py when joining, this pulls names of channels you want to scrape from the channellist.csv file
- Readv3.py: This defines a number of functions to parse the raw text sent by Twitch IRC in order to pull out useful values.
- Settingsv2.py: Stores various useful values required in other parts of the code

***This bot will not run as-is.*** It needs to be modified to add a list of channels to scrape and doesn't have a username or password to connect to Twitch with. These are pretty easy to add, but I won't put my own here for obvious reasons (i.e., my account info and research participant privacy).

**Things to do before this will work:**
1. Create a Twitch account the regular way on the Twitch website
2. Add this account's username to the Settingsv2 file in the location noted
3. Get an oauth token for this account and put it in the Settingsv2 file in the location noted. Instructions for this are in the Settingsv2 file.
4. Put the names of the channels you want to scrape in the channellist.csv file. (I've put "food", "bobross", and "twitchpresents" in there as examples.)
