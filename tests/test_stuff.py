#!/usr/bin/env python3
import ssri
import sys


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
    listFiles = ssri.getListOfFilesToSearchDir("testFolder/staging", ["testFolder/sites"], True, False )
    assert listFiles == snapshot

def test_readfilesFile(snapshot):
    listFiles = ssri.getListOfFilesToSearchFiles(["testFolder/staging/emacsFiles.html"], ["testFolder/sites"], "testFolder/templates", False, 0, False)
    assert listFiles == snapshot

def test_checkCopyFiles(snapshot):
    inputFiles = ssri.getListOfFilesToSearchDir("testFolder/staging", ["testFolder/sites"], True, False)
    fileCreatedCounter = 0
    numFilesCopied = 0
    for fileSearchIndex in range(len(inputFiles[0])):
        numFilesCopied += ssri.copyFilesToNewLocation(inputFiles[1][fileSearchIndex], inputFiles[0][fileSearchIndex], fileCreatedCounter)
    assert numFilesCopied == snapshot


def test_checkFiles(snapshot):
    inputFiles = ssri.getListOfFilesToSearchDir("testFolder/staging", ["testFolder/sites"], True, False)
    fileCreatedCounter = 0
    for fileSearchIndex in range(len(inputFiles[0])):
        ssri.copyFilesToNewLocation(inputFiles[1][fileSearchIndex], inputFiles[0][fileSearchIndex], fileCreatedCounter)
    checkIncludes = []
    for files in inputFiles[1]:
        checkIncludes.append(ssri.checkFileForIncludes(files, "testFolder/templates", 0, False, 0))
    assert checkIncludes == snapshot
