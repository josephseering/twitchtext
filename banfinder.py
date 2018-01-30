import csv
from Settingsv2 import ROUNDS

# This is activated in Runv3, but can be activated in finishrunv3 if runv3 ended prematurely
# Adds a column to the far right of the dataset 
# This column has a 1 if the user was banned following a given message, or a 0 otherwise
# Script works by iterating through the file in pairs of line + next line 
#	and looking for ban indicators

# This is intended to be used after data has been collected (via runv3) and sorted (via sorter)
# It requires csvs with names "sortedall" + number ".csv", which are the output of sorter.py

def MarkBannedMessages():
	i = 1
	while i < (ROUNDS + 1):
		with open('sortedall' + str(i) + '.csv','r') as csvinput:
			
			# Needs to compare row to previous row; row1 is start row, row2 is next row
			row1 = []
			row2 = [0,0,0,0,0]

			reader = csv.reader(csvinput)
			
			# Will contain output
			all = []
			
			# Iterates over each row in the previous file (all2, which is sorted by user)
			for row in reader:
				
				# Increments current row and next row
				row1 = row2
				row2 = row
				
				# If the row itself is a ban indicator, put a zero
				if row1[4] == "oghma.ban":
					row1.append(0)
				
				# If the row is a message AND the next message is a ban indicator AND
				#	the usernames are the same for both, then put a 1
				if not row1[4] == "oghma.ban":
					if row2[4] == "oghma.ban" and row1[2] == row2[2]:
						row1.append(1)
					else:
						row1.append(0)
				
				# Adds all to the output file
				all.append(row2)

			# Changes the last cell in the header row from a "0" to "banned"
			all[0][13] = "banned"
			
			# Appends a zero to the last message in the set. We don't have the next message
			#	so we can't tell if it got banned, so we assume it wasn't.
			all[len(all)-1].append(0)
				
			# Output all to all3.csv
			with open('markedall' + str(i) + '.csv', 'ab') as fp:
				writer = csv.writer(fp, lineterminator='\n')
				writer.writerows(all)
			i = i + 1