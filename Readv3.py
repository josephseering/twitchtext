#I'm not gonna explain how all of these work... they all just parse the messy text we get from Twitch. Trust me, they work. Ish.

# parses the name of the user contained in a line read from twitch IRC
def getUser(line):
	if "twitchnotify!twitchnotify@twitchnotify" in line:
		user = "twitchnotify"
	else:
		separate = line.split("!", 1)
		user = separate[1].split("@", 1)[0]
	return user
# parses the ID of the user contained in a line read from twitch IRC
def getUserID(line):
	if "twitchnotify!twitchnotify@twitchnotify" in line:
		userid = "0"
	else:
		separate = line.split(";user-id=",1)
		separate2 = separate[1].split(";",1)
		userid = separate2[0]
	return userid
# parses the unique message ID from a line read from twitch IRC
def getMessageID(line):
	if "twitchnotify!twitchnotify@twitchnotify" in line:
		messageid = "0"
	else:
		separate = line.split(";id=",1)
		separate2 = separate[1].split(";",1)
		messageid = separate2[0]
	return messageid
# parses the text of a message contained in a line read from twitch IRC
def getMessage(line):
	if "twitchnotify!twitchnotify@twitchnotify" in line:
		separate = line.split(":",2)
		message = separate[2].strip()
	else:
		separate = line.split("!", 1)
		message = separate[1].split(":", 1)[1]
	return message
	
# parses the name of a channel contained in a line read from twitch IRC
def getChannelname(line):
	if "twitchnotify!twitchnotify@twitchnotify" in line:
		separate = line.split(":", 2)
		channelnametemp = separate[1].split("#", 1)[1]
		channelname = channelnametemp.strip()
	else:
		separate = line.split("!", 1)
		separate2 = separate[1].split(":", 1)
		channelnametemp = separate2[0].split("#", 1)[1]
		channelname = channelnametemp.strip()
	return channelname

# parses whether a user who sends a message is a mod
def getMod(line):
	if "twitchnotify!twitchnotify@twitchnotify" in line:
		mod = 0
	else:
		separate = line.split("mod=", 1)
		separate2 = separate[1].split(";",1)
		mod = separate2[0].strip()
	return mod

# parses whether a user who sends a message is a subscriber
def getSub(line):
	if "twitchnotify!twitchnotify@twitchnotify" in line:
		sub = 0
	else:
		separate = line.split("subscriber=", 1)
		separate2 = separate[1].split(";",1)
		sub = separate2[0].strip()
	return sub

# parses whether a user who sends a message has turbo
def getTurbo(line):
	if "twitchnotify!twitchnotify@twitchnotify" in line:
		turbo = 0
	else:
		separate = line.split("turbo=", 1)
		separate2 = separate[1].split(";",1)
		turbo = separate2[0].strip()
	return turbo
	
# parses whether a user who sends a message is the channel owner
def getOwner(line):
	if "twitchnotify!twitchnotify@twitchnotify" in line:
		owner = 0
	else:
		mod = 1
		separate = line.split("room-id=", 1)
		separate2 = separate[1].split(";",1)
		roomid = separate2[0].strip()
		separate = line.split("user-id=", 1)
		separate2 = separate[1].split(";",1)
		userid = separate2[0].strip()
		if userid == roomid:
			owner = 1
		else:
			owner = 0
	return owner

# parses whether a user who sends a message has a subscriber badge, and for what month increment
def getSubbadge(line):
	if "twitchnotify!twitchnotify@twitchnotify" in line:
		subbadge = 0
	elif "subscriber/" in line:
		separate = line.split("subscriber/", 1)
		separate2 = separate[1].split(";",1)
		if "," in separate2[0]:
			subbadge = separate2[0].split(",",1)[0]
		else:
			subbadge = separate2[0]
	else:
		subbadge = 0
	return subbadge

# parses whether a user who sends a message has a bits badge and what number increment
def getBitsbadge(line):
	if "twitchnotify!twitchnotify@twitchnotify" in line:
		bitsbadge = 0
	elif "bits/" in line:
		separate = line.split("bits/", 1)
		separate2 = separate[1].split(";",1)
		if "," in separate2[0]:
			bitsbadge = separate2[0].split(",",1)[0]
		else:
			bitsbadge = separate2[0]
	else:
		bitsbadge = 0
	return bitsbadge

