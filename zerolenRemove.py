#!/usr/bin/python

import sys
import glob

fastqFiles = glob.glob('*.fastq')

for fastqFile in fastqFiles:
	

	fastqLines = []
	headName = fastqFile.split('.')[0]
	fastqFileOut = open(headName + '.zerolen.fastq','w')
	
	with open(fastqFile,'r') as fastqIn:
		for line in fastqIn:
			fastqLines.append(line)
			
	entryLineNumber = 0
	zeroLengthSeqs = 0
	
	for line in range(len(fastqLines)):
		if entryLineNumber == 1:
			if len(fastqLines[line]) > 5:
				fastqFileOut.write(fastqLines[line - 1])
				fastqFileOut.write(fastqLines[line])
				fastqFileOut.write(fastqLines[line + 1])
				fastqFileOut.write(fastqLines[line + 2])
			else:
				zeroLengthSeqs += 1
			
			entryLineNumber += 1
		elif entryLineNumber == 3:
			entryLineNumber = 0
		else:
			entryLineNumber += 1  
	print(str(zeroLengthSeqs) + " zero length sequences removed in output",file=sys.stderr)
			