#!/bin/python
# Script to manage dotfiles

import json
import os
import subprocess

# read json file that lists all dotfiles that must be tracked.
BACKUP_DATA = json.load(open("sources.json"))
BACKUP_FOLDER = "/home/storage/backupManager/backup/"

groups = BACKUP_DATA.keys()

if "dotfiles" in groups:
    gitRepos = {}
    # create folder for copying all dotfiles into
    if not os.path.exists(BACKUP_FOLDER):
        os.mkdir(BACKUP_FOLDER)
    for path in BACKUP_DATA["dotfiles"]:
        if not os.path.isdir(os.path.join(path, ".git")):
            subprocess.run(["cp", "-rf", path, BACKUP_FOLDER])
        else:
            gitRepos[path] = subprocess.run(["git", "remote", "-v"], cwd=path, capture_output=True, text=True).stdout.strip().split("\n")
    print("Not tracking the following git repositories.")
    print (json.dumps(gitRepos, indent=2, default=str))
    with open(os.path.join(BACKUP_FOLDER, "gitRepos.json"), 'w', encoding='utf-8') as file:
        json.dump(gitRepos, file, indent=4)

if "system-files" in groups:
    if not os.path.exists(BACKUP_FOLDER):
        os.mkdir(BACKUP_FOLDER)
    sysFilesFolder = os.path.join(BACKUP_FOLDER, "systemFiles/")
    if not os.path.exists(sysFilesFolder):
        os.mkdir(sysFilesFolder)
    for path in BACKUP_DATA["system-files"]:
        subprocess.run(["cp", "-f", path, BACKUP_FOLDER])
if "themes" in groups:
    if not os.path.exists(BACKUP_FOLDER):
        os.mkdir(BACKUP_FOLDER)
    themes = "\n".join(os.listdir(BACKUP_DATA["themes"]))
    with open(os.path.join(BACKUP_FOLDER, "gtkThemes.txt"), "w") as file:
        file.write(themes)
if "icons" in groups:
    if not os.path.exists(BACKUP_FOLDER):
        os.mkdir(BACKUP_FOLDER)
    icons = "\n".join(os.listdir(BACKUP_DATA["icons"]))
    with open(os.path.join(BACKUP_FOLDER, "iconThemes.txt"), "w") as file:
        file.write(icons)
if "fonts" in groups:
    if not os.path.exists(BACKUP_FOLDER):
        os.mkdir(BACKUP_FOLDER)
    fonts = "\n".join(os.listdir(BACKUP_DATA["fonts"]))
    with open(os.path.join(BACKUP_FOLDER, "fonts.txt"), "w") as file:
        file.write(fonts)
if "packages" in groups:
    if not os.path.exists(BACKUP_FOLDER):
        os.mkdir(BACKUP_FOLDER)
    packages = subprocess.run(BACKUP_DATA["packages"].split(" "), capture_output=True, text=True).stdout
    with open(os.path.join(BACKUP_FOLDER, "packages.txt"), "w") as file:
        file.write(packages)
if "conda" in groups:
    if not os.path.exists(BACKUP_FOLDER):
        os.mkdir(BACKUP_FOLDER)
    subprocess.run([BACKUP_DATA["conda"], "export", "--file", os.path.join(BACKUP_FOLDER, "conda.yml")])
