#!/usr/bin/python

import sys
sys.path.append('/usr/lib')
from ReadFasta import ReadFasta
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("-file1", metavar="FASTA",help="Specify a query fasta file", type=str,required = True)
parser.add_argument("-file2", metavar="FASTA",help="Specify a subject fasta file", type=str,required = True)
parser.add_argument("-w", metavar="word size",help="Specify a min word size", type=int,default = 6)
args = parser.parse_args()

readerQuery = ReadFasta(args.file1)
collectionQuery = readerQuery.openFasta()

readerSubject = ReadFasta(args.file2)
collectionSubject = readerSubject.openFasta()

def populateTable(seqA,seqB):
	table = []
	lengthA = len(seqA)
	lengthB = len(seqB)
	
	#print(lengthB,lengthA,sep='\t')
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
			#print(seqB[iterator], aIndex, seqA[aIndex],sep = '  ')
			#print(seqA[aIndex])
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
					if diagStep + iterator <= len(table): #and diagStep + iterator <= len(xPos):
						#print(str(diagStep + iterator),end=',')
						if table[iterator + diagStep][yValue - diagStep] == 'X':
							diagScore += 1
						else:
							break
			if diagScore >= args.w:
				# +1 transform to x,y from list indices
				#print(diagScore,iterator + 1,yValue + 1,sep='\t')
				coordinate = [diagScore,iterator,yValue]
				coordsList.append(coordinate)
		iterator += 1	
		
	return coordsList
		
def findSeqOverlap(coordsList,seqA,seqB,name,subjectName):
	#[7,5,10] SCORE,B,A
	for coord in coordsList:
		print("Top Sequence (5'-3'): ",name[1:])
		print("Bottom Sequence (3'-5' RC): ",subjectName[1:]," ",coord)
		#push B onto A
		if coord[2] >= coord[1]:
			difference = coord[2] - coord[1]
			
			seqAindex = len(seqA) - coord[1] - 1 - coord[2]
			difference = seqAindex
			
			if difference > 0:
				print(seqA)
				for space in range(difference): #prepending matchLine spaces
					print(" ",end='')
				#print()
				
				seqBindex = 0
				for matchLinesPos in range(difference,len(seqA)):
					if seqBindex < len(seqB):
						if seqA[matchLinesPos] == seqB[seqBindex]:
							print('|',end='')
						else:
							print(' ',end='')
						seqBindex += 1
				
				print()
				for space in range(difference):
					print(" ",end='')
				print(seqB)
				print()
			#cant push b onto a, move a onto b
			else:
				difference = abs(seqAindex)
				for space in range(difference):
					print(" ",end='')
				overlapA = len(seqB) - difference
				print(seqA)
				for space in range(difference):
					print(" ",end='')
				for overlapBase in range(overlapA):
					if overlapBase < len(seqA):
						if seqA[overlapBase] == seqB[difference + overlapBase]:
							print("|",end='')
						else:
							print(" ",end="")
				print()
				print(seqB)
				print()
		if coord[1] > coord[2]:
			seqAindex = len(seqA) - coord[2] - 1 # 14
			seqBindex = coord[1] + 1 # 27   = 6 spaces
			diff = (seqBindex - seqAindex)
			#push a onto b
			if diff > 0:
				for space in range(diff - 1):
					print(" ",end='')
				print(seqA)
				for space in range(diff - 1):
					print(" ",end='')
				overlapA = len(seqB) - diff
				for overlapBase in range(overlapA + 1):
					if overlapBase < len(seqA):
						bIndex = diff + overlapBase - 1
						if bIndex < len(seqB):
							#print(bIndex,end=',')
							if seqA[overlapBase] == seqB[bIndex]:
								print("|",end='')
							else:
								print(" ",end="")
				
				
				print()
				print(seqB)
				print()
			#push b onto a
			else:
				difference = abs(diff) + 1
				print("Alignment suspect")
				print(seqA)
				overlap = len(seqA) - difference
				for space in range(difference):
					print(" ",end='')
				#print("overlap: ",overlap)
				for overlapBase in range(overlap):
					if overlapBase < len(seqB):
						aIndex = difference + overlapBase 
						#print(aIndex,end=',')
						if seqA[aIndex] == seqB[overlapBase]:
							print("|",end='')
						else:
							print(" ",end='')
					
				print()
				for space in range(difference):
					print(" ",end='')
				print(seqB)
				print()
		
	
	
	
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
		#print(name," vs. ",subjectName)
		rev = reverseComplement(collectionSubject[subjectName])
		filledTable = populateTable(collectionQuery[name],rev)
		#printTable(filledTable)
		result = walkTable(filledTable)
		
		findSeqOverlap(result,collectionQuery[name],rev,name,subjectName)
		#printTable(filledTable)
		