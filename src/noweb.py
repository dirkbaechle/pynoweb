#!/usr/bin/env python
# coding: latin-1
#
# Copyright (c) 2009 Dirk Baechle.
# www: http://www.mydarc.de/dl9obn/programming/python/pynoweb
# mail: dl9obn AT darc.de
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
#
# Based on an idea by Jonathan Aquino (jonathan.aquino@gmail.com)
#
# This program extracts code from a literate programming document in "noweb" format.
# For more information, including the original source code and documentation,
# see http://jonaquino.blogspot.com/2010/04/nowebpy-or-worlds-first-executable-blog.html
#
# Additional refactorings and modifications by Dirk Baechle:
#
#  - You can now say <<file:included.txt>>, which reads in "include.txt"
#    while parsing the noweb file(s). This can be done recursively and helps to
#    organize long files (like shell scripts) in smaller pieces.
#

import sys,re

OPEN = "<<"
CLOSE = ">>"

def expand(chunkName, chunks, indent):
    chunkLines = chunks[chunkName]
    expandedChunkLines = []
    for line in chunkLines:
        match = re.match("(\s*)" + OPEN + "([^>]+)" + CLOSE + "\s*$", line)
        if match:
            expandedChunkLines.extend(expand(match.group(2), chunks, indent + match.group(1)))
        else:
            expandedChunkLines.append(indent + line)
    return expandedChunkLines

def parseFile(filename, chunks):
    file = open(filename)
    chunkName = None
    for line in file.readlines():
        line = line.rstrip('\n')
        filematch = re.match(OPEN + "file:([^>]+)" + CLOSE, line)
        match = re.match(OPEN + "([^>]+)" + CLOSE + "=", line)
        if filematch:
            parseFile(filematch.group(1), chunks)
        elif match:
            chunkName = match.group(1)
            chunks[chunkName] = []
        else:
            match = re.match("@", line)
            if match:
                chunkName = None
            elif chunkName:
                chunks[chunkName].append(line)
    file.close()

def expandFile(filename, chunks, outputChunkName):
    parseFile(filename, chunks)

    return expand(outputChunkName, chunks, "")

def usage():
    print "noweb.py -Routchunk infile > outfile"

def main():
    if len(sys.argv) < 3:
        usage()
        
    chunks = {}
    for l in expandFile(sys.argv[-1], chunks, sys.argv[-2][2:]):
        print l
    
if __name__ == "__main__":
    main()
