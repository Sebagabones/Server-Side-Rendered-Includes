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
    listFiles = ssri.getListOfFilesToSearchDir("testFolder", ["outputLocation"], False, False )
    assert listFiles == snapshot
