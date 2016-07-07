# bioinformatics
## Selected Bioinformatics Tools for Oligonucleotide design and High Throughput sequencing output file manipulation


### OligoCompat.py
OligoCompat.py is a software tool used for comparing sets of oligonucleotide sequences to other sets 
of oligonucleotide sequences to look for opportunities for hybridization.  The general use case is to 
screen designed sets of oligos for compatibility with each other.  The simplest case being the comparison
of a forward and reverse primer for the potential to form a primer-dimer.  
OligoCompat.py is more sensitive than the primer-dimer screening built in many primer design programs, as it 
doesn't limit the output to 3' ends that complement each other exactly. 

OligoCompat.py can also be used for 
looking for internal structure, folding or unwanted hybridization between two oligos.  Another use case is to 
investigate whether or not a molecular probe is predicted to bind to a oligonucleotide in a reagent mix.
This tools can be used for investigative purposes where undesireable behavior in a reaction is occurring, such
as weak amplification, unexplained gel bands etc. but adjusting the match stringency incrementally down until
structure between oligos is observed.
```
usage: OligoCompat.py [-h] -file1 FASTA -file2 FASTA [-w word size]
                      [-m minimum total matches]

optional arguments:
  -h, --help                show this help message and exit
  -file1 FASTA              Specify a query fasta file
  -file2 FASTA              Specify a subject fasta file
  -w word size              Specify a min word size
  -m minimum total matches  Specify a minimum total matches
```

OligoCompat.py outputs alignments between sequences showing base matching between sequences which represents
complementarity.  In each alignment one of the sequences is reverse-complemented.

Example output:

```
Primer test2 and Primer test1 form a 7-base Primer-Dimer
Primer test1 and Primer test2 form a 7-base Primer-Dimer
Top Sequence (5'-3'): test1	{D:7,C:7|7;1;1;1,T:10,ID:0}
Bottom Sequence (3'-5' RC): test2 [7, 0, 15]
GACTAGCATAGCATCTACTGCATCTA
          ||||||| |  |   |
          GCATCTAATCGACTGATGCTAGT

Primer test1 and Primer test2 form a 7-base Primer-Dimer
Top Sequence (5'-3'): test1	{D:7,C:7|7,T:7,ID:1}
Bottom Sequence (3'-5' RC): test2 [7, 0, 6]
GACTAGCATAGCATCTACTGCATCTA
                   |||||||
                   GCATCTAATCGACTGATGCTAGT
```                   
  
