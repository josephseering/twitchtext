# This actually runs the thing. 
# - a separate file named "engsample.csv" must be in the same folder. It needs to have a list of channel names in the first column, one per row.
# - It uses stuff from Socketv2 to actually join the IRC chats of the channels to be scraped
# - It uses stuff from Readv3 to parse the text it gets from Twitch.
# - It uses stuff from Settingsv2 for various inputs.
# - It outputs the result to a set of csvs named all1.csv, all2.csv, etc up to the number set in ROUNDS


import string
import csv
import time
import operator
from Readv3 import getUser, getMessage, getChannelname, getBannedUser, getBannedChannelname
from Readv3 import getslowmode, getr9k, getsubmode, getroomstatechannelname
from Readv3 import getOwner, getTurbo, getSub, getMod
from Socketv2 import openSocket, sendMessage, closeSocket
#from Initializev2 import joinRoom #I'm pretty sure this doesn't do anything
from Settingsv2 import ROUNDS, ROUNDLENGTH #, CHANNELLIST, HOST, PORT, PASS, IDENT
#from getchannellist import getbucketdict
from datetime import datetime
from sorter import sortbyUsername
from banfinder import MarkBannedMessages

# Actually joins the rooms
s = openSocket()
### joinRoom(s)
readbuffer = ""

r9ksettings = {}
slowsettings = {}
subsettings = {}
#bucketsizes = {}

#bucketsizes = getbucketdict()

# Opens the output file (all.csv) and writes the headers
#with open('all.csv', 'ab') as fp:
#	ab = csv.writer(fp, delimiter=',');
#	data = ["id", "channelname", "username", "timestamp", "comment","owner","mod","sub","turbo","r9k","slow","subs","channelbucket"];
#	ab.writerow(data);

# Starts the post counter
id = 0

# Starts the cycle counter
i = 0

countdown = time.time()

# ROUNDS is the number of times it scrapes for the number of seconds specified below. I do this in a loop rather than all at once to keep files manageable sizes.
while i < (ROUNDS + 1):

	print i

	# Sets how long the scraper will run for (in seconds) per ROUND. Adds a number of seconds to the current time.
	stoptime = time.time() + ROUNDLENGTH

	# Runs until time is up
	while time.time() < stoptime:
		
		# Pulls a chunk off the buffer, puts it in "temp"
		readbuffer = readbuffer + s.recv(1024)
		temp = string.split(readbuffer, "\n")
		readbuffer = temp.pop()
	
		# Iterates through the chunk
		for line in temp:
			id = id + 1
			print line
		
			# Parses lines and writes them to the file
			if "PRIVMSG" in line:
				try:

					# Gets user, message, channel, etc from a line
					user = getUser(line)
					message = getMessage(line)
					channelname = getChannelname(line)
					owner = getOwner(line)
					mod = getMod(line)
					sub = getSub(line)
					turbo = getTurbo(line)
					
					# Though not specified in the data this way, we treat all channel owners as mods
					if owner == 1:
						mod = 1
		
					# Writes Message ID, channel, user, date/time, and cleaned message to file. Notes 1 if user is owner/mod/sub/turbo or 0 if not. 
					# Notes 1 if r9k mode or sub mode is enabled, 0 if not. Notes number of seconds of slow mode (0 if off)
					with open('all' + str(i) + '.csv', 'ab') as fp:
						ab = csv.writer(fp, delimiter=',');
						data = [id, channelname, user, datetime.now(), message.strip(), owner, mod, sub, turbo, r9ksettings[channelname], slowsettings[channelname], subsettings[channelname]];
						ab.writerow(data);
						print "Wrote " + str(id)
						countdown = time.time()
						
		
				# Survives if there's a message problem
				except Exception as e:
					print "MESSAGE PROBLEM"
					print line
					print e
		
			# Responds to PINGs from twitch so it doesn't get disconnected
			elif "PING" in line:
				try:
					separate = line.split(":", 2)
					s.send("PONG %s\r\n" % separate[1])
					print "I PONGED BACK " + str(time.time()) + "."
				
				# Survives if there's a ping problem
				except:
					print "PING problem PING problem PING problem"
					print line
		
			# Parses ban messages and writes them to the file
			elif "CLEARCHAT" in line:
				try:
			
					# Gets banned user's name and channel name from a line
					user = getBannedUser(line)
					channelname = getBannedChannelname(line)
				
					# Writes Message ID, channel, user, date/time, and an indicator that it was a ban message.
					#	I use "oghma.ban" because the bot's name is oghma, and I figure it's not a phrase that's
					#	likely to show up in a message so it's easy to search for.
					#	The various zeroes at the end are just fillers here because this row will get removed later.
					with open('all' + str(i) + '.csv', 'ab') as fp:
						ab = csv.writer(fp, delimiter=',');
						data = [id, channelname, user, datetime.now(), "oghma.ban", 0, 0, 0, 0, 0, 0, 0];
						ab.writerow(data);
						print "Wrote " + str(id)
				# Survives if there's a ban message problem
				except Exception as e:
					print "BAN PROBLEM"
					print line
					print e
			
			# This section notices if there's a change in chat mode status
			elif "ROOMSTATE" in line:
				try:
					channelname = getroomstatechannelname(line)
			
					if "r9k" in line:
						r9kmode = getr9k(line)
						r9ksettings[channelname] = r9kmode
						#print r9ksettings[channelname]
					if "slow" in line:
						slowmode = getslowmode(line)
						slowsettings[channelname] = slowmode
						#print slowsettings[channelname]
					if "subs-only" in line:
						submode = getsubmode(line)
						subsettings[channelname] = submode
						#print subsettings[channelname]
			
				# Survives if there's a chat mode problem
				except Exception as e:
					print "MODE PROBLEM"
					print line
					print e
				
		# gonna be honest, I totally forget what this does
		if countdown + 60 < time.time():
			closeSocket(s)
			print "closed"
			s = openSocket()
			print "opened"
			countdown = time.time()
					
	i = i + 1

# Creates the "sortedall" csv files, which are the all.csv sorted by username (for the purpose of finding banned messages)
sortbyUsername()

# Creates the all3.csv file, which is all2.csv with a notation if a message was banned.
MarkBannedMessages()