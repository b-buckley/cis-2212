#!/usr/bin/python
###########################################################################
# FILE      : ftoc.py
# SUBJECT   : Program to print temperature conversion table.
# PROGRAMMER: (C) Copyright 2002 by Peter Chapin
#
# This program prints out a F -> C temperature conversion table. It accepts as input the bounds
# of the table and the step size between table rows. It allows for both increasing and
# decreasing ranges (use a negative step for a decreasing range).
#
# To do:
#
# + Need to add the ability to get input parameters from the command line.
#
# + The duplication of the while loops at the bottom seems bad. Is there a good, Python way of
#   dealing with that? I'm thinking about creating a function object that handles the condition.
#   I could create the function object two different ways depending on the input range.
#
# + It might be neat to make the precision of the output a command line option as well. I'd have
#   to dynamically construct the format string. That shouldn't be a problem.
#
# Please send comments or bug reports to
#
#      Peter Chapin
#      Computer Information Systems
#      Vermont Technical College
#      Williston, VT 05495
#      pchapin@vtc.edu
###########################################################################

import sys

# Get the bounds and the step size. Need option to do this from command line.
print('First bound?', end=' ')
first = float(sys.stdin.readline())
print('Second bound?', end=' ')
second = float(sys.stdin.readline())
print('Step size?', end=' ')
step = float(sys.stdin.readline())

# Validate the input.
# Note that I'm allowing both increasing and decreasing steps.
if step >= 0 and first >= second:
    print('Invalid bounds')
    sys.exit(1)

if step <= 0 and first <= second:
    print('Invalid bounds')
    sys.exit(1)

# Initialize the table.
print()
print('     F       C')
print('======  ======')
degrees_f = first

# Compute the table. Is there a clean way to eliminate the duplication?
if step > 0:
    while degrees_f <= second:
        degrees_c = 5.0 * (degrees_f - 32.0) / 9.0
        print('%6.2f  %6.2f' % (degrees_f, degrees_c))
        degrees_f += step
else:
    while degrees_f >= second:
        degrees_c = 5.0 * (degrees_f - 32.0) / 9.0
        print('%6.2f  %6.2f' % (degrees_f, degrees_c))
        degrees_f += step
