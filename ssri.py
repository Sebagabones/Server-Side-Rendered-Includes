#!/usr/bin/env python3
import os
import argparse
from os import walk
import re
import shutil
import fileinput
import readline                 # I like having inputs work well with navigation - sue me
import glob
# from termcolor import colored

# Coloured Outputs Constants
CRED     = '\33[91m'
CGREEN   = '\33[92m'
CYELLOW  = '\33[93m'
CEND     = '\33[0m'

def getListOfFilesToSearchDir(inputDir, outputDir):
     files = ([], [])           # first list is of orginal location, second is of new location
     global noWarnings
     global numWarnings

     for (dirpath, subdirs, filenames) in walk(inputDir): # breaks without dirnames, so that's staying here I guess lmao
          safeMode = False
          for name in filenames:
               # print(subdirs)
               if(name.endswith(".html")):
                    if os.path.exists((outputDir[0]+ "/" + str(name))) and noWarnings == False and safeMode == False:
                         print(f"{CRED}Warning, you are about to overwrite {outputDir[0]+ '/' + name}, do you want to continue (if you did not intend to do please look at the -o option)? y/N{CEND}")
                         print(f"{CYELLOW}If you want to continue but have each output file end with '.ssri' to prevent overwriting template files press s{CEND}")
                         print(f"{CYELLOW}(to turn off this alert pass --no-warnings){CEND}")
                         print(f"{CRED}If you want to turn off all warnings for the rest of this run press a {CEND}")
                         continueVal = str(input('').strip() or "N")
                         if(continueVal == "y" or continueVal == "Y" or continueVal == "yes" or continueVal == "Yes"):
                              print(f"{CRED}{name} will be overwritten{CEND}")
                         elif(continueVal == "s" or continueVal == "S"):
                              safeMode = True
                         elif(continueVal == "a" or continueVal == "A"):
                              noWarnings = True
                         else:
                              print(f"{CGREEN}Exiting without any changes {CEND}")
                              exit()

                    if(safeMode):
                         # print(name)

                         dirPathNewOutput = dirpath.replace(inputDir, outputDir[0], 1)

                         files[0].append(os.path.join(dirpath, name))
                         # print(f"adding {os.path.join(dirpath, name)} to files")
                         name = name + ".ssri" # Prevent overwriting exisiting files))
                         # print(outputDir[0]+ "/" + str(name))
                         files[1].append(os.path.join(dirPathNewOutput, name))
                         # print(f"adding {os.path.join(dirPathNewOutput, name)} to files")

                         # files[1].append((outputDir[0]+ "/" + str(name)))
                    else:
                         dirPathNewOutput = dirpath

                         dirPathNewOutput = dirpath.replace(inputDir, outputDir[0], 1)


                         files[0].append(os.path.join(dirpath, name))
                         files[1].append(os.path.join(dirPathNewOutput, name))
                         # print(f"adding {os.path.join(dirPathNewOutput, name)} to files")
     verboseMsg = "The following files will be checked for include statements:\n"
     verboseMsg += ', '.join(map(str, files[0]))
     verbosePrint(verboseMsg)
     verboseMsg = "\nThe following files will be the output files:\n"
     verboseMsg += ', '.join(map(str, files[1]))
     verbosePrint(verboseMsg)
     verbosePrint("\n")


     return(files)


