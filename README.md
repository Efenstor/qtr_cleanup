# qtr_cleanup
### Qtractor project directory clean-up utility

It is a small Python utility that deletes all MIDI, wave, peak and curve files unreferred in a Qtractor project file from its directory, as far as this functionality is currently missing in the Qtractor itself.

The Cleanup option in the file list context menu only cleans up the project itself of redundant references, while the project directory actually remains full of junk files.

### Usage
**[python] folder_cleanup.py \<FILENAME\>**

*Where: FILENAME = Qtractor project file name*

All MIDI, wave, peak and curve files referred in the project will be ignored, all the other such files in the project directory will be deleted.

### Move to trash

There is a special *send2trash* variable defined at the beginning of the file, when set to *False* (default), all files will be deleted permanently, if set to *True* they will be moved to trash. Unfortunately this functionality doesn't work out of the box, you will need to download and install the *send2trash* library: https://github.com/hsoft/send2trash or just do *pip install Send2Trash*
