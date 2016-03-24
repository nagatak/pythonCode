#!/usr/bin/env python
#run with 'python reformat.py -pl plink.map -lm .LMmap file > nameOfOutputFile

import argparse
import sys

from operator import itemgetter
from collections import defaultdict

# buffer file into memory, enable search by line number
def bufferFile(f , temp):
    count = 1
    with open(f, 'r') as input:
        for line in input:
            l  = line.strip().split()
            if len(l) > 1:
                temp[str(count)].append(l)
            count += 1
# remove 1st 17 and last chars, also removes period in id.
def cleanId(s):
    return s[17:-1].replace('.','')
# removes _ from scaffold position
def cleanPosition(s):
    return s.replace('_', '')
# Determines starting LG. If LG is not specified at start of file,
# assumes LG is one less than 1st instance found
def LGStart(input):
    count = 1;
    with open(input, 'r') as input:
        for line in input:
            l = line.strip().split()
            if len(l) > 0:
                if str(l[0]).startswith('#***'):
                    if count < 3:
                        input.close()
                        return int(l[3])
                    else:
                        input.close()
                        return int(l[3])-1
            count += 1
# prints file
def writeToFile(corrected):
    print ('Scaffold_ID,Scaffold_position,LG,Genetic_position')
    for i in range (len(corrected)):
        l = corrected[i];
        print str(l[0])+','+str(l[1])+','+str(l[2])+','+str(l[3])
# retrieves the data from buffer, formats the output
def doWork(lineNum, d, temp, lm, corrected, lg):
    l = d[lineNum]
    a = l[0]
    #format the output
    temp=[cleanId(a[0]), cleanPosition(a[1]), lg, lm[1]]
    #append to list
    corrected.append(temp)
# main
def main():
    #declare the vars
    lm = []
    plink = []
    d = defaultdict(list)
    corrected = []
    temp = range(10)
    lg = 0

    #argparse stuff
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_plink', '-pl', help = "Enter the" +\
                        " name of the file.", type = str, required=True)
    parser.add_argument('--input_LMmap', '-lm', help = "Enter the" +\
                        " name of the LMmap files.", type = str, required=True)
    args=parser.parse_args()

    #buffer the file to memory(dictionary)
    bufferFile(args.input_plink, d)
    #find starting LG value
    lg = LGStart(args.input_LMmap)
    #parse the file
    with open(args.input_LMmap, 'r') as input:
        for line in input:
            lm = line.strip().split()
            if len(lm) > 0:
                if str(lm[0]).startswith('#***'):
                    if(lg<int(lm[3])):
                        lg = int(lm[3])
                if not str(lm[0]).startswith('#'):
                    doWork(lm[0], d, temp, lm, corrected, lg)
            lm [:] = []
    #print
    writeToFile(corrected)


if __name__ == "__main__":
    main()
