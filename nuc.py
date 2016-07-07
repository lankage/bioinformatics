#!/usr/bin/python

#Michael Graham
#Oligo compatibility screening tool
# takes a subject and query oligo file and looks for opportunities 
# for complementarity.  Companion scripts are ReadFasta.py and OligoCompat.py

import sys
sys.path.append('/usr/lib')
from ReadFasta import ReadFasta
import argparse
import re
import os

parser = argparse.ArgumentParser()
parser.add_argument("-file1", metavar="FASTA",help="Specify a query fasta file", type=str,required = True)
parser.add_argument("-file2", metavar="FASTA",help="Specify a subject fasta file", type=str,required = True)
parser.add_argument("-w", metavar="word size",help="Specify a min word size", type=str,default = "6")
parser.add_argument("-m", metavar="minimum total matches",help="Specify a minimum total matches", type=str,default = "5")
args = parser.parse_args()

args.w = int(args.w)
args.m = int(args.m)

readerQuery = ReadFasta(args.file1)
collectionQuery = readerQuery.openFasta()

readerSubject = ReadFasta(args.file2)
collectionSubject = readerSubject.openFasta()

def populateTable(seqA,seqB):
	table = []
	lengthA = len(seqA)
	lengthB = len(seqB)
	
	for base in range(lengthB):
		if seqB[base] == seqA[-1:]:
			cell = ['X']
		else:
			cell = ['O']
		table.append(cell)

	iterator = 0
	for cell in table:
		
		for subjectPosition in range(1,lengthA):
			aIndex = len(seqA) - subjectPosition - 1
			
			if seqB[iterator] == seqA[aIndex]:
				cell.append('X')
			else:
				cell.append('O')
		iterator += 1
	
	return table
	
def walkTable(table):
	coordsList = []
	iterator = 0
	for xPos in table:
		yHeight = len(xPos) - 1
		for yValue in range(yHeight, -1, -1):
			diagScore = 0
			if xPos[yValue] == "X":
				diagScore = 1
				
				#max steps for a diagonal
				for diagStep in range(1,len(table) - iterator):
					#dont look beyond the table
					if diagStep + iterator <= len(table): 
						if table[iterator + diagStep][yValue - diagStep] == 'X':
							diagScore += 1
						else:
							break
			if diagScore >= args.w:
				
				coordinate = [diagScore,iterator,yValue]
				coordsList.append(coordinate)
		iterator += 1	
	
	return coordsList
		
def findSeqOverlap(coordsList,seqA,seqB,name,subjectName):
	#[7,5,10] SCORE,B,A
	
	tempOutput = open('temphits.txt','w')
	for coord in coordsList:
		
		tempOutput.write("Top Sequence (5'-3'): " + name[1:] + '\n')
		tempOutput.write("Bottom Sequence (3'-5' RC): " + subjectName[1:] + " " + str(coord) + '\n')
		
		#push B onto A
		if coord[2] >= coord[1]:
			difference = coord[2] - coord[1]
			
			seqAindex = len(seqA) - coord[1] - 1 - coord[2]
			difference = seqAindex
			
			if difference > 0:
				#print(seqA)
				tempOutput.write(seqA + '\n')
				
				for space in range(difference): #prepending matchLine spaces
					tempOutput.write(' ')
					
				
				seqBindex = 0
				for matchLinesPos in range(difference,len(seqA)):
					if seqBindex < len(seqB):
						if seqA[matchLinesPos] == seqB[seqBindex]:
							
							tempOutput.write('|')
						else:
							
							tempOutput.write(' ')
						seqBindex += 1
				
				
				tempOutput.write('\n')
				for space in range(difference):
					
					tempOutput.write(' ')
				
				tempOutput.write(seqB + '\n')
				
				tempOutput.write('\n')
				
			#cant push b onto a, move a onto b
			else:
				difference = abs(seqAindex)
				for space in range(difference):
					
					tempOutput.write(' ')
					
				overlapA = len(seqB) - difference
				
				tempOutput.write(seqA + '\n')
				
				for space in range(difference):
					
					tempOutput.write(' ')
					
				for overlapBase in range(overlapA):
					if overlapBase < len(seqA):
						if seqA[overlapBase] == seqB[difference + overlapBase]:
							
							tempOutput.write('|')
						else:
							
							tempOutput.write(' ')
				
				tempOutput.write('\n')
				
				tempOutput.write(seqB + '\n')
				
				tempOutput.write('\n')
				
		if coord[1] > coord[2]:
			seqAindex = len(seqA) - coord[2] - 1 
			seqBindex = coord[1] + 1 
			diff = (seqBindex - seqAindex)
			#push a onto b
			if diff > 0:
				for space in range(diff - 1):
					
					tempOutput.write(' ')
				
				tempOutput.write(seqA + '\n')
				
				for space in range(diff - 1):
					
					tempOutput.write(' ')
					
				overlapA = len(seqB) - diff
				for overlapBase in range(overlapA + 1):
					if overlapBase < len(seqA):
						bIndex = diff + overlapBase - 1
						if bIndex < len(seqB):
							
							if seqA[overlapBase] == seqB[bIndex]:
								
								tempOutput.write('|')
							else:
								
								tempOutput.write(' ')
				
				tempOutput.write('\n')
				tempOutput.write(seqB + '\n')
				tempOutput.write('\n')
				
			#push b onto a
			else:
				difference = abs(diff) + 1
				tempOutput.write(seqA + '\n')
				overlap = len(seqA) - difference
				for space in range(difference):
					
					tempOutput.write(' ')
				for overlapBase in range(overlap):
					if overlapBase < len(seqB):
						aIndex = difference + overlapBase 
						
						if seqA[aIndex] == seqB[overlapBase]:
							
							tempOutput.write('|')
						else:
							tempOutput.write(' ')
					
				tempOutput.write('\n')
				for space in range(difference):
					
					tempOutput.write(' ')
				
				tempOutput.write(seqB + '\n')
				tempOutput.write('\n')
	tempOutput.close()
		
