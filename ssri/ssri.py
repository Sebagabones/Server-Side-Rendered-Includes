#!/usr/bin/env python3
from collections import namedtuple
import os
import argparse
from os import walk
import re
import shutil
import fileinput
import readline  # I like having inputs work well with navigation - sue me
import sys
# from termcolor import colored

# Coloured Outputs Constants
CRED = "\33[91m"
CGREEN = "\33[92m"
CYELLOW = "\33[93m"
CEND = "\33[0m"


def getListOfFilesToSearchDir(inputDir, outputDir, noWarnings, verbose):
    files = ([], [])  # first list is of orginal location, second is of new location

    for dirpath, subdirs, filenames in walk(
        inputDir
    ):  # breaks without dirnames, so that's staying here I guess lmao
        safeMode = False
        for name in filenames:
            # print(subdirs)
            if name.endswith(".html"):
                if (
                    os.path.exists((outputDir[0] + "/" + str(name)))
                    and noWarnings == False
                    and safeMode == False
                ):
                    print(
                        f"{CRED}Warning, you are about to overwrite {outputDir[0]+ '/' + name}, do you want to continue (if you did not intend to do please look at the -o option)? y/N{CEND}"
                    )
                    print(
                        f"{CYELLOW}If you want to continue but have each output file end with '.ssri' to prevent overwriting template files press s{CEND}"
                    )
                    print(f"{CYELLOW}(to turn off this alert pass --no-warnings){CEND}")
                    print(
                        f"{CRED}If you want to turn off this warning for the rest of this run press a {CEND}"
                    )
                    continueVal = str(input("").strip() or "N")
                    if (
                        continueVal == "y"
                        or continueVal == "Y"
                        or continueVal == "yes"
                        or continueVal == "Yes"
                    ):
                        print(f"{CRED}{name} will be overwritten{CEND}")
                    elif continueVal == "s" or continueVal == "S":
                        safeMode = True
                    elif continueVal == "a" or continueVal == "A":
                        noWarnings = True
                    else:
                        print(f"{CGREEN}Exiting without any changes {CEND}")
                        exit()

                if safeMode:
                    # print(name)

                    dirPathNewOutput = dirpath.replace(inputDir, outputDir[0], 1)

                    files[0].append(os.path.join(dirpath, name))
                    # print(f"adding {os.path.join(dirpath, name)} to files")
                    name = name + ".ssri"  # Prevent overwriting exisiting files))
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
    verboseMsg += ", ".join(map(str, files[0]))
    # verbosePrint(verboseMsg)
    verboseMsg += "\nThe following files will be the output files:\n"
    verboseMsg += ", ".join(map(str, files[1]))
    verboseMsg += "\n"

    verbosePrint(verbose, verboseMsg)

    return files


def getListOfFilesToSearchFiles(
    inputFile, outputDir, templates, noWarnings, numWarnings, verbose
):
    filesToSearch = ([], [])
    lastGoodFile = "."
    safeMode = False
    for files in inputFile:
        if not os.path.isfile(files):
            if os.path.exists(files):
                print(
                    f"{CYELLOW}! {files} is a directory, please use the '-d' flag - we are going to skip it{CEND}"
                )
                numWarnings += 1
                continue
            print(f"{CYELLOW}! {files} does not exist - we are going to skip it{CEND}")
            numWarnings += 1
            continue

        filesToSearch[0].append(str(files))
        lastGoodFile = files
        filePathOut = outputDir[0] + "/" + str(files)
        if os.path.exists(filePathOut) and noWarnings == False and safeMode == False:
            print(
                f"{CRED}Warning, you are about to overwrite {filePathOut}, do you want to continue (if you did not intend to do please look at the -o option)? y/N{CEND}"
            )
            print(
                f"{CYELLOW}If you want to continue but have each output file end with '.ssri' to prevent overwriting template files press S{CEND}"
            )
            print(f"{CYELLOW}(to turn off this alert pass --no-warnings){CEND}")
            print(
                f"{CRED}If you want to turn off this warning for the rest of this run press a {CEND}"
            )
            continueVal = str(input("").strip() or "N")
            if (
                continueVal == "y"
                or continueVal == "Y"
                or continueVal == "yes"
                or continueVal == "Yes"
            ):
                print(f"{CRED}{filePathOut} will be overwritten{CEND}")
            elif continueVal == "s" or continueVal == "S":
                safeMode = True
            elif continueVal == "a" or continueVal == "A":
                noWarnings = True
            else:
                print("{CGREEN}Exiting without any changes {CEND}")
                exit()

        if safeMode:
            filesToSearch[1].append(
                outputDir[0] + "/" + str(files) + ".ssri"
            )  # Prevent overwriting exisiting files
        else:
            print(re.findall(r"([^\/]+$)", str(files)))
            filesToSearch[1].append(
                outputDir[0] + "/" + re.findall(r"([^\/]+$)", str(files))[0]
            )

        # print(filesToSearch)
        # print(files)
    if templates is None:  # Get templates from same dir as rest of html files
        if lastGoodFile != ".":
            templatesDir = re.findall(r".*\/", lastGoodFile)
            if len(templatesDir) == 0:  # means the file was grabbed from the cwd
                templatesDir = "."
            else:
                templatesDir[0] = templatesDir[0][:-1]
        else:  # Well, you didn't have any working files, but I guess I will let you continue, and set template dir to the cwd
            templatesDir = "."
    else:
        templatesDir = templates
    files = filesToSearch
    verboseMsg = "The following files will be checked for include statements:\n"
    verboseMsg += ", ".join(map(str, files[0]))
    verbosePrint(verbose, verboseMsg)
    verboseMsg = "\nThe following files will be the output files:\n"
    verboseMsg += ", ".join(map(str, files[1]))
    verbosePrint(verbose, verboseMsg)
    verboseMsg = "The directory for templates is " + templatesDir[0] + "\n"
    verbosePrint(verbose, verboseMsg)
    return (filesToSearch, templatesDir, numWarnings)


