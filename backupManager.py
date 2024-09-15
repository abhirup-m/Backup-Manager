#!/bin/python
# Script to manage dotfiles

import json
import os
import subprocess
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
colorama_init()

# read json file that lists all dotfiles that must be tracked.
BACKUP_DATA = json.load(open("sources.json"))
BACKUP_FOLDER = "/home/storage/backupManager/backup/"

groups = BACKUP_DATA.keys()

if "dotfiles" in groups:
    gitRepos = {}
    backedUp = []
    # create folder for copying all dotfiles into
    if not os.path.exists(BACKUP_FOLDER):
        os.mkdir(BACKUP_FOLDER)
    for path in BACKUP_DATA["dotfiles"]:
        if not os.path.isdir(os.path.join(path, ".git")):
            subprocess.run(["cp", "-rf", path, BACKUP_FOLDER])
            backedUp.append(path)
        else:
            gitRepos[path] = subprocess.run(["git", "remote", "get-url", "origin"], cwd=path, capture_output=True, text=True).stdout.strip()
    print(f"{Fore.YELLOW}Backed up following folders:{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{"\t\t".join(backedUp)}{Style.RESET_ALL}\n")
    print(f"{Fore.RED}Not tracking the following git repositories.{Style.RESET_ALL}")
    print ("\n".join([f"{Fore.YELLOW}{k}  -->  {Fore.BLUE}{v}{Style.RESET_ALL}" for k,v in gitRepos.items()]), "\n")
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
    print(f"{Fore.YELLOW}Backed up following system files:{Style.RESET_ALL}")
    print(f"{Fore.BLUE}{"\n".join(BACKUP_DATA["system-files"])}{Style.RESET_ALL}\n")
themingBackup = {}
if "themes" in groups:
    if not os.path.exists(BACKUP_FOLDER):
        os.mkdir(BACKUP_FOLDER)
    themes = "\n".join(os.listdir(BACKUP_DATA["themes"]))
    themingBackup["Gtk themes"] = "\t".join(os.listdir(BACKUP_DATA["themes"]))
    with open(os.path.join(BACKUP_FOLDER, "gtkThemes.txt"), "w") as file:
        file.write(themes)
if "icons" in groups:
    if not os.path.exists(BACKUP_FOLDER):
        os.mkdir(BACKUP_FOLDER)
    icons = "\n".join(os.listdir(BACKUP_DATA["icons"]))
    themingBackup["Icon themes"] = "\t".join(os.listdir(BACKUP_DATA["icons"]))
    with open(os.path.join(BACKUP_FOLDER, "iconThemes.txt"), "w") as file:
        file.write(icons)
if "fonts" in groups:
    if not os.path.exists(BACKUP_FOLDER):
        os.mkdir(BACKUP_FOLDER)
    fonts = "\n".join(os.listdir(BACKUP_DATA["fonts"]))
    themingBackup["Fonts"] = "\t".join(os.listdir(BACKUP_DATA["fonts"]))
    with open(os.path.join(BACKUP_FOLDER, "fonts.txt"), "w") as file:
        file.write(fonts)
print(f"{Fore.YELLOW}Backed up the following theme-related stuff:{Style.RESET_ALL}")
print ("\n".join([f"{Fore.YELLOW}{k}  -->  {Fore.BLUE}{v}{Style.RESET_ALL}" for k,v in themingBackup.items()]), "\n")
if "packages" in groups:
    if not os.path.exists(BACKUP_FOLDER):
        os.mkdir(BACKUP_FOLDER)
    packages = subprocess.run(BACKUP_DATA["packages"].split(" "), capture_output=True, text=True).stdout
    with open(os.path.join(BACKUP_FOLDER, "packages.txt"), "w") as file:
        file.write(packages)
print(f"{Fore.YELLOW}Backed up system packages.{Style.RESET_ALL}\n")
if "conda" in groups:
    if not os.path.exists(BACKUP_FOLDER):
        os.mkdir(BACKUP_FOLDER)
    subprocess.run([BACKUP_DATA["conda"], "export", "--file", os.path.join(BACKUP_FOLDER, "conda.yml")])
print(f"{Fore.YELLOW}Backed up conda packages.{Style.RESET_ALL}")
