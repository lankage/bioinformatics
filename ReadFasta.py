#!/usr/bin/python
# Fasta Reader utility class
# 10/1/2014
# Michael Graham

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
	
        
if __name__ == "__main__":

	testRead = ReadFasta('test.fasta')
	collection = testRead.openFasta()

	for name in collection:
		
		print(name,collection[name])
		