def checkFilesForIncludes(
    filesToSearch, templateDir, numFilesChanged, verbose, numWarnings
):  # Returns a dict where templateFile : set( namedTuples(fileWithIncludeStatement, includeStatementTest)  )
    dictionaryOfFilesToInclude = dict()
    fileNameIncludeTextStruct = namedtuple(
        "fileNameIncludeText", ["fileName", "includeText"]
    )
    for fileName in filesToSearch:
        fileRead = open((fileName), "r")
        fileReadIn = fileRead.readlines()
        includeFiles = (
            [],
            [],
        )  # first list is text found, second is the text to replace it with

        for line in fileReadIn:
            includeFiles[0].extend(re.findall(r'<!--.*#include file=".+".*-->', line))
            fileRead.close()

        if len(includeFiles[0]) != 0:
            verboseMsg = f"{fileName} has match(es) with {includeFiles[0]}"
            verbosePrint(verbose, verboseMsg)
            # copyOfInitialIncludesFile = includeFiles[0].copy()
            for matchReg in includeFiles[0]:
                fileToRead = re.search(r'"(.+)"', matchReg).group().strip('"')
                fullPathOfInclude = templateDir + "/" + fileToRead
                verboseMsg = (
                    f"Will attempt to be reading in in file: {fullPathOfInclude}"
                )
                verbosePrint(verbose, verboseMsg)
                if not os.path.exists(fullPathOfInclude):
                    print(
                        f"{CRED}! Could not find file: {fullPathOfInclude}, which was requested by {fileName} - make sure you are following all the rules laid out about directory locations specfied in --help {CEND}\n"
                    )
                    numWarnings += 1
                    continue

                fileNameIncludeText = fileNameIncludeTextStruct(fileName, matchReg)
                if fullPathOfInclude in dictionaryOfFilesToInclude.keys():
                    dictionaryOfFilesToInclude[fullPathOfInclude].add(
                        fileNameIncludeText
                    )
                else:
                    dictionaryOfFilesToInclude.update(
                        {fullPathOfInclude: {fileNameIncludeText}}
                    )
            numFilesChanged += 1

    return (dictionaryOfFilesToInclude, numFilesChanged, numWarnings)


def getTextForIncludeFile(templateFile):  # Returns the contents of the template file
    textIn = open(templateFile, "r")
    textToCopyIn = textIn.read()
    # print(textToCopyIn)

    textIn.close()
    return textToCopyIn


def writeTextToFiles(
    templateFile, fileList, verbose
):  # write the provided template file into the fileList (which is actually a set of named tuples)
    # TODO: Change this to do multithreading - will want to swap out from using fileinput when you do this though
    verbosePrint(verbose, "\n")
    textToAdd = getTextForIncludeFile(templateFile)
    typesOfInclude = set([fileIn.includeText for fileIn in fileList])

    fileListThatIsAList = [fileIn.fileName for fileIn in fileList]
    for includeText in typesOfInclude:
        # print(includeText)
        with fileinput.FileInput(fileListThatIsAList, inplace=True) as files:
            for line in files:
                # print(f"would be replacing {fileIn.includeText} with {textToAdd}")
                print(line.replace(includeText, textToAdd), end="")
    if len(fileList) > 1:
        print(
            f"{CGREEN}✓ {templateFile} successfully included in  {len(fileList)} files {CEND}"
        )
        # numFilesChanged += 1
    elif len(fileList) == 1:
        print(
            f"{CGREEN}✓ {templateFile} successfully included in {len(fileList)} file {CEND}"
        )
        # numFilesChanged += 1
    # return(numFilesChanged)


def copyFilesToNewLocation(newFileLocation, oldFileLocation):
    # print(f"copying files from {oldFileLocation} to {newFileLocation}")
    # print(f"newFileLocation {newFileLocation}")
    # fileCreatedCounter += 1
    os.makedirs(os.path.dirname(newFileLocation), exist_ok=True)
    shutil.copy2(oldFileLocation, newFileLocation)
    # return(fileCreatedCounter)


