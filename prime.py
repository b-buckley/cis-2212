#!/usr/bin/python
"""
A prime number calculator

The program accepts an integer on the command line and prints a message specifying if that
integer is prime or not.
"""

import sys

if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "number")
    exit(1)

number = int(sys.argv[1])

n = number // 2
while n > 1:
    if number % n == 0:
        print(number, "=", n, "*", number // n)
        break
    n = n - 1
else:
    print(number, "is prime.")
