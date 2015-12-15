#!/usr/bin/python
# Filename:delblankline.py
# -*- coding: utf-8 -*-
import sys
import os
def delblankline(infile):
    """ Delete blanklines of infile """
    infp = open(infile, "r")
    outfp = open("tmp_" + infile, "w")
    lines = infp.readlines()
    for li in lines:
        if li.split():
            outfp.writelines(li)
            
    infp.close()
    outfp.close()
    current_path = os.getcwd()
    os.remove(current_path + os.sep + infile)
    os.rename(current_path+ os.sep + "tmp_" + infile,current_path + os.sep + infile)
if __name__ == "__main__":
    delblankline(sys.argv[1])