# parses whether a user who sends a message has a global mod badge
def getGlobalmodbadge(line):
	if "twitchnotify!twitchnotify@twitchnotify" in line:
		globalmodbadge = 0
	elif "global_mod/" in line:
		separate = line.split("global_mod/", 1)
		separate2 = separate[1].split(";",1)
		if "," in separate2[0]:
			globalmodbadge = separate2[0].split(",",1)[0]
		else:
			globalmodbadge = separate2[0]
	else:
		globalmodbadge = 0
	return globalmodbadge

# parses whether a user who sends a message has a partner badge
def getPartnerbadge(line):
	if "twitchnotify!twitchnotify@twitchnotify" in line:
		partnerbadge = 0
	elif "partner/" in line:
		separate = line.split("partner/", 1)
		separate2 = separate[1].split(";",1)
		if "," in separate2[0]:
			partnerbadge = separate2[0].split(",",1)[0]
		else:
			partnerbadge = separate2[0]
	else:
		partnerbadge = 0
	return partnerbadge

# parses whether a user who sends a message has an admin badge
def getAdminbadge(line):
	if "twitchnotify!twitchnotify@twitchnotify" in line:
		adminbadge = 0
	elif "admin/" in line:
		separate = line.split("admin/", 1)
		separate2 = separate[1].split(";",1)
		if "," in separate2[0]:
			adminbadge = separate2[0].split(",",1)[0]
		else:
			adminbadge = separate2[0]
	else:
		adminbadge = 0
	return adminbadge

# parses whether a user who sends a message has a staff badge
def getStaffbadge(line):
	if "twitchnotify!twitchnotify@twitchnotify" in line:
		staffbadge = 0
	elif "staff/" in line:
		separate = line.split("staff/", 1)
		separate2 = separate[1].split(";",1)
		if "," in separate2[0]:
			staffbadge = separate2[0].split(",",1)[0]
		else:
			staffbadge = separate2[0]
	else:
		staffbadge = 0
	return staffbadge

	
	
	
	
	
# parses the name of a channel contained in a ban indicator message
def getBannedChannelname(line):
	separate = line.split(":", 2)
	channelnametemp = separate[1].split("#", 1)[1]
	channelname = channelnametemp.strip()
	return channelname

# parses the name of a user who got banned from a ban indicator message in twitch IRC
def getBannedUser(line):
	separate = line.split(":",2)
	user = separate[2].strip()
	return user

# records the duration of a ban
def getBanduration(line):
	if "ban-duration" in line:
		separate = line.split("ban-duration=",1)
		separate2 = separate[1].split(";",1)
		banduration = separate2[0]
	else:
		banduration = "PERMANENT BAN"
	return banduration
	
# records the specified reason for a ban, if any
def getBanreason(line):
	if "ban-reason" in line:
		separate = line.split("ban-reason=",1)
		separate2 = separate[1].split(";",1)
		banreason = separate2[0]
	else:
		banreason = "NO REASON GIVEN"
	return banreason
	
# records the user id targeted for a ban
def getBantarget(line):
	separate = line.split("target-user-id=",1)
	separate2 = separate[1].split(";",1)
	bantarget = separate2[0]
	return bantarget	
	
	
	
	
	
	
# parses mode changes in emote-only
def getemoteonly(line):
	separate = line.split("emote-only=", 1)
	separate2 = separate[1].split(";", 1)
	emotemode = separate2[0].strip()
	return emotemode

# parses mode changes in followers-only
def getfollowersonly(line):
	separate = line.split("followers-only=", 1)
	separate2 = separate[1].split(";", 1)
	followermode = separate2[0].strip()
	return followermode
	
# parses mode changes in r9k
def getr9k(line):
	separate = line.split("r9k=", 1)
	separate2 = separate[1].split(";", 1)
	r9kmode = separate2[0].strip()
	return r9kmode
	
# parses mode changes in submode
def getsubmode(line):
	separate = line.split("subs-only=", 1)
	separate2 = separate[1].split(":", 1)
	submode = separate2[0].strip()
	return submode
	
# parses mode changes in slowmode
def getslowmode(line):
	separate = line.split("slow=", 1)
	separate2 = separate[1].split(";", 1)
	slowmode = separate2[0].strip()
	return slowmode

def getroomstatechannelname(line):
	channelname = line.split("#",1)[1]
	channelname = channelname.strip()
	return channelname
