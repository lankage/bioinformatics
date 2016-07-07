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
Dependencies:
Requires python3 installed. Requires nuc.py and ReadFasta.py in working directory.

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
  




### Pivotron Geneious plugin
Pivotron is a Geneious plugin that operates on contig assembly files within Geneious. Pivotron creates a text file within geneious as output that lists counts of reads broken out by contig name (allele name) and by barcode identifier.  Pivotron looks for barcode identifiers appended to the sequencing read header.  Raw reads used in a mapping need to have been name appended prior to being assembled into contigs.

To Install:

Drag and drop the .gplugin file onto a running Geneious window.

To use:

Select 1 or more contig files (the three red lines) that are the result of mapping to reference.  Click "Activate Pivotron" on the menu bar at the top.  A Text File will be generated that contains the pivoted information.  As geneious doesn't have an export function for a text file yet, we have to do a simple workaround to get the data out of Geneious.  Open a new text file in any text editor.  Select the Text File output from Pivotron within Geneious.  Highlight all the text in the Text View window and copy it.  Paste this text into your empty text document.   This file can now be imported using excels text import feature.

Pivotron expects reads to be **name appended** like the following formats:

m151105_060456_42238_c100909452550000001823206504301616_s1_p0/144308/ccs/**0012_Forward--0013_Reverse.zerolen.fastq** -> "0012_Forward--0013_Reverse" appears as column in table

m151105_060456_42238_c100909452550000001823206504301616_s1_p0/144308/ccs/**KT0918** -> "KT0918" appears as column in table

m151115_083855_42134_c100936172550000001823205704291617_s1_p0/85/ccs/**0001_F--0001_R.zerolen.fastq** -> "0001_F--0001_R" appears as column in table

Preparing the sequencing reads with names appended can be accomplished in Geneious using the Batch Rename function, or externally via script.
