# twitchtext

Runv3 is the main file to run, the rest are various dependencies. getchannellist is used by Socketv2. All other things (including Socketv2) are used in Runv3. <br />
<br />
This bot will not run as-is. It needs to be modified to add a list of channels to scrape and doesn't have a username or password to connect to Twitch with. These are pretty easy to add, but I won't put my own here for obvious reasons (i.e., my account info and research participant privacy).

Things to do before this will work:
1. Create a Twitch account the regular way on the Twitch website
2. Add this account's username to the Settingsv2 file in the location noted
3. Get an oauth token for this account and put it in the Settingsv2 file in the location noted. Instructions for this are in the Settingsv2 file.
4. Put the names of the channels you want to scrape in the channellist.csv file
