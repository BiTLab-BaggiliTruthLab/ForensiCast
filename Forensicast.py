# Nicholas Dubois
import subprocess
import sys
import os
import csv
import re
import os.path
from os import path
import shutil
from datetime import datetime


def main():
    intro()
    num = int(input(">>> "))
    switch_main(num)

# Print Ascii Art
def ASCII():
    print("    ______                           _                 __")
    print("   / ____/___  ________  ____  _____(_)________ ______/ /_")
    print("  / /_  / __ \/ ___/ _ \/ __ \/ ___/ / ___/ __ `/ ___/ __/")
    print(" / __/ / /_/ / /  /  __/ / / (__  ) / /__/ /_/ (__  ) /_  ")
    print("/_/    \____/_/   \___/_/ /_/____/_/\___/\__,_/____/\__/  \n")

# Print Main Menu
def intro():
    ASCII()
    listDevices()
    print("1) Create Full Timeline")
    print("2) Create Fuzzy Timeline")
    print("3) Create Partial Timeline")
    print("4) Dump All Recoverable Data")
    print("5) Backup All")
    print("6) Backup Package")
    print("7) List Installed Applications")
    print("8) List All Packages")
    print("9) Install APK\n")

# Main Menu Switch Statement
def switch_main(arg):
    if arg == 1:
        fullTimeline("Artifacts.csv")
    elif arg == 2:
        fuzzyTimeline()
    elif arg == 3:
        partialTimeline()
    elif arg == 4:
        dumpAll()
    elif arg == 5:
        backupAll()
    elif arg == 6:
        backupPackage()
    elif arg == 7:
        listApps()
    elif arg == 8:
        listPackages()
    elif arg == 9:
        installAPK()
    else:
        print("ERROR, Restarting")
    main()

def testTimeline(artifact_csv):
    get_artifact_data = get_artifact_path(artifact_csv)
    collected_artifacts = []
    for artifact in get_artifact_data:
        if path.isfile("TEMPBackup/apps/" + artifact[1]):
            with open("TEMPBackup/apps/" + artifact[1], 'r', errors="ignore") as f:
                string = f.read()
                match = re.findall(artifact[3], string)
                collected_artifacts.append((artifact[0], artifact[2], match))
    for artifact in collected_artifacts:
        print(artifact)

# Create Timeline With All KNOWN/VERIFIABLE Data
def fullTimeline(artifact_csv):
    print("Prompt To Backup On Chromecast:")
    try:
        subprocess.run(["adb backup -apk -shared -all -f TEMPBackup.ab"], shell=True, check=True)
    except subprocess.CalledProcessError:
        print('ERROR')
        sys.exit(1)

    # Extracts Backup File With Android Backup Extractor JAR
    try:
        subprocess.run(["java -jar abe.jar unpack TEMPBackup.ab TEMPBackup.tar"], shell=True, check=True)
        subprocess.run(["mkdir -p 'TEMPBackup' && tar -xf TEMPBackup.tar -C TEMPBackup/"], shell=True, check=True)
    except subprocess.CalledProcessError:
        print('ERROR')
        sys.exit(1)

    os.remove("TEMPBackup.ab")
    os.remove("TEMPBackup.tar")
    print("Packages Backed Up To Backup Directory!\n")
    get_artifact_data = get_artifact_path(artifact_csv)
    collected_artifacts = []
    for artifact in get_artifact_data:
        if path.isfile("TEMPBackup/apps/" + artifact[1]):
            with open("TEMPBackup/apps/" + artifact[1], 'r', errors="ignore") as f:
                string = f.read()
                match = re.findall(artifact[3], string)
                collected_artifacts.append((artifact[0], artifact[2], match))
    printTimeline(collected_artifacts)
    shutil.rmtree('TEMPBackup')

