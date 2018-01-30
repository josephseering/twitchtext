#I'm not gonna explain how all of these work... they all just parse the messy text we get from Twitch. Trust me, they work. Ish.
#Note to self - add a getPrime and getStaff.


# parses the name of the user contained in a line read from twitch IRC
def getUser(line):
	if "twitchnotify!twitchnotify@twitchnotify" in line:
		user = "twitchnotify"
	else:
		separate = line.split("!", 1)
		user = separate[1].split("@", 1)[0]
	return user

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
	
	
	
	
	
# parses mode changes in r9k
def getr9k(line):
	separate = line.split("r9k=", 1)
	separate2 = separate[1].split(":", 1)
	if "@broadcaster-lang" in line:
		separate2 = separate2[0].split(";",1)
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
	separate2 = separate[1].split(":", 1)
	if "@broadcaster-lang" in line:
		separate2 = separate2[0].split(";",1)
	slowmode = separate2[0].strip()
	return slowmode

def getroomstatechannelname(line):
	channelname = line.split("#",1)[1]
	channelname = channelname.strip()
	return channelname