def verbosePrint(verbose, msg):
    if verbose:
        print(msg)
    return


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--dir",
        action="store_true",
        help="Go through specified directory (recursively)",
    )
    parser.add_argument(
        "inputFile",
        type=str,
        nargs="+",
        help="The input file to parse, if -d is specified than this should be the directory to start searching in - if you are specifying the files without using -d please be aware that the file outputs will be in OUTPUT/filename, directory structure will not be kept. The files (if not using -d) must also all be the in same directory if you do not specify a directory for templates (otherwise the directory the last file given is in will be used for template searching)",
    )
    parser.add_argument(
        "-t",
        "--templates-dir",
        nargs=1,
        type=str,
        help="Collect template files from this directory",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=".",
        nargs=1,
        type=str,
        help="The directory for output files to be placed (default is current directory)",
    )
    parser.add_argument(
        "--no-warnings",
        action="store_true",
        help="Don't print a warning when you are about to overwrite your existing files",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Increased printing what the script is doing at any time",
    )
    parser.add_argument(
        "-c",
        "--copy-all",
        action="store_true",
        help="Copy all files in the specified directory (must be used with -d and a single source directory)",
    )
    return parser.parse_args(args)

    # Future plan, make a flag that copies all files/dirs in directory over, not just .html files
    # Also in future maybe add in an ablity to nest include files in include files - this might already work tbh, or at least there is a janky way to do it lol



def copyAllFiles(source, output):
            shutil.copytree(source, output, dirs_exist_ok=True)

def main():
    args = parse_args(sys.argv[1:])

    templatesDir = args.inputFile  # This *should* be fine?

    fileCreatedCounter = 0

    noWarnings = args.no_warnings
    verbose = args.verbose
    numFilesChanged = (
        0  # Number of files that have had include statements with modifications
    )
    global numWarnings
    numWarnings = 0

    os.makedirs(os.path.dirname(args.output[0] + "/"), exist_ok=True)
    filesToSearch = None

    if args.copy_all:
        copyAllFiles(args.inputFile[0], args.output[0])
        noWarnings = True   # Turns off warnings as we will be overwriting new copied files anyway


    if args.dir:
        for directory in args.inputFile:
            # Go through dir checking all files for an include
            if not os.path.exists(directory):
                print(
                    f"{CYELLOW}! {directory} does not exist - we are going to skip it{CEND}"
                )
                numWarnings += 1
                continue
            if os.path.isfile(directory):
                print(f"{CYELLOW}! {directory} is a file, so skipping it{CEND}")
                numWarnings += 1
                continue
            filesToSearch = getListOfFilesToSearchDir(
                directory, args.output, noWarnings, verbose
            )

            # print(f"list of files to read is {filesToSearch[0]}")
    else:
        filesToSearch, templatesDir, numWarnings = getListOfFilesToSearchFiles(
            args.inputFile,
            args.output,
            args.templates_dir,
            noWarnings,
            numWarnings,
            verbose,
        )

    if filesToSearch == None:
        print(f"{CRED}! No files were able to be scanned, exiting {CEND}")
        exit()

        # First copy files to new location
        # print(filesToSearch)
    dictOfTemplatesToFiles = None
    if args.templates_dir is None:  # Get templates from same dir as rest of html files
        for fileSearchIndex in range(len(filesToSearch[0])):
            copyFilesToNewLocation(
                filesToSearch[1][fileSearchIndex], filesToSearch[0][fileSearchIndex]
            )
            fileCreatedCounter += 1
        dictOfTemplatesToFiles, numFilesChanged, numWarnings = checkFilesForIncludes(
            filesToSearch[1], templatesDir[0], numFilesChanged, verbose, numWarnings
        )  # this is a dictionary where key is include file an values is a named tuple with fileName and includeText from the files that ask for the key
        for template in dictOfTemplatesToFiles.items():
            writeTextToFiles(template[0], template[1], verbose)

        # numFilesChanged =
    else:
        for fileSearchIndex in range(len(filesToSearch[0])):
            copyFilesToNewLocation(
                filesToSearch[1][fileSearchIndex], filesToSearch[0][fileSearchIndex]
            )
            fileCreatedCounter += 1
        dictOfTemplatesToFiles, numFilesChanged, numWarnings = checkFilesForIncludes(
            filesToSearch[1],
            args.templates_dir[0],
            numFilesChanged,
            verbose,
            numWarnings,
        )  # this is a dictionary where key is include file an values is a named tuple with fileName and includeText from the files that ask for the key
        # print(dictOfTemplatesToFiles)
        for template in dictOfTemplatesToFiles.items():
            writeTextToFiles(template[0], template[1], verbose)

    if numWarnings == 0:
        printColour = CGREEN
        includeText = "✓"
    else:
        printColour = CRED
        includeText = "!"
    if args.dir:
        print(
            f"{printColour}{includeText} Looked at {fileCreatedCounter} files in {args.inputFile[0]}, found {numFilesChanged} file(s) with include statements, and output files to {args.output[0]} {CEND}"
        )
    if numWarnings == 1:
        print(f"{printColour}{includeText} {numWarnings} error encountered {CEND}")
    else:
        print(f"{printColour}{includeText} {numWarnings} errors encountered {CEND}")


if __name__ == "__main__":
    main()
