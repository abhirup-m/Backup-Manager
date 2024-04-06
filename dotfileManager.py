#!/bin/python
# Script to manage dotfiles
import sys
import json
import os
import shutil
import subprocess

# read json file that lists all dotfiles that must be tracked.
objectList = json.load(open(sys.argv[1]))

# parse the json to create two lists, one for the full paths and one for the basenames.
# the basenames must be listed in order to look for conflicts, since they will all be
# dumped into a single folder, irrespective of their full source paths.
baseNames = []
objectPaths = []
for folder, objects in objectList.items():
    for obj in objects:
        objectPath = os.path.expanduser(os.path.join(folder, obj))

        # append to our lists only if the path exists on the file system.
        if os.path.exists(objectPath):
            objectPaths.append(objectPath)
            baseNames.append(obj)
        else:
            print("{} does not exist, skipping it.".format(objectPath))

# check if all basenames are unique.
if len(set(baseNames)) != len(baseNames):
    print("There are objects with conflicting basenames.")

# go over the entire list to filter out duplicates.
for i, (baseName, objectPath) in enumerate(zip(baseNames[1:], objectPaths[1:])):

    # found a duplicate.
    if baseName in baseNames[:i+1]:
        print("Multiple instances of {}. Considering only the first.".format(baseName))
        objectPaths.pop(i+1)

# create folder for copying all dotfiles into
dotfilesFolderPath = os.path.expanduser(os.path.join(".", "dotfilesFolder"))
if not os.path.exists(dotfilesFolderPath):
    os.mkdir(dotfilesFolderPath)

# copy all uniquely named dotfiles
for (baseName, objectPath) in zip(baseNames, objectPaths):
    shutil.copy2(objectPath, os.path.join(dotfilesFolderPath, baseName))
