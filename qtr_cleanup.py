#!/usr/bin/python
# Qtractor project directory clean-up utility v0.1
# Written by Efenstor
# License: GPLv3

import sys
import os
from lxml import etree

# SEND2TRASH
# To move files to trash instead of deletion download and install Send2Trash
# from https://github.com/hsoft/send2trash or do "pip install Send2Trash",
# after that set "send2trash = True" in the line below
send2trash = True
if send2trash:
  from send2trash import send2trash

# CHANGE THESE IF NEEDED
midi_ext = ".mid"
wave_ext = ".wav"
peak_ext = ".peak"

# Display some help
print("\nQtractor project directory clean-up utility v0.1\n")
print("Usage: [python] folder_cleanup.py <FILENAME>")
print("Where: FILENAME = Qtractor project file name\n")
print("All MIDI, wave, peak and curve files referred in the project will be")
print("ignored, all the other such files in the project directory will be")
print("deleted.\n")

if not send2trash:
  print("WARNING: all files will be deleted permanently! If you want to move them")
  print("to trash instead, download and enable Send2Trash (see inside folder_cleanup.py")
  print("for instructions)\n")

if len(sys.argv) < 2:
  print("Please provide a project file name.\n")
  sys.exit()

if not os.path.isfile(sys.argv[1]):
  # Not exists or not a file
  print("\""+sys.argv[1]+"\" project file does not exist or not a file.\n")
  sys.exit()

# Open the file
srcFile = open(sys.argv[1])
tree = etree.parse(srcFile)

# Get the base elements
properties = tree.find("properties")
directory = properties.find("directory")
print("Project directory: \""+directory.text+"\"")
files = tree.find("files")
audioList = files.find("audio-list")
audioFiles = audioList.findall("file")
midiList = files.find("midi-list")
midiFiles = midiList.findall("file")

# Make the curve file list
curveFiles = []
tracks = tree.find("tracks")
for t in tracks.findall("track"):
  curveFile = t.find("curve-file")
  if curveFile is not None:
    curveFilename = curveFile.find("filename")
    curveFiles.append(curveFilename.text)

# List through the files
dirlist = os.listdir(directory.text)
for f in dirlist:
  fabs = os.path.abspath(f)
  path,fname = os.path.split(fabs)
  name,ext = os.path.splitext(fname)
  found = 0
  if ext == midi_ext:
    found = 1
    # It's a MIDI file, search in the MIDI file list
    for mf in midiFiles:
      if mf.text == fname:
        found = 2
        break
    # Also search in the curve file list
    for cf in curveFiles:
      if cf == fname:
        found = 2
        break
  elif ext == wave_ext:
    found = 1
    # It's an audio file, search in the audio file list
    for af in audioFiles:
      if af.text == fname:
        found = 2
        break
  elif ext == peak_ext:
    found = 1
    # It's a peak file, search in the audio file list
    bname,bext = os.path.splitext(name)
    for af in audioFiles:
      if af.text == bname+wave_ext:
        found = 2
        break

  # Delete or ignore
  if found == 1:
    print("DELETING \""+f+"\"")
    if send2trash:
      send2trash(fabs)
    else:
      os.remove(fabs)
  elif found == 2:
    print("IGNORING \""+f+"\"")

print("Done!\n")

