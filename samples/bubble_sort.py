#!/usr/bin/python
###########################################################################
# FILE      : mysort.py
# SUBJECT   : Sort the lines of the text file at the standard input.
# PROGRAMMER: (C) Copyright 2002 by Peter Chapin
#
# The program below implements the bubble sort algorithm. Note that it uses list indicies as
# "pointers" into the list and thus tries to randomly access the list with the [] operator. If
# the [] operator is O(n) on lists this code will be even slower than usual for bubble sort.
#
# To do:
#
# + Implement a better sorting algorithm.
#
# + Look into using iterator objects for accessing the sequence (STL-like).
#
# Please send comments or bug reports to
#
#      Peter Chapin
#      Computer Information Systems
#      Vermont Technical College
#      Williston, VT 05495
#      PChapin@vtc.vsc.edu
###########################################################################

import sys

# Get the input
text = sys.stdin.readlines()
size = len(text)

# The following implements a bubble sort.
while 1:
    p1 = 0
    p2 = 1
    switched = False
    while p2 < size:
        if text[p2] < text[p1]:
            temp     = text[p1]
            text[p1] = text[p2]
            text[p2] = temp
            switched = True
        p1 += 1
        p2 += 1
    if not switched: break

# Print the output
for line in text: print(line, end=''),

