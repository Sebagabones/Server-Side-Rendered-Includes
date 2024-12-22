#!/usr/bin/env python3
import os
import argparse
from os import walk
from posixpath import dirname
import re
import shutil
import fileinput


def getListOfFilesToSearch(inputDir, outputDir):
     print(f"Searching in {inputDir}")
     # listOfFiles = os.listdir(inputDir)
     files = ([], [])           # first list is of orginal location, second is of new location

     # dirpath = os.getcwd()
     for (dirpath, dirnames, filenames) in walk(inputDir):
          for name in filenames:
               if(name.endswith(".html")):
                    files[0].append(os.path.join(dirpath, name))
                    print(f"adding {os.path.join(dirpath, name)} to files")
                    print(outputDir[0]+ "/" + str(name))
                    files[1].append((outputDir[0]+ "/" + str(name)))
     return(files)
          # dirs.extend(dirnames)
          # print(f"adding {dirnames} to dirs")
def checkFileForIncludes(fileName, inputDir): # inputdir is placeholder for location of template files
     print(f"Now reading in {fileName}")
     fileRead = open((fileName), "r")
     fileReadIn = fileRead.readlines()
     includeFiles = ([],[])     # first list is text found, second is the text to replace it with
     for line in fileReadIn:
          # will be searching for things of format <!--#include file="file.html"--> where file.html is a html file in same dir
          # in the future I could expand this to be a different dir for templates possibly  Actually now that i think abt it so long as path is relative to where this was run it shoooould work
          includeFiles[0].extend(re.findall(r'<!--#include file=".+\.html"-->', line))
     fileRead.close()
     if(len(includeFiles[0]) != 0):
          print(f"{fileName} has a match at {includeFiles}")
          for matchReg in includeFiles[0]:
               fileToRead = matchReg[19:-4]
               print(f"We want to read in file: {inputDir +"/" + fileToRead}")
               textIn = open(inputDir +"/" + fileToRead, "r")
               textToCopyIn = textIn.read()
               textIn.close()
               print(textToCopyIn)
               includeFiles[1].append(textToCopyIn)
     for index in range(len(includeFiles[0])):
          with fileinput.FileInput(fileName, inplace=True, backup='.bak') as file:
               for line in file:
                    print(line.replace(includeFiles[0][index], includeFiles[1][index]), end='')
def copyFilesToNewLocation(newFileLocation, oldFileLocation):

     os.makedirs(os.path.dirname(newFileLocation), exist_ok=True)
     shutil.copyfile(oldFileLocation, newFileLocation)
# def replaceIncludeWithFile(includeStatement, fileToReadAndCopyFrom, fileToReadInto)


if __name__ == "__main__":
     parser = argparse.ArgumentParser()
     parser.add_argument("-d", "--dir", action="store_true", help="Go through specified directory (recursively)")
     parser.add_argument("inputFile", type=str, help="The input file to parse, if -d is specified than this should be the directory to start searching in - possibly will add ablity to comma seperate list of input files later")
     parser.add_argument("-o", "--output", required=True, nargs=1, type=str, help="The directory for output files to be placed")

     args = parser.parse_args()
     if args.dir:
          # Go through dir checking all files for an include
          filesToSearch = getListOfFilesToSearch(args.inputFile, args.output)
          print(f"list of files to read is {filesToSearch[0]}")
          for fileSearchIndex in range(len(filesToSearch[0])):
               # First copy files to new location
               copyFilesToNewLocation(filesToSearch[1][fileSearchIndex], filesToSearch[0][fileSearchIndex])
               checkFileForIncludes(filesToSearch[1][fileSearchIndex], args.inputFile)
