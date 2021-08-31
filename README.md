![](https://github.com/unhcfreg/ForensiCast/blob/main/Forensicast%20Banner.png)

# Forensicast

The Google Chromecast with Google TV (Chromecast TV) is a standalone streaming device produced by Google. Forensicast is a tool to aquire, discover, and present artifacts for the Chromecast with Google TV IOT device as well as any other Android-enabled device with developer mode capabilities.

As of now this tool only runs on Linux operating systems. (As it makes use of Linux system command calls)

This work has been funded under the Office of Naval Research Grant #N00014-20-1-2296

## Prerequestites

[ADB - Android Debug Bridge](https://developer.android.com/studio/command-line/adb)

[AAPT - Android Asset Packaging Tool](https://developer.android.com/studio/command-line/aapt2)

[Java](https://www.java.com/en/download/help/linux_x64_install.html)

`sudo apt install aapt adb`

## Operation
Forensicast makes use of regex and specified paths in the `/Artifacts.csv` file. To add your own artifacts, create a new line and input the artifact in [appname, type, path, regex] format. Type variants perform specified functions. (Eg. 'Timestamp' artifacts will accept a UNIX timestamp and convert it to UST) 

Type variants include ["Installation Timestamp", "Initial Run Timestamp", "Last Run Timestamp", "Last Close Timestamp", "Last Pause Timestamp", "Links Visited", "Links Visited + Timestamp", "Backend Links Visited", "Site Headers", "User Email", "User Login Timestamp", "Saved Messages", "Account ID", "Username", "Remote Mac Addr"]

![](https://github.com/unhcfreg/ForensiCast/blob/main/Forensicast%20Demo.png)

`sudo python3 Forensicast.py`

 1 : Create Full Timeline - Create a list of every known verifiable artifact.

 2 : Dump All Recoverable Data - Backup and extract all recoverable data to a "Backup/" folder.

 3 : Backup All - Perform a full ADB backup of all applications.

 4 : Backup Package - Backup a singular specified package.

 5 : List Installed Applications - Output a list of intalled packages and extract application names when possible.

 6 : List All Packages - Output a list of installed packages, both system and third party.

 7 : Install APK - Manually install an Android application.


## Authors

Forensicast - [@nootsploit](https://twitter.com/nootsploit)

[Full Research Paper](https://dl.acm.org/doi/abs/10.1145/3465481.3470060) - Presented at The International Conference on Availability, Reliability and Security (ARES) - [@nootsploit](https://twitter.com/nootsploit) [@sciclone19841](https://twitter.com/sciclone19841)
