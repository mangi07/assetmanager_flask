# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 09:32:59 2018

@author: Ben.Olson
"""

import hashlib
import sys
import os

try:
    filepath = sys.argv[1]
    filename, file_extension = os.path.splitext(filepath)

    BLOCKSIZE = 65536

    hasher = hashlib.md5()
    
    with open(filepath, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    
    # rename file
    directory = os.path.dirname(filepath)
    newfilename = hasher.hexdigest() + file_extension
    newpath = os.path.join(directory, newfilename)
    os.rename(filepath, newpath)
    print("New file name: ", newpath)

except:
    print("\nERROR: Fully-qualified file path needed.\nIf you already tried, try again and surround the path with quotes.\n")
    