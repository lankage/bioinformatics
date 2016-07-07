#!/usr/local/bin/python3

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-fq", help="Specify an input fastq file", type=str)
parser.add_argument("-fa", help="Specify an output file", type=str)
args = parser.parse_args()

myFastq = open(args.fq, 'r') #open fastq file for reading
myFasta = open(args.fa, 'w') #open fasta file for writing
 
while 1: #initiate infinite loop
    #read 4 lines of the fasta file
    SequenceHeader= myFastq.readline()
    Sequence= myFastq.readline()
    QualityHeader= myFastq.readline()
    Quality= myFastq.readline()
    if SequenceHeader == '': #exit loop when end of file is reached
        break
    #write output
    myFasta.write('>%s%s' %(SequenceHeader.strip('@'), Sequence))
 
#close files
myFastq.close()
myFasta.close()