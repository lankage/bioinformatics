#!/usr/bin/python

import argparse
from ReadFasta import ReadFasta

parser = argparse.ArgumentParser()
parser.add_argument("-barcode_defs", help="Specify a barcode definitions file", type=str, required=True)
parser.add_argument("-barcode_ref", help="Specify a barcode reference file", type=str, required=True)
	
args = parser.parse_args()

reader = ReadFasta(args.barcode_ref)
collection = reader.openFasta()


revDictDNA = {"a":"t", "t":"a", "g":"c", "c":"g", "A":"T", "T":"A", "G":"C", "C":"G"}

def revcom(sequenceIn):
	sequenceRev = sequenceIn[::-1]
	sequenceRevCom = ""
	
	for char in sequenceRev:
		newchar = revDictDNA[char]
		sequenceRevCom += newchar
	return sequenceRevCom

with open(args.barcode_defs,'r') as barcodeInfile:
	for line in barcodeInfile:
		barcodeParts = line.split(',')
		forwardBC = barcodeParts[0]
		reverseBC = barcodeParts[1].rstrip()
		forwardName = '>' + forwardBC.zfill(4) + '_Forward'
		reverseNameLookup = '>' + reverseBC.zfill(4) + '_Forward'
		reverseNamePrint = '>' + reverseBC.zfill(4) + '_Reverse'
		
		print(forwardName)
		print(collection[forwardName])
		print(reverseNamePrint)
		print(revcom(collection[reverseNameLookup]))
		
		