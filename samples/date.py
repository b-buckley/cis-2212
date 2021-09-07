#!/usr/bin/python

month_lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# Instances of this class are raised when an invalid date would have be computed.
class InvalidDate(RuntimeError):
    def __init__(self, message):
        self.message = message

class Date:
    """A class for manipulating calendar dates

    Instances of this class represent dates between the years 1800 and 2099 (inclusive). Simple methods and supporting functions are provided to advance a date forward or backward, compare dates, and compute the difference between two dates.

    This class is intended to be primarly educational. Thus it may not illustrate all appropriate best practices (so as to avoid creating a class that is overwhelming to the newcomer). However, this class is continuously evolving and may become progressively more useful in the future. Note, however, that the Python library already contains modules for date manipulation that may be more appropriate to use in a real program.
    """

    # The constructor sets the date to the given date.
    def __init__(self, day: int, month: int, year: int ):
        self.set(day, month, year)


    def is_leap(self) -> bool:
        """Returns true if the year associated with this date is a leap year.
        
        This method implements the full leap year rules of the Gregorian calendar. It is necessary to do this because the year 2000, which is in the range of supported dates, requires all of the rules in order to be handled correctly.
        """
        result = False
        if                (self.Y %   4) == 0: result = True
        if     result and (self.Y % 100) == 0: result = False
        if not result and (self.Y % 400) == 0: result = True
        return result


    # Returns the number of days in the month associated with this date.
    def month_length(self) -> int:
        length = month_lengths[self.M - 1]
        if self.M == 2 and self.is_leap():
            length = length + 1
        return length


    def set(self, day: int, month: int, year: int) -> None:
        """Sets this date to the given date.
        
        This method attempts to check the sensibilty of the given date. In particular, a two digit year is converted to a four digit year in the range 1950 to 2049 (e. g., a year of '97' becomes 1997 and a year of '35' becomes 2035). This method also forces the year into the range from 1800 to 2099 by silently truncating out of range years. Finally, it forces the day and month into sensible ranges.

        This method should probably raise an exception for out of range years and for invalid dates. It currently accepts dates such as February 30, 2020 because '30' is generally in range for months even if not for February. It should raise an exception for that sort of invalidity as well.
        """

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

        # Check year.
        if self.Y < 1800 or self.Y > 2099:
            raise InvalidDate("invalid year: {0}".format(self.Y))

        # Check month.
        if self.M < 1 or self.M > 12:
            raise InvalidDate("invalid month: {0}".format(self.M))

        # Check day.
        if self.D < 1 or self.D > 31:
            raise InvalidDate("invalid day: {0}".format(self.D))
        if self.D > self.month_length():
            raise InvalidDate("invalid day of the month: day = {0}, month = {1}".format(
                self.D, self.M))


    # Advance this date by one day.
    def next(self) -> None:
        self.D = self.D + 1
        if self.D > self.month_length():
            self.D = 1
            self.M = self.M + 1
            if self.M > 12:
                self.M = 1
                self.Y = self.Y + 1
        if self.Y > 2099: raise InvalidDate("invalid date after 'next'")


    # Back up this date by one day.
    def previous(self) -> None:
        fix_day = 0

        self.D = self.D - 1
        if self.D < 1:
            fix_day = 1
            self.M = self.M - 1
            if self.M < 1:
                self.M = 12
                self.Y = self.Y - 1

        if fix_day: self.D = self.month_length()
        if self.Y < 1800: raise InvalidDate("invalid date after 'previous'")


    # Advance this date by the given number of days.
    def advance(self, delta: int) -> None:
        # If there is nothing to do, bail out.
        if delta == 0: return

        # Otherwise do real work.
        if delta > 0:
            for i in range(1, delta + 1):
                self.next()
        else:
            for i in range(1, -delta + 1):
                self.previous()

    # Relational Operators
    # --------------------

    def __lt__(self, other) -> bool:
        compare_result = compare(self, other)
        if compare_result == -1: return True
        return False

    def __le__(self, other) -> bool:
        compare_result = compare(self, other)
        if compare_result == -1 or compare_result == 0: return True
        return False

    def __gt__(self, other) -> bool:
        compare_result = compare(self, other)
        if compare_result ==  +1: return True
        return False

    def __ge__(self, other) -> bool:
        compare_result = compare(self, other)
        if compare_result == +1 or compare_result == 0: return True
        return False

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Date):
            return NotImplemented
        return compare(self, other) == 0

    def __ne__(self, other: object) -> bool:
        return not (self == other)


#
# This is the end of the class definition. What follows are normal functions.
#

# Returns -1 if d1 is before d2, 0 if d1 = d2, and +1 if d1 is after d2.
def compare(d1: Date, d2: Date) -> int:
    if d1.Y < d2.Y: return -1
    if d1.Y > d2.Y: return +1
    if d1.M < d2.M: return -1
    if d1.M > d2.M: return +1
    if d1.D < d2.D: return -1
    if d1.D > d2.D: return +1
    return 0


# Returns the number of days d1 is after d2
def difference(d1: Date, d2: Date) -> int:
    result = 0

    # What is their relationship?
    relation = compare(d1, d2)

    # Handle the simple case first.
    if relation == 0: return 0

    # Make copies. Is there a better way to do this?
    tempD1 = Date(d1.D, d1.M, d1.Y)
    tempD2 = Date(d2.D, d2.M, d2.Y)

    # Man, this is ugly!
    while compare(tempD1, tempD2) == 1:
        tempD2.next()
        result = result + 1

    while compare(tempD1, tempD2) == -1:
        tempD1.next()
        result = result - 1

    return result

# Test/Demonstration code. More complete testing is needed.
if __name__ == "__main__":
    d = Date(28, 2, 2000)
    d.next()
    print("%04d-%02d-%02d" % (d.Y, d.M, d.D))
    d.set(3, 9, 2021)
    print("%04d-%02d-%02d" % (d.Y, d.M, d.D))