def getListOfFilesToSearchFiles(inputFile, outputDir, templates):
     global numWarnings
     global safeMode
     global noWarnings
     filesToSearch = ([],[])
     lastGoodFile = "."
     safeMode = False
     for files in inputFile:
          if not os.path.isfile(files):
               print(f"{CYELLOW}! {files} does not exist - we are going to skip it{CEND}")
               numWarnings += 1
               continue
          filesToSearch[0].append(str(files))
          lastGoodFile = files
          filePathOut = outputDir[0]+ "/" + str(files)
          if os.path.exists(filePathOut) and noWarnings == False and safeMode == False:

               print(f"{CRED}Warning, you are about to overwrite {filePathOut}, do you want to continue (if you did not intend to do please look at the -o option)? y/N{CEND}")
               print(f"{CYELLOW}If you want to continue but have each output file end with '.ssri' to prevent overwriting template files press S{CEND}")
               print(f"{CYELLOW}(to turn off this alert pass --no-warnings){CEND}")
               print(f"{CRED}If you want to turn off all warnings for the rest of this run press a {CEND}")
               continueVal = str(input('').strip() or "N")
               if(continueVal == "y" or continueVal == "Y" or continueVal == "yes" or continueVal == "Yes"):
                    print(f"{CRED}{filePathOut} will be overwritten{CEND}")
               elif(continueVal == "s" or continueVal == "S"):
                    safeMode = True
               elif(continueVal == "a" or continueVal == "A"):
                    noWarnings = True
               else:
                    print("{CGREEN}Exiting without any changes {CEND}")
                    exit()

          if(safeMode):
               filesToSearch[1].append(outputDir[0]+ "/" + str(files) + ".ssri") # Prevent overwriting exisiting files
          else:

               print(re.findall(r"([^\/]+$)",str(files)))
               filesToSearch[1].append(outputDir[0]+ "/" + re.findall(r"([^\/]+$)",str(files))[0])

          # print(filesToSearch)
          # print(files)
     if templates is None: # Get templates from same dir as rest of html files
          if lastGoodFile != ".":
               templatesDir=re.findall(r".*\/",lastGoodFile)
               if len(templatesDir) == 0: # means the file was grabbed from the cwd
                    templatesDir = "."
               else:
                    templatesDir[0] = templatesDir[0][:-1]
          else:                 # Well, you didn't have any working files, but I guess I will let you continue, and set template dir to the cwd
               templatesDir = "."
     else:
          templatesDir = templates
     files = filesToSearch
     verboseMsg = "The following files will be checked for include statements:\n"
     verboseMsg += ', '.join(map(str, files[0]))
     verbosePrint(verboseMsg)
     verboseMsg = "\nThe following files will be the output files:\n"
     verboseMsg += ', '.join(map(str, files[1]))
     verbosePrint(verboseMsg)
     verboseMsg = "The directory for templates is " + templatesDir[0] +"\n"
     verbosePrint(verboseMsg)
     return(filesToSearch, templatesDir)


def checkFileForIncludes(fileName, inputDir): # inputdir is placeholder for location of template files - not anymore lol, now it is template dir
     # print(f"Now reading in {fileName}")
     fileRead = open((fileName), "r")
     fileReadIn = fileRead.readlines()
     includeFiles = ([],[])     # first list is text found, second is the text to replace it with
     global numFilesChanged
     global numWarnings

     for line in fileReadIn:
          includeFiles[0].extend(re.findall(r'<!--.*#include file=".+".*-->', line))
     fileRead.close()
     if(len(includeFiles[0]) != 0):
          verboseMsg = f"{fileName} has match(es) with {includeFiles[0]}"
          verbosePrint(verboseMsg)
          copyOfInitialIncludesFile = includeFiles[0].copy()
          for matchReg in copyOfInitialIncludesFile:
               fileToRead = re.search(r'"(.+)"', matchReg).group().strip('"')

               verboseMsg = f"We want to read in file: {inputDir + '/' + fileToRead}"
               verbosePrint(verboseMsg)
               if not os.path.exists(inputDir + '/' + fileToRead):
                    print(f"{CRED}! Could not find file: {inputDir +'/' + fileToRead}, which was requested by {fileName} - make sure you are following all the rules laid out about directory locations specfied in --help {CEND}\n")
                    numWarnings += 1
                    includeFiles[0].remove(matchReg) # remove the include file from list cause cant read it lol
                    # print(includeFiles)
                    continue

               textIn = open(inputDir +"/" + fileToRead, "r")
               textToCopyIn = textIn.read()
               # print(textToCopyIn)
               includeFiles[1].append(textToCopyIn)
               textIn.close()
          verbosePrint("\n")
     for index in range(len(includeFiles[0])):
          with fileinput.FileInput(fileName, inplace=True) as files:
               for line in files:
                    print(line.replace(includeFiles[0][index], includeFiles[1][index]), end='')
     if(len(includeFiles[0]) > 1):
          print(f"{CGREEN}✓ {fileName} successfully completed with {len(includeFiles[0])} templates added in {CEND}")
          numFilesChanged += 1
     elif(len(includeFiles[0]) == 1):
          print(f"{CGREEN}✓ {fileName} successfully completed with {len(includeFiles[0])} template added in {CEND}")
          numFilesChanged += 1