def printTimeline(collected_artifacts):
    for artifact in collected_artifacts:

        if(artifact[1]=="Installation Timestamp"):
            print(artifact[0] + " - Application Install Time == ")
            for time in artifact[2]:
                print (unix2ust(time))
            print("\n")

        if (artifact[1] == "Initial Run Timestamp"):
            print(artifact[0] + " - Initial Application Run Time == ")
            for time in artifact[2]:
                print(unix2ust(time))
            print("\n")

        if(artifact[1]=="Last Run Timestamp"):
            print(artifact[0] + " - Application Last Run Time == ")
            for time in artifact[2]:
                print(unix2ust(time))
            print("\n")

        if(artifact[1]=="Last Close Timestamp"):
            print(artifact[0] + " - Application Last Closed Time == ")
            for time in artifact[2]:
                print (unix2ust(time))
            print("\n")

        if(artifact[1]=="Last Pause Timestamp"):
            print(artifact[0] + " - Application Last Paused Time == ")
            for time in artifact[2]:
                print (unix2ust(time))
            print("\n")

        if(artifact[1]=="Links Visited"):
            print(artifact[0] + " - Links User Visited == { ")
            for link in artifact[2]:
                print(link)
            print("}\n")

        if (artifact[1] == "Links Visited + Timestamp"):
            print(artifact[0] + " - Links User Visited == { ")
            for link in artifact[2]:
                print(link)
            print("}\n")

        if (artifact[1] == "Backend Links Visited"):
            print(artifact[0] + " - Backend Links Visited == {")
            for link in artifact[2]:
                print(link)
            print("}\n")

        if (artifact[1] == "Site Headers"):
            print(artifact[0] + " - Visited Site Headers == {")
            for link in artifact[2]:
                print(link)
            print("}\n")

        if(artifact[1]=="User Email"):
            print(artifact[0] + " - User Email(s) == ")
            printartifacts=removeDuplicates(artifact[2])
            for email in printartifacts:
                print(email)
            print("\n")

        if (artifact[1] == "User Login Timestamp"):
            print(artifact[0] + " - User Login Time == ")
            printartifacts = removeDuplicates(artifact[2])
            for time in printartifacts:
                print(unix2ust(time))
            print("\n")

        if (artifact[1] == "Saved Messages"):
            print(artifact[0] + " - Saved Application Messages == {")
            printartifacts = removeDuplicates(artifact[2])
            for message in printartifacts:
                print(message)
            print("}\n")

        if (artifact[1] == "Accound ID"):
            print(artifact[0] + " - Application Account ID == ")
            printartifacts = removeDuplicates(artifact[2])
            for ID in printartifacts:
                print(ID)
            print("\n")

        if (artifact[1] == "Username"):
            print(artifact[0] + " - Application Username(s) == ")
            printartifacts = removeDuplicates(artifact[2])
            for users in printartifacts:
                print(users)
            print("\n")

        if (artifact[1] == "Remote Mac Addr"):
            print(artifact[0] + " - Remote Mac Address == ")
            printartifacts = removeDuplicates(artifact[2])
            for mac in printartifacts:
                print(mac)
            print("\n")

    input("Press Enter To Continue")

def get_artifact_path(file):
    artifact_struct = []
    with open(file, newline='') as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            artifact_struct.append((row['appname'], row["path"], row['type'],  row['regex']))
        return artifact_struct

# Create Timeline With All Patterns And Potential Data
def fuzzyTimeline():
    print("test2")

# Create Timeline Based On Given Start/End Time With All KNOWN/VERIFIABLE Data
def partialTimeline():
    print("test3")

# Backup And Extract To Backup/ Folder
def dumpAll():
    print("Prompt To Backup On Chromecast:")
    try:
        subprocess.run(["adb backup -apk -shared -all -f TEMPBackup.ab"], shell=True, check=True)
    except subprocess.CalledProcessError:
        print('ERROR')
        sys.exit(1)

    # Extracts Backup File With Android Backup Extractor JAR
    try:
        subprocess.run(["java -jar abe.jar unpack TEMPBackup.ab TEMPBackup.tar"], shell=True, check=True)
        subprocess.run(["mkdir -p 'Backup' && tar -xf TEMPBackup.tar -C Backup/"], shell=True, check=True)
    except subprocess.CalledProcessError:
        print('ERROR')
        sys.exit(1)

    os.remove("TEMPBackup.ab")
    os.remove("TEMPBackup.tar")
    print("Packages Backed Up To Backup Directory!")
    input("Press Enter To Continue")

