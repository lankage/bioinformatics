#!/usr/bin/python

import glob

fastqFiles = glob.glob('*.zerolen.fastq')

for fastqFile in fastqFiles:
	outFile = open(fastqFile + '.appended.fastq','w')
	
	lineCount = 0
	with open(fastqFile,'r') as readFile:
		for line in readFile:
			if lineCount == 0 and line[:1] == "@":
				lineparts = line.split()
				readName = lineparts[0] + '/' + fastqFile
				outFile.write(readName + ' ' + lineparts[1] + ' ' + lineparts[2] + '\n')
				lineCount += 1
			elif lineCount == 3:
				outFile.write(line)
				lineCount = 0
			else:
				outFile.write(line)
				lineCount += 1
			
				
			
		