def copyFilesToNewLocation(newFileLocation, oldFileLocation):
     # print(f"copying files from {oldFileLocation} to  {newFileLocation}")
     # print(f"newFileLocation {newFileLocation}")
     global fileCreatedCounter
     fileCreatedCounter += 1
     os.makedirs(os.path.dirname(newFileLocation), exist_ok=True)
     shutil.copy2(oldFileLocation, newFileLocation)


def verbosePrint(msg):
     global verbose
     if verbose:
          print(msg)
     return



def main():
     parser = argparse.ArgumentParser()
     parser.add_argument("-d", "--dir", action="store_true", help="Go through specified directory (recursively)")
     parser.add_argument("inputFile", type=str, nargs='+', help="The input file to parse, if -d is specified than this should be the directory to start searching in - if you are specifying the files without using -d please be aware that the file outputs will be in OUTPUT/filename, directory structure will not be kept. The files (if not using -d) must also all be the in same directory if you do not specify a directory for templates (otherwise the directory the last file given is in will be used for template searching)")
     parser.add_argument("-t", "--templates-dir",  nargs=1, type=str, help="Collect template files from this directory")
     parser.add_argument("-o", "--output", default=".", nargs=1, type=str, help="The directory for output files to be placed (default is current directory)")
     parser.add_argument("--no-warnings",action="store_true" , help="Don't print a warning when you are about to overwrite your existing files")
     parser.add_argument("-v", "--verbose",action="store_true" , help="Increased printing what the script is doing at any time")

     # Future plan, make a flag that copies all files/dirs in directory over, not just .html files
     # Also in future maybe add in an ablity to nest include files in include files - this might already work tbh, or at least there is a janky way to do it lol
     # Also do verbosity at some point

     args = parser.parse_args()

     templatesDir=args.inputFile         # This *should* be fine?

     global fileCreatedCounter
     fileCreatedCounter = 0
     global noWarnings
     noWarnings = args.no_warnings
     global verbose
     verbose = args.verbose
     global numFilesChanged     # Number of files that have had include statements with modifications
     global numWarnings
     numWarnings = 0
     numFilesChanged = 0
     os.makedirs(os.path.dirname(args.output[0] + "/"), exist_ok=True)
     filesToSearch = None
     if args.dir:
          for directory in args.inputFile:
               # Go through dir checking all files for an include
               if not os.path.exists(directory):
                    print(f"{CYELLOW}! {directory} does not exist - we are going to skip it{CEND}")
                    numWarnings += 1
                    continue
               if os.path.isfile(directory):
                    print(f"{CYELLOW}! {directory} is a file, so skipping it{CEND}")
                    numWarnings += 1
                    continue
               filesToSearch = getListOfFilesToSearchDir(directory, args.output)

               # print(f"list of files to read is {filesToSearch[0]}")
     else:
          filesToSearch, templatesDir = getListOfFilesToSearchFiles(args.inputFile, args.output, args.templates_dir)

     if(filesToSearch == None):
          print(f"{CRED}! No files were able to be scanned, exiting {CEND}")
          exit()
     for fileSearchIndex in range(len(filesToSearch[0])):
               # First copy files to new location
               # print(filesToSearch)
               copyFilesToNewLocation(filesToSearch[1][fileSearchIndex], filesToSearch[0][fileSearchIndex])
               if args.templates_dir is None: # Get templates from same dir as rest of html files
                    checkFileForIncludes(filesToSearch[1][fileSearchIndex], templatesDir[0])
               else:
                    checkFileForIncludes(filesToSearch[1][fileSearchIndex], args.templates_dir[0])
     if(numWarnings == 0):
          printColour = CGREEN
          includeText = "✓"
     else:
          printColour = CRED
          includeText = "!"
     if(args.dir):
          print(f"{printColour}{includeText} Looked at {fileCreatedCounter} files in {args.inputFile[0]}, found {numFilesChanged} file(s) with include statements, and output files to {args.output[0]} {CEND}")
     if numWarnings == 1:
          print(f"{printColour}{includeText} {numWarnings} error encountered {CEND}")
     else:
          print(f"{printColour}{includeText} {numWarnings} errors encountered {CEND}")

if __name__ == "__main__":
     main()
