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

    # Delete header block and optional blocks
    head = ''
    lines = fileContents.split('\n')
    for line in lines:
        if not (line.strip()[:1].isdigit() and
                line.strip()[2] == ':' and
                line.strip()[3:4].isdigit() and
                line.strip()[5] == ':' and
                line.strip()[6:7].isdigit()):
            head += line + '\n'
        else:
            break
    replacement = fileContents.replace(head, '')

    # replase '.' for ',' in timecode
    replacement = re.sub(r'([\d]+)\.([\d]+)', r'\1,\2', replacement)
    replacement = re.sub(r'^\d+\n', '', replacement)
    replacement = re.sub(r'\n\d+\n', '\n', replacement)

    # add number before timecode
    res = replacement
    for i, match in enumerate(re.finditer(
            r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}',
            replacement)):
        res = res.replace(match.group(), str(i+1)+'\n'+(match.group()))
    return res


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
