#!/usr/local/bin/python3
#reverse complement script
#11/19/2014
#Michael Graham

import argparse
import re

class ReadFasta():
	"""
	Fasta reader utility class
	"""
	
	def __init__(self,filename):
		"""
		Constructor
		"""
		self.filename = filename
		
	def openFasta(self):
		"""
		Open fasta file. Returns Dictionary object of fasta entries.
		"""
		self.fastaList = {}
		with open(self.filename) as fp:
			for name, seq in self.read_fasta(fp):
				self.fastaList[name] = seq
		return self.fastaList
		
	def read_fasta(self,fp):
		"""
		Read file line by line and separate sequences and headers
		"""
		name, seq = None, []
		for line in fp:
			line = line.rstrip()
			if line.startswith(">"):
				if name: yield (name, ''.join(seq))
				name, seq = line, []
			else:
				seq.append(line)
		if name: yield (name, ''.join(seq))


parser = argparse.ArgumentParser()
parser.add_argument("-s", help="Specify an oligo sequence", type=str)
parser.add_argument("-f", help="Specify an oligo file", type=str)
args = parser.parse_args()


revDictDNA = {"a":"t", "t":"a", "g":"c", "c":"g", "A":"T", "T":"A", "G":"C", "C":"G"}
revDictRNA = {"g":"c", "c":"g", "a":"u", "u":"a", "G":"C", "C":"G", "A":"U", "U":"A"}


if args.s:
	sequenceIn = args.s
	sequenceRev = sequenceIn[::-1]
	sequenceRevCom = ""
	match = re.search('u|U',sequenceIn)
	
	for char in sequenceRev:
		if match:
			newchar = revDictRNA[char]
			sequenceRevCom += newchar
		else:
			newchar = revDictDNA[char]
			sequenceRevCom += newchar
	print(sequenceRevCom)
	
if args.f:
	fastaReads = ReadFasta(args.f)
	collection = fastaReads.openFasta()
	
	for name in collection:
		print(name)
		sequenceIn = collection[name]
		sequenceRev = sequenceIn[::-1]
		sequenceRevCom = ""
		match = re.search('u|U',sequenceIn)
	
		for char in sequenceRev:
			if match:
				newchar = revDictRNA[char]
				sequenceRevCom += newchar
			else:
				newchar = revDictDNA[char]
				sequenceRevCom += newchar
		print(sequenceRevCom)
		
		



	
   
		
	