# This actually runs the thing. 
# - a separate file named "channellist.csv" must be in the same folder. It needs to have a list of channel names in the first column, one per row.
# - It uses stuff from Socketv2 to actually join the IRC chats of the channels to be scraped
# - It uses stuff from Readv3 to parse the text it gets from Twitch.
# - It uses stuff from Settingsv2 for various inputs.
# - It outputs the result to a set of csvs named all1.csv, all2.csv, etc up to the number set in ROUNDS


import string
import csv
import time
import operator
from datetime import datetime
from Readv3 import getUser, getMessage, getChannelname, getBannedUser, getBannedChannelname, getMessageID, getBanduration, getBanreason, getBantarget, getUserID
from Readv3 import getslowmode, getr9k, getsubmode, getemoteonly, getfollowersonly, getroomstatechannelname
from Readv3 import getOwner, getTurbo, getSub, getMod, getGlobalmodbadge, getAdminbadge, getStaffbadge
from Readv3 import getSubbadge, getBitsbadge, getPartnerbadge
from Socketv2 import openSocket, sendMessage, closeSocket
from Settingsv2 import ROUNDS, ROUNDLENGTH


# Actually joins the rooms
s = openSocket()
### joinRoom(s)
readbuffer = ""

# Initializes mode settings
r9ksettings = {}
slowsettings = {}
subsettings = {}
followersonlysettings = {}
emoteonlysettings = {}

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
					messageid = getMessageID(line)
					userid = getUserID(line)
					
					subbadge = getSubbadge(line)
					bitsbadge = getBitsbadge(line)
					partnerbadge = getPartnerbadge(line)
					globalmodbadge = getGlobalmodbadge(line)
					adminbadge = getAdminbadge(line)
					staffbadge = getStaffbadge(line)
					
					
					# Though not specified in the data this way, we treat all channel owners as mods
					if owner == 1:
						mod = 1
		
					# Writes Message ID, channel, user, date/time, and cleaned message to file. Notes 1 if user is owner/mod/sub/turbo or 0 if not. 
					# Next it notes which badges the person has next to their name. They can have sub badges of 1/3/6/12/24 etc months, bit badges of various intervals, partner badge, globalmod, admin, or staff badge.
					# Notes 1 if r9k mode or sub mode is enabled, 0 if not. Notes number of seconds of slow mode (0 if off). Followersonlymode shows number of seconds, 0 if just requires followers of any duration, and -1 if off. Emoteonly is 1 if on 0 if off.
					with open('all' + str(i) + '.csv', 'ab') as fp:
						ab = csv.writer(fp, delimiter=',');
						data = [id, messageid, channelname, user, datetime.now(), message.strip(), owner, mod, sub, turbo, subbadge, bitsbadge, partnerbadge, globalmodbadge, adminbadge, staffbadge, r9ksettings[channelname], slowsettings[channelname], subsettings[channelname], followersonlysettings[channelname], emoteonlysettings[channelname]];
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
					targetid = getBantarget(line)
					banduration = getBanduration(line)
					banreason = getBanreason(line)
					# Writes Message ID, an indicator that it was a ban message, channel, user, date/time, reason for ban if any given, and duration of ban (can be "PERMANENT BAN") 
					#	I use "oghma.ban" because the bot's name is oghma, and I figure it's not a phrase that's
					#	likely to show up in a message so it's easy to search for.
					#	The various zeroes at the end are just fillers here because this message doesn't have those other properties.
					with open('all' + str(i) + '.csv', 'ab') as fp:
						ab = csv.writer(fp, delimiter=',');
						data = [id, "oghma.ban", channelname, user, datetime.now(), banreason, banduration, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
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
					if "followers-only" in line:
						followermode = getfollowersonly(line)
						followersonlysettings[channelname] = followermode
					if "emote-only" in line:
						emotemode = getemoteonly(line)
						emoteonlysettings[channelname] = emotemode
			
				# Survives if there's a chat mode problem
				except Exception as e:
					print "MODE PROBLEM"
					print line
					print e
				
		# If for some reason it's been more than 60 seconds since the last message, it closes and re-opens the socket.
		if countdown + 60 < time.time():
			closeSocket(s)
			print "closed"
			s = openSocket()
			print "opened"
			countdown = time.time()
					
	i = i + 1