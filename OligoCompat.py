#!/usr/bin/python

# 7/6/2016
# Michael Graham
# Oligo compatibility screening tool
# takes a subject and query oligo file and looks for opportunities 
# for complementarity.  Companion scripts are ReadFasta.py and nuc.py

import re
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("-file1", metavar="FASTA",help="Specify a query fasta file", type=str,required = True)
parser.add_argument("-file2", metavar="FASTA",help="Specify a subject fasta file", type=str,required = True)
parser.add_argument("-w", metavar="word size",help="Specify a min word size", type=int,default = 6)
parser.add_argument("-m", metavar="minimum total matches",help="Specify a minimum total matches", type=int,default = 5)
args = parser.parse_args()

lines = subprocess.check_output(['python3','nuc.py','-file1',args.file1,'-file2',args.file2,'-w',str(args.w),'-m',str(args.m)]).splitlines()
decodedLines = []

for line in lines:
	decodedLines.append(line.decode("utf-8"))
	
	
def parseMatchCharacter(matchValues,seqTopLen,topPrimerName,botPrimerName):
	matchValList = matchValues.split(',')
	endendDimer = matchValList[0].split(':')[1]
	maxConsec = matchValList[1].split(':')[1].split('|')[0]
	totalMatches = matchValList[2].split(':')[1]
	internalDimer = matchValList[3].split(':')[1]
	
	warningListText = []
	
	#total matches Flag rule
	if int(totalMatches) > seqTopLen:
		totalMatchWarn = "Primer " + topPrimerName + " and Primer " + botPrimerName + " have significant complementarity"
		warningListText.append(totalMatchWarn)
	
	#end end dimer Flag rule
	if int(endendDimer) > 0:
		endendDimerWarn = "Primer " + topPrimerName + " and Primer " + botPrimerName + " form a " + endendDimer + "-base Primer-Dimer"
		warningListText.append(endendDimerWarn)
		
		
	for warn in warningListText:
		print(warn)
	
	return True
	
	
topLinesList = []

lineiter = 0
for line in range(len(decodedLines)):
	if lineiter == 3:
		matchLine = decodedLines[line]
		topLine = decodedLines[line - 3]
		topLineMatch = re.search('\{(.+)\}',decodedLines[line - 3])
		seqTop = re.sub('\s+','',decodedLines[line - 1])
		topPrimerNameMatch = re.search(r'\(5\'-3\'\):\s(\w+)',decodedLines[line - 3])
		botPrimerNameMatch = re.search(r'\(3\'-5\' RC\):\s(\w+)',decodedLines[line - 2])
		topPrimerName = topPrimerNameMatch.group(1)
		botPrimerName = botPrimerNameMatch.group(1)
		
		matchValues = topLineMatch.group(1)
		
		matchCharacterTest = parseMatchCharacter(matchValues,len(seqTop),topPrimerName,botPrimerName)
		if matchCharacterTest != False and topLine not in topLinesList:
			print(decodedLines[line - 3])
			print(decodedLines[line - 2])
			print(decodedLines[line - 1])
			print(decodedLines[line])
			print(decodedLines[line + 1])
			print(decodedLines[line + 2])
			topLinesList.append(topLine)
			
		lineiter += 1
		
	elif lineiter == 5:
		lineiter = 0
	else:
		lineiter += 1
		
		