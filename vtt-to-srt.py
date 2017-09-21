#!/usr/bin/python
# -*- coding: utf-8 -*-
# ---------------------------------------
# vtt-to-srt.py
# (c) Jansen A. Simanullang
# 02.04.2016 13:39
# LAST CHANGE:
# 02.04.2016 16:56
# recursively visit subdirectories
# ---------------------------------------
# usage: python vtt-to-srt.py
#
# example:
# python vtt-to-srt.py
#
# features:
# check a directory and all its subdirectories
# convert all vtt files to srt subtitle format
#
# real world needs:
# converting Coursera's vtt subtitle


import os
import re
import sys
from stat import ST_MODE, S_ISDIR, S_ISREG


def convertContent(fileContents):

    # replase '.' for ',' in timecode
    replacement = re.sub(r'([\d]+)\.([\d]+)', r'\1,\2', fileContents)

    replacement = re.sub(r'^\d+\n', '', replacement)
    replacement = re.sub(r'\n\d+\n', '\n', replacement)

    timecode = re.compile(
            r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}')
    header_and_timecode = re.compile(
        r'^.*?(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})',
        re.DOTALL)

    # Delete header block and optional blocksgit 
    bodyContent = re.split(header_and_timecode, replacement, maxsplit=1)
    replacement = ('').join(bodyContent)

    # Add numeration before timecode
    for i, match in enumerate(re.finditer(timecode, replacement)):
        replacement = replacement.replace(
                match.group(), str(i+1)+'\n'+(match.group()))

    return replacement


def vtt_to_srt(vttNamaFile):

    with open(vttNamaFile, "r") as f:
        fileContents = f.read()
        print "file being read: " + vttNamaFile

    strData = convertContent(fileContents)

    strNamaFile = vttNamaFile.replace(".vtt", ".srt")
    with open(strNamaFile, "w") as fout:
        fout.write(strData)
        print "file created:    " + strNamaFile


def walktree(TopMostPath, callback):

    '''recursively descend the directory tree rooted at TopMostPath,
       calling the callback function for each regular file'''

    for f in os.listdir(TopMostPath):

        pathname = os.path.join(TopMostPath, f)
        mode = os.stat(pathname)[ST_MODE]

        if S_ISDIR(mode):
            # It's a directory, recurse into it
            walktree(pathname, callback)
        elif S_ISREG(mode):
            # It's a file, call the callback function
            callback(pathname)
        else:
            # Unknown file type, print a message
            print 'Skipping %s' % pathname


def convertVTTtoSRT(file):
    if '.vtt' in file:
        vtt_to_srt(file)


def main():
    # just edit the path below
    TopMostPath = '/home/duncan/Загрузки/srt'

    walktree(TopMostPath, convertVTTtoSRT)


if __name__ == '__main__':
    main()
