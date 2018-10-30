# This actually runs the thing. 
# - a separate file named "channellist.csv" must be in the same folder. It needs to have a list of channel names in the first column, one per row.
# - It uses stuff from Socketv2 to actually join the IRC chats of the channels to be scraped
# - It uses stuff from Readv3 to parse the text it gets from Twitch.
# - It uses stuff from Settingsv2 for various inputs.
# - It outputs the result to a set of csvs named all1.csv, all2.csv, etc up to the number set in ROUNDS

# - The columns in the final output .csv will be as follows:
# - Column 0: an ID number, literally the number of the line pulled from the buffer in the socket connection you've made (but basically just an ID number)
# - Column 1: Twitch's internal unique ID for the message. I'm not sure there's much of a point in scraping this, but here you go.
# - Column 2: Name of the channel where the message was sent
# - Column 3: Name of the user who sent the message
# - Column 4: The time when the message was sent
# - Column 5: The message's text. Usually it does pretty well with special characters, but some of the more obscure copypasta symbols turn out weird.
# - Column 6: 1 if the message was sent by the channel's owner (e.g., the streamer), 0 if not
# - Column 7: 1 if the message was sent by a mod in this channel, 0 if not
# - Column 8: 1 if the message was sent by a sub in this channel, 0 if not
# - Column 9: 1 if the message was sent by a user with Turbo (and I believe Prime, but I'm not positive on this), 0 if not
# - Column 10: If the user who sent the message is a sub in this channel, their badge number of months (e.g., 1 month, 3 months, 6 months, 12 months...)
# - Column 11: If the user who sent the message has given enough bits in this channel for a badge, the number on that badge
# - Column 12: 1 if the message was sent by a user who is a partnered streamer (I'm not positive whether this shows up only if they've chosen to have that badge visible or not), 0 if not
# - Column 13: 1 if the message was sent by a user who is a global mod, 0 if not
# - Column 14: 1 if the message was sent by a user who is an admin, 0 if not
# - Column 15: 1 if the message was sent by a user who is staff, 0 if not
# - Column 16: 1 if r9k mode was on in the channel where this message was sent when it was sent, 0 if not
# - Column 17: If slow mode was on in the channel where this message was sent when it was sent, this will show the number of seconds slow mode was set to
# - Column 18: 1 if subscribers-only mode was on in the channel where this message was sent when it was sent, 0 if not
# - Column 19: -1 if, when this message was sent, you didn't have to be a follower of the channel to post a message; 0 if you had to be a follower, but not for any specific length of time; if greater than 0, you had to have been a follower for this much time to send a message to the channel
# - Column 20: 1 if emote-only mode was on in the channel where this message was sent when it was sent, 0 if not



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
						# ab.writerow(data);
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
					if "slow" in line:
						slowmode = getslowmode(line)
						slowsettings[channelname] = slowmode
					if "subs-only" in line:
						submode = getsubmode(line)
						subsettings[channelname] = submode
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
