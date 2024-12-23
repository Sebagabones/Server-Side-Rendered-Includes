#!/usr/bin/env python3
import os
import argparse
from os import walk
from posixpath import dirname
import re
import shutil
import fileinput
import readline
from termcolor import colored
from contextlib import closing

def getListOfFilesToSearch(inputDir, outputDir):
     # print(f"Searching in {inputDir}")
     # listOfFiles = os.listdir(inputDir)
     files = ([], [])           # first list is of orginal location, second is of new location

     # dirpath = os.getcwd()
     for (dirpath, dirnames, filenames) in walk(inputDir):
          for name in filenames:
               if(name.endswith(".html")):
                    files[0].append(os.path.join(dirpath, name))
                    # print(f"adding {os.path.join(dirpath, name)} to files")
                    # print(outputDir[0]+ "/" + str(name))
                    files[1].append((outputDir[0]+ "/" + str(name)))
     return(files)
          # dirs.extend(dirnames)
          # print(f"adding {dirnames} to dirs")
def checkFileForIncludes(fileName, inputDir): # inputdir is placeholder for location of template files
     # print(f"Now reading in {fileName}")
     fileRead = open((fileName), "r")
     fileReadIn = fileRead.readlines()
     includeFiles = ([],[])     # first list is text found, second is the text to replace it with
     for line in fileReadIn:
          # will be searching for things of format <!--#include file="file.html"--> where file.html is a html file in same dir
          # in the future I could expand this to be a different dir for templates possibly  Actually now that i think abt it so long as path is relative to where this was run it shoooould work
          includeFiles[0].extend(re.findall(r'<!--#include file=".+\.html"-->', line))
     fileRead.close()
     if(len(includeFiles[0]) != 0):
          print(f"{fileName} has a match(es) with {includeFiles[0]}")
          copyOfInitialIncludesFile = includeFiles[0].copy()
          for matchReg in copyOfInitialIncludesFile:
               fileToRead = matchReg[19:-4]
               # print(f"We want to read in file: {inputDir + '/' + fileToRead}")
               if not os.path.exists(inputDir + '/' + fileToRead):
                    print(colored(f"Could not find file: {inputDir +'/' + fileToRead}, which was requested by {fileName} - make sure you are following all the rules laid out about directory locations specfied in --help \n", "red"))
                    includeFiles[0].remove(matchReg) # remove the include file from list cause no cant read it lol
                    # print(includeFiles)
                    continue

               textIn = open(inputDir +"/" + fileToRead, "r")
               textToCopyIn = textIn.read()
               # print(textToCopyIn)
               includeFiles[1].append(textToCopyIn)
               textIn.close()
     for index in range(len(includeFiles[0])):
          with fileinput.FileInput(fileName, inplace=True) as files:
               for line in files:
                    print(line.replace(includeFiles[0][index], includeFiles[1][index]), end='')
                    
     # return(1)

def copyFilesToNewLocation(newFileLocation, oldFileLocation):
     # print(f"copying files from {oldFileLocation} to  {newFileLocation}")
     # print(f"newFileLocation {newFileLocation}")
     os.makedirs(os.path.dirname(newFileLocation), exist_ok=True)
     shutil.copy2(oldFileLocation, newFileLocation)

# def replaceIncludeWithFile(includeStatement, fileToReadAndCopyFrom, fileToReadInto)


if __name__ == "__main__":
     parser = argparse.ArgumentParser()
     parser.add_argument("-d", "--dir", action="store_true", help="Go through specified directory (recursively)")
     parser.add_argument("inputFile", type=str, nargs='+', help="The input file to parse, if -d is specified than this should be the directory to start searching in - if you are specifying the files without using -d please be aware that the file outputs will be in OUTPUT/filepath_given_here. The files (if not using -d) must also all be the in same directory if you do not specify a directory for templates (otherwise the directory the last file given is in will be used for template searching)")
     parser.add_argument("-t", "--templates-dir",  nargs=1, type=str, help="Collect template files from this directory")
     parser.add_argument("-o", "--output", default=".", nargs=1, type=str, help="The directory for output files to be placed (default is current directory)")
     parser.add_argument("--no-warning",action="store_true" , help="Don't print a warning when you are about to overwrite your existing files (this warning is only in effect when not using -d, by default unless you specifiy the same location of output as input when using -d you should not overwrite any template files)")



     args = parser.parse_args()
     filesToSearch = ([],[])
     templatesDir = "."         # This *should* be fine?



     if args.dir:
          for directory in args.inputFile:
               # Go through dir checking all files for an include
               if not os.path.exists(directory):
                    print(colored(f"{directory} does not exist - we are going to skip it", "yellow"))
                    continue
               filesToSearch = getListOfFilesToSearch(directory, args.output)
               templatesDir=args.inputFile
               # print(f"list of files to read is {filesToSearch[0]}")
     else:

          print(args.inputFile)
          lastGoodFile = "."
          for files in args.inputFile:
               if not os.path.isfile(files):
                    print(colored(f"{files} does not exist - we are going to skip it", "yellow"))
                    continue
               filesToSearch[0].append(str(files))
               lastGoodFile = files
               filePathOut = args.output[0]+ "/" + str(files)
               safeMode = False
               if os.path.exists(filePathOut) and args.no_warning == False:

                    print(colored(f"Warning, you are about to overwrite {filePathOut}, do you want to continue (if you did not intend to do please look at the -d and -o options)? y/N", "red"))
                    print(colored("If you want to continue but have each output file end with '.ssi' to prevent overwriting template files press S", "yellow"))
                    print(colored("(to turn off this alert pass --no-warning)", "yellow"))
                    continueVal = str(input('').strip() or "N")
                    if(continueVal == "y" or continueVal == "Y" or continueVal == "yes" or continueVal == "Yes"):
                         print(colored(f"{filePathOut} will be overwritten", "red"))
                    elif(continueVal == "s" or continueVal == "S"):
                         safeMode = True
                    else:
                         print("Exiting without any changes")
                         exit()

               if(safeMode):
                    filesToSearch[1].append(args.output[0]+ "/" + str(files) + ".ssi") # Prevent overwriting exisiting files
               else:
                    filesToSearch[1].append(args.output[0]+ "/" + str(files))

          # print(filesToSearch)
          # print(files)
          if args.templates_dir is None: # Get templates from same dir as rest of html files

               templatesDir=re.findall(r".*\/",lastGoodFile)
               templatesDir[0] = templatesDir[0][:-1]


          #
          # exit()

     for fileSearchIndex in range(len(filesToSearch[0])):
               # First copy files to new location
               # print(filesToSearch)
               copyFilesToNewLocation(filesToSearch[1][fileSearchIndex], filesToSearch[0][fileSearchIndex])
               if args.templates_dir is None: # Get templates from same dir as rest of html files
                    checkFileForIncludes(filesToSearch[1][fileSearchIndex], templatesDir[0])
               else:
                    checkFileForIncludes(filesToSearch[1][fileSearchIndex], args.templates_dir[0])