def unix2ust(inp):
    regex = re.compile('[1234567890]{10,14}')
    date = regex.findall(str(inp))
    if len(date[0]) == 10:
        ts = int(date[0])
    elif len(date[0]) == 11:
        ts = int(date[0])
        ts /= 10
    elif len(date[0]) == 12:
        ts = int(date[0])
        ts /= 100
    elif len(date[0]) == 13:
        ts = int(date[0])
        ts /= 1000
    elif len(date[0]) == 14:
        ts = int(date[0])
        ts /= 10000
    else:
        return "Unknown timestamp, unable to convert."
    return datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

# Backup Device Backups, Does Not Extract
def backupAll():
    print("Prompt To Backup On Chromecast:")
    try:
        subprocess.run(["adb backup -apk -shared -all -f FullBackup.ab"], shell=True, check=True)
    except subprocess.CalledProcessError:
        print('ERROR')
        sys.exit(1)

    print("Packages Backed Up To FullBackup.ab!")
    input("Press Enter To Continue")

# Backup Specific Package, Does Not Extract
def backupPackage():
    package = input("Package Name (com.xxx.xxx): ")
    try:
        subprocess.run(["adb backup -f " + package + ".ab " + package], shell=True, check=True)
    except subprocess.CalledProcessError:
        print('ERROR')
        sys.exit(1)

    print("Packages Backed Up To " + package + ".ab!")
    input("Press Enter To Continue")

# List All Packages
def listPackages():
    try:
        subprocess.run(["adb shell pm list packages"], shell=True, check=True)
    except subprocess.CalledProcessError:
        print('ERROR')
        sys.exit(1)

    input("Press Enter To Continue")

# List All Packages And Try To Extract App Names From Them
def listApps():
    try:
        Packages = subprocess.run(["adb shell pm list packages"], shell=True, stdout=subprocess.PIPE).stdout.decode(
            'utf-8').replace('package:', '').split()
    except subprocess.CalledProcessError:
        print('ERROR')
        sys.exit(1)

    print("Prompt To Backup On Chromecast:")
    try:
        subprocess.run(["adb backup -apk -shared -all -f TEMPBackup.ab"], shell=True, check=True)
    except subprocess.CalledProcessError:
        print('ERROR')
        sys.exit(1)

    # Extracts Backup File With Android Backup Extractor JAR
    try:
        subprocess.run(["java -jar abe.jar unpack TEMPBackup.ab TEMPBackup.tar"], shell=True, check=True)
        subprocess.run(["mkdir -p 'TEMPBackup' && tar -xf TEMPBackup.tar -C TEMPBackup/"], shell=True, check=True)
    except subprocess.CalledProcessError:
        print('ERROR')
        sys.exit(1)

    os.remove("TEMPBackup.ab")
    os.remove("TEMPBackup.tar")

    for line in Packages:
        apkPath = "TEMPBackup/apps/" + line + "/a/base.apk"

        try:
            appLabel = subprocess.run(
                ["aapt d badging " + apkPath + " | grep \"application: label\" | awk '{print $2}'"], shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.decode('utf-8').replace('label=', '').replace(
                '\'', '')
        except subprocess.CalledProcessError:
            print('ERROR')

        if (appLabel == ""):
            appLabel = "N/A"
        line = (line + " == " + appLabel).rstrip()
        print(line)
    shutil.rmtree('TEMPBackup')

    input("Press Enter To Continue")

# Install APK File To Device
def installAPK():
    package = input("Path To Package: ")
    try:
        subprocess.run(["adb install " + package], shell=True, check=True)
    except subprocess.CalledProcessError:
        print('File Not Found Or Not Formatted As APK')
        sys.exit(1)
    print("Package Installed!")
    input("Press Enter To Continue")

# List Attached Devices
def listDevices():
    try:
        subprocess.run(["adb devices"], shell=True, check=True)
    except subprocess.CalledProcessError:
        print('ADB May Not Be Installed, Install ADB and Run Again')
        sys.exit(1)

def removeDuplicates(lst):
    return list(set([i for i in lst]))

if __name__ == "__main__":
    main()