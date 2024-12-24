#!/usr/bin/env python3
import os
import argparse
from os import walk
import re
import shutil
import fileinput
import readline                 # I like having inputs work well with navigation - sue me
# from termcolor import colored

# Coloured Outputs Constants
CRED     = '\33[91m'
CGREEN   = '\33[92m'
CYELLOW  = '\33[93m'
CEND     = '\33[0m'

def getListOfFilesToSearch(inputDir, outputDir):
     files = ([], [])           # first list is of orginal location, second is of new location
     global noWarnings
     for (dirpath, dirnames, filenames) in walk(inputDir): # breaks without dirnames, so that's staying here I guess lmao
          safeMode = False
          for name in filenames:
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


                         files[0].append(os.path.join(dirpath, name))
                         print(f"adding {os.path.join(dirpath, name)} to files")
                         name = name + ".ssri" # Prevent overwriting exisiting files))
                         # print(outputDir[0]+ "/" + str(name))
                         files[1].append((outputDir[0]+ "/" + str(name)))
                    else:
                         files[0].append(os.path.join(dirpath, name))
                         print(f"adding {os.path.join(dirpath, name)} to files")
                         # print(outputDir[0]+ "/" + str(name))
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
          includeFiles[0].extend(re.findall(r'<!--.*#include file=".+".*-->', line))
     fileRead.close()
     if(len(includeFiles[0]) != 0):
          print(f"{fileName} has a match(es) with {includeFiles[0]}")
          copyOfInitialIncludesFile = includeFiles[0].copy()
          for matchReg in copyOfInitialIncludesFile:
               fileToRead = re.search(r'"(.+)"', matchReg).group().strip('"')

               # print(f"We want to read in file: {inputDir + '/' + fileToRead}")
               if not os.path.exists(inputDir + '/' + fileToRead):
                    print(f"{CRED}Could not find file: {inputDir +'/' + fileToRead}, which was requested by {fileName} - make sure you are following all the rules laid out about directory locations specfied in --help {CEND}\n")
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
     if(len(includeFiles[0]) > 1):
          print(f"{CGREEN}✓ {fileName} successfully completed with {len(includeFiles[0])} templates added in {CEND}")
     elif(len(includeFiles[0]) == 1):
          print(f"{CGREEN}✓ {fileName} successfully completed with {len(includeFiles[0])} template added in {CEND}")




def copyFilesToNewLocation(newFileLocation, oldFileLocation):
     # print(f"copying files from {oldFileLocation} to  {newFileLocation}")
     # print(f"newFileLocation {newFileLocation}")
     global fileCreatedCounter
     fileCreatedCounter += 1
     os.makedirs(os.path.dirname(newFileLocation), exist_ok=True)
     shutil.copy2(oldFileLocation, newFileLocation)




def main():
     parser = argparse.ArgumentParser()
     parser.add_argument("-d", "--dir", action="store_true", help="Go through specified directory (recursively)")
     parser.add_argument("inputFile", type=str, nargs='+', help="The input file to parse, if -d is specified than this should be the directory to start searching in - if you are specifying the files without using -d please be aware that the file outputs will be in OUTPUT/filepath_given_here. The files (if not using -d) must also all be the in same directory if you do not specify a directory for templates (otherwise the directory the last file given is in will be used for template searching)")
     parser.add_argument("-t", "--templates-dir",  nargs=1, type=str, help="Collect template files from this directory")
     parser.add_argument("-o", "--output", default=".", nargs=1, type=str, help="The directory for output files to be placed (default is current directory)")
     parser.add_argument("--no-warnings",action="store_true" , help="Don't print a warning when you are about to overwrite your existing files (this warning is only in effect when not using -d, by default unless you specifiy the same location of output as input when using -d you should not overwrite any template files)")
     # Future plan, make a flag that copies all files/dirs in directory over, not just .html files
     # Also in future maybe add in an ablity to nest include files in include files - this might already work tbh, or at least there is a janky way to do it lol
     # Also do verbosity at some point

     args = parser.parse_args()
     filesToSearch = ([],[])
     templatesDir = "."         # This *should* be fine?
     global fileCreatedCounter
     fileCreatedCounter = 0
     global noWarnings
     noWarnings = args.no_warnings
     os.makedirs(os.path.dirname(args.output[0] + "/"), exist_ok=True)

     if args.dir:
          for directory in args.inputFile:
               # Go through dir checking all files for an include
               if not os.path.exists(directory):
                    print(f"{CYELLOW}{directory} does not exist - we are going to skip it{CEND}")
                    continue
               filesToSearch = getListOfFilesToSearch(directory, args.output)
               templatesDir=args.inputFile
               # print(f"list of files to read is {filesToSearch[0]}")
     else:
          print(args.inputFile)
          lastGoodFile = "."
          safeMode = False
          for files in args.inputFile:
               if not os.path.isfile(files):
                    print(f"{CYELLOW}{files} does not exist - we are going to skip it{CEND}")
                    continue
               filesToSearch[0].append(str(files))
               lastGoodFile = files
               filePathOut = args.output[0]+ "/" + str(files)
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
                    filesToSearch[1].append(args.output[0]+ "/" + str(files) + ".ssri") # Prevent overwriting exisiting files
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
     print(f"{CGREEN}✓ Created {fileCreatedCounter} new files in {args.output[0]}")

if __name__ == "__main__":
     main()
