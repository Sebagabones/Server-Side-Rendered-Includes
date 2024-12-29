#!/usr/bin/env python3
#import ssri
# import ssri
import ssri
import sys
import filecmp
import pytest
from pathlib import Path
import os
import shutil


def test_verbose(snapshot):
    verbose = ssri.parse_args(["-v", "inputFile"])
    # print(verbose)
    assert verbose == snapshot


def test_dir(snapshot):
    dirCheck = ssri.parse_args(["-d","dir"])
    assert dirCheck == snapshot

def test_infile(snapshot):
    filecheck = ssri.parse_args(["inputFile"])
    assert filecheck == snapshot

def test_templates_infile(snapshot):
    filecheck = ssri.parse_args(["inputFile", "-t", "template"])
    assert filecheck == snapshot


def test_templates_dir(snapshot):
    dirCheck = ssri.parse_args(["-d","dir", "-t", "templates"])
    assert dirCheck == snapshot

def test_templates_output_dir(snapshot):
    dirCheck = ssri.parse_args(["-d","dir", "-t", "templates", "-o", "output"])
    assert dirCheck == snapshot


def test_templates_output_infile(snapshot):
    filecheck = ssri.parse_args(["inputFile", "-t", "template", "-o", "output"])
    assert filecheck == snapshot

def test_readfilesDir(snapshot):
    listFiles = ssri.getListOfFilesToSearchDir("tests/testFolder/staging", ["tests/testFolder/sites"], True, False )
    listFilesSort = (sorted(listFiles[0]), sorted(listFiles[1]))
    assert listFilesSort == snapshot

def test_readfilesFile(snapshot):
    listFiles = ssri.getListOfFilesToSearchFiles(["tests/testFolder/staging/emacsFiles.html"], ["tests/testFolder/sites"], "tests/testFolder/templates", False, 0, False)
    assert listFiles == snapshot

def test_lookForInclude(snapshot):
    inputFiles = ssri.getListOfFilesToSearchDir("tests/testFolder/staging", ["tests/testFolder/sites"], True, False)
    inputFilesSort = (sorted(inputFiles[0]), sorted(inputFiles[1]))
    assert inputFilesSort == snapshot


def test_checkCopyFiles(snapshot):
    inputFiles = ssri.getListOfFilesToSearchDir("tests/testFolder/staging", ["tests/testFolder/sites"], True, False)
    fileCreatedCounter = 0
    numFilesCopied = 0
    for fileSearchIndex in range(len(inputFiles[0])):
        ssri.copyFilesToNewLocation(inputFiles[1][fileSearchIndex], inputFiles[0][fileSearchIndex])
        numFilesCopied += 1
    assert numFilesCopied == snapshot

def test_getIncludeFileText(snapshot):
    inputFiles = ssri.getListOfFilesToSearchDir("testFolder/staging", ["testFolder/sites"], True, False)
    fileCreatedCounter = 0
    for fileSearchIndex in range(len(inputFiles[0])):
        ssri.copyFilesToNewLocation(inputFiles[1][fileSearchIndex], inputFiles[0][fileSearchIndex])
    checkIncludes = ssri.checkFilesForIncludes(inputFiles[0], "testFolder/templates", 0, False, 0)
    assert checkIncludes == snapshot


def test_checkFiles(snapshot):
    inputFiles = ssri.getListOfFilesToSearchDir("tests/testFolder/staging", ["tests/testFolder/sites"], True, False)
    knownGoodFiles = ssri.getListOfFilesToSearchDir("tests/testFolder/staging", ["tests/testFolder/sites"], True, False) # This is me being lazy and using getListOfFiles to get an array for the known good copy of sites
    fileCreatedCounter = 0
    for fileSearchIndex in range(len(inputFiles[0])):
        ssri.copyFilesToNewLocation(inputFiles[1][fileSearchIndex], inputFiles[0][fileSearchIndex])
    checkIncludes = ssri.checkFilesForIncludes(inputFiles[0], "tests/testFolder/templates", 0, False, 0)
    for template in checkIncludes[0].items():
        ssri.writeTextToFiles(template[0], template[1], True)
    arrayOfMatchesOfNot = []    # an array that will be filled with the output of filecmp
    list1 = sorted(inputFiles[1])
    list2 = sorted(knownGoodFiles[1])
    for filesToCompare in zip(list1, list2):
        sitesFile, knownGoodFile = tuple(filesToCompare)
        arrayOfMatchesOfNot.append(filecmp.cmp(sitesFile, knownGoodFile, shallow=False))
    assert arrayOfMatchesOfNot == snapshot


def test_copyAllFiles(snapshot):
    if(os.path.exists("tests/testFolder/blankDir")):
        if os.path.isfile("tests/testFolder/blankDir"):
            os.remove("tests/testFolder/blankDir")
        else:
            shutil.rmtree("tests/testFolder/blankDir")
    ssri.copyAllFiles("tests/testFolder/staging","tests/testFolder/blankDir")
    outputCheck = []
    for root, dirs, files in os.walk("tests/testFolder/blankDir"): # Gratefully borrowed from here https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
        level = root.replace("tests/testFolder/blankDir", '').count(os.sep) # As dir structure is important to track if it changes in this test so formatting the output makes sense
        indent = 'a' * (level)
        outputCheck.append(('{}{}/'.format(indent, os.path.basename(root))))
        subindent = 'z'* (level + 1)
        for f in files:
            outputCheck.append(('{}{}'.format(subindent, f)))
    shutil.rmtree("tests/testFolder/blankDir")
    assert sorted(outputCheck) == snapshot # For some reason Arch and Debian seem to sort files differently idk

#     inputFiles = ssri.getListOfFilesToSearchDir("tests/testFolder/staging", ["tests/testFolder/sites"], True, False)
#     knownGoodFiles = ssri.getListOfFilesToSearchDir("tests/testFolder/staging", ["tests/testFolder/sites"], True, False) # This is me being lazy and using getListOfFiles to get an array for the known good copy of sites
#     fileCreatedCounter = 0
#     for fileSearchIndex in range(len(inputFiles[0])):
#         ssri.copyFilesToNewLocation(inputFiles[1][fileSearchIndex], inputFiles[0][fileSearchIndex])
#     checkIncludes = ssri.checkFilesForIncludes(inputFiles[0], "tests/testFolder/templates", 0, False, 0)
#     for template in checkIncludes[0].items():
#         ssri.writeTextToFiles(template[0], template[1], True)
#     arrayOfMatchesOfNot = []    # an array that will be filled with the output of filecmp
#     for filesToCompare in zip(inputFiles[1],knownGoodFiles[1]):
#         sitesFile, knownGoodFile = tuple(filesToCompare)
#         arrayOfMatchesOfNot.append(filecmp.cmp(sitesFile, knownGoodFile, shallow=False))
#     assert arrayOfMatchesOfNot == snapshot
