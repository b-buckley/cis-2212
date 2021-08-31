#!/usr/bin/python
###########################################################################
# FILE      : date.py
# SUBJECT   : A date class for Python
# PROGRAMMER: (C) Copyright 2007 by Peter C. Chapin
#
# Please send comments or bug reports to
#
#      Peter C. Chapin
#      Computer Information Systems
#      Vermont Technical College
#      Williston, VT 05495
#      PChapin@vtc.vsc.edu
###########################################################################

# I need this array kicking around.
month_lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

class date:

    # The constructor sets the date to the given date..
    def __init__(self, day, month, year):
        self.set(day, month, year)


    # Returns true if the year associated with this date is a leap year.
    def is_leap(self):
        result = 0
        if                (self.Y %   4) == 0: result = 1
        if     result and (self.Y % 100) == 0: result = 0
        if not result and (self.Y % 400) == 0: result = 1
        return result


    # Returns the number of days in the month associated with this date.
    def month_length(self):
        length = month_lengths[self.M - 1]
        if self.M == 2 and self.is_leap():
            length = length + 1

        return length


    # Sets the date object to the given date. Very useful.
    def set(self, day, month, year):

        # Set the members according to what we are given.
        self.D = day
        self.M = month
        self.Y = year

        # If we are given a year less than 100, convert it to four digits.
        if self.Y < 100:
            if self.Y < 50:
                self.Y = self.Y + 2000
            else:
                self.Y = self.Y + 1900 

        # Force a "reasonable" range.
        if self.Y < 1800: self.Y = 1800
        if self.Y > 2099: self.Y = 2099

        # Force a legal month.
        if self.M <  1: self.M = 1
        if self.M > 12: self.M = 12

        # Force a legal day.
        # This should take into account the length of each month.
        if self.D <  1: self.D = 1
        if self.D > 31: self.D = 31


    # Advance the date by one day.
    def next(self):
        self.D = self.D + 1
        if self.D > self.month_length():
            self.D = 1
            self.M = self.M + 1
            if self.M > 12:
                self.M = 1
                self.Y = self.Y + 1


    # Back up the date by one day.
    def previous(self):
        fix_day = 0

        self.D = self.D - 1
        if self.D < 1:
            fix_day = 1
            self.M = self.M - 1
            if self.M < 1:
                self.M = 12
                self.Y = self.Y - 1

        if fix_day: self.D = self.month_length()


    # Advance the date by the given number of days.
    def advance(self, delta):

        # If there is nothing to do, bail out.
        if delta == 0: return

        # Otherwise do real work.
        if delta > 0:
            for i in range(1, delta + 1):
                self.next()
        else:
            for i in range(1, -delta + 1):
                self.previous()


#
# This is the end of the class definition. What follows are normal functions.
#

# Returns -1 if d1 is before d2, 0 if d1 == d2, and +1 if d1 is after d2.
def compare(d1, d2):

    if d1.Y < d2.Y: return -1
    if d1.Y > d2.Y: return +1

    if d1.M < d2.M: return -1
    if d1.M > d2.M: return +1

    if d1.D < d2.D: return -1
    if d1.D > d2.D: return +1

    return 0


# Returns the number of days d1 is after d2
def difference(d1, d2):
    result = 0

    # What is their relationship?
    relation = compare(d1, d2)

    # Handle the simple case first.
    if relation == 0: return 0

    # Make copies. Is there a better way to do this?
    tempD1 = date(d1.D, d1.M, d1.Y)
    tempD2 = date(d2.D, d2.M, d2.Y)

    # Man, this is ugly!
    while compare(tempD1, tempD2) == 1:
        tempD2.next()
        result = result + 1

    while compare(tempD1, tempD2) == -1:
        tempD1.next()
        result = result - 1

    return result

# Test code.
if __name__ == "__main__":
    d = date(28, 2, 2000)
    d.next()
    print("%04d-%02d-%02d" % (d.Y, d.M, d.D))