def filterHits():
	hitLines = []
	with open('temphits.txt','r') as tempHitsFile:
		for line in tempHitsFile:
			hitLines.append(line)
			
	lineiter = 0
	for line in range(len(hitLines)):
		
		if lineiter == 3:
			matchLine = hitLines[line]
			seqTop = re.sub('\s+','',hitLines[line - 1])
			seqBot = re.sub('\s+','',hitLines[line + 1])
			matchTest = matchCharacter(seqTop,seqBot,matchLine,hitLines[line - 1],hitLines[line + 1])
			if matchTest != False:
				print(hitLines[line - 3].rstrip(),"\t{D:",matchTest[0],",","C:",matchTest[1],",","T:",matchTest[2],",","ID:",matchTest[3],"}",sep='')
				print(hitLines[line - 2],end='')
				print(hitLines[line - 1],end='')
				print(hitLines[line],end='')
				print(hitLines[line + 1],end='')
				print(hitLines[line + 2],end='')
			
			lineiter += 1
		
		elif lineiter == 5:
			lineiter = 0
		else:
			lineiter += 1
	#### Delete temp file when done
	os.remove('temphits.txt')
			
def matchCharacter(seqTop,seqBot,matchLines,seqTopSpaces,seqBotSpaces):
	
	totalMatches = matchLines.count('|')
	maxConsec = max(len(s) for s in re.findall(r'\|+',matchLines))
	consecList = list(len(s) for s in re.findall(r'\|+',matchLines))
	consString = ';'.join(str(x) for x in consecList)
	
	#find longest 3' end-end dimer overlap THE WORST
	endendConsec = 0
	for consecIter in range(4,len(seqTop)):
		if seqTop[-consecIter:] == seqBot[:consecIter]:
			endendConsec = consecIter
	#verify legit dimers, top seq alignment with spaces look for | at match line string at same position
	#true dimer should involve a 3' match with the top primer
	finalbase = len(seqTopSpaces) - 2 #-2 because newline and convert to 0 based index
	
	internalDimer = 0
	topSeqDimer = 1
	botSeqDimer = 1
	
	#find first index of botseq with non spaces
	botstart = re.search('\S', seqBotSpaces).start()
	
	if finalbase < len(matchLines) and totalMatches >= args.w:
		if matchLines[finalbase] != '|':
			endendConsec = 0
			topSeqDimer = 0
		else:
			#test last 4 bases of top seq / bot seq for match chars
			for basepos in range(0,4):
				if matchLines[finalbase - basepos] != '|':
					topSeqDimer = 0
			for baseposbot in range(0,4):
				if matchLines[botstart + baseposbot] != '|':
					botSeqDimer = 0
				
	else:
		#match lines do not extend to topseq 3' end, cannot be dimer
		endendConsec = 0
		topSeqDimer = 0
	if topSeqDimer and botSeqDimer:
		internalDimer = 1
	
	
	if maxConsec >= args.w and totalMatches >= args.m:
		#hit passed word size and match total filter
		return [endendConsec, str(maxConsec) + '|' + consString , totalMatches, internalDimer]
	else:
		return False
	
	
	
def printTable(filledTable):
	yHeight = len(filledTable[0]) - 1
	
	for yValue in range(yHeight,-1, -1):
		#print(yValue)
		for seqBposition in range(len(filledTable)):
			print(filledTable[seqBposition][yValue],end=' ')
		#print(yValue,end='')
		print()
		
def reverseComplement(sequence):
	
	revDictDNA = {"a":"t", "t":"a", "g":"c", "c":"g", "A":"T", "T":"A", "G":"C", "C":"G"}
	revDictRNA = {"g":"c", "c":"g", "a":"u", "u":"a", "G":"C", "C":"G", "A":"U", "U":"A"}
	sequenceRev = sequence[::-1]
	sequenceRevCom = ""
	match = re.search('u|U',sequenceRev)
        
	for char in sequenceRev:
		if match:
			newchar = revDictRNA[char]
			sequenceRevCom += newchar
		else:
			newchar = revDictDNA[char]
			sequenceRevCom += newchar
	
	return sequenceRevCom


for name in collectionQuery:
	for subjectName in collectionSubject:
		
		rev = reverseComplement(collectionSubject[subjectName])
		filledTable = populateTable(collectionQuery[name],rev)
		
		result = walkTable(filledTable)
		
		findSeqOverlap(result,collectionQuery[name],rev,name,subjectName)
		
		filterHits()
		
		