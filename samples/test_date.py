#!/usr/bin/python

import date
from   date import Date, InvalidDate

def test_set():
    # Let's try valid dates.
    test_dates = [
        ( 1, 1, 1800), (31, 12, 2099),
        (31, 1, 2000), (29,  2, 2000), (31,  3, 2000), (30,  4, 2000),
        (31, 5, 2000), (30,  6, 2000), (31,  7, 2000), (31,  8, 2000),
        (30, 9, 2000), (31, 10, 2000), (30, 11, 2000), (31, 12, 2000)
    ]
    for test_date in test_dates:
        d1 = Date(test_date[0], test_date[1], test_date[2])
        assert d1.D == test_date[0] and d1.M == test_date[1] and d1.Y == test_date[2]

    # Let's try invalid dates.
    test_dates = [
        (31, 12, 1799), ( 1,  1, 2100),
        (32,  1, 2000), (29,  2, 1900), (32,  3, 2000), (31,  4, 2000),
        (32,  5, 2000), (31,  6, 2000), (32,  7, 2000), (32,  8, 2000),
        (31,  9, 2000), (32, 10, 2000), (31, 11, 2000), (32, 12, 2000),
        (15,  0, 2000), (15, 13, 2000)
    ]
    for test_date in test_dates:
        try:
            d1 = Date(test_date[0], test_date[1], test_date[2])
            assert False, "Failed to raise InvalidDate when needed during 'set' operation"
        except InvalidDate:
            None

def test_next():
    test_cases = [
        ((15,  1, 2000), (16,  1, 2000)),
        ((31,  1, 2000), ( 1,  2, 2000)), ((28,  2, 2000), (29,  2, 2000)),
        ((29,  2, 2000), ( 1,  3, 2000)), ((31,  3, 2000), ( 1,  4, 2000)),
        ((30,  4, 2000), ( 1,  5, 2000)), ((31,  5, 2000), ( 1,  6, 2000)),
        ((30,  6, 2000), ( 1,  7, 2000)), ((31,  7, 2000), ( 1,  8, 2000)),
        ((31,  8, 2000), ( 1,  9, 2000)), ((30,  9, 2000), ( 1, 10, 2000)),
        ((31, 10, 2000), ( 1, 11, 2000)), ((30, 11, 2000), ( 1, 12, 2000)),
        ((31, 12, 2000), ( 1,  1, 2001))
    ]
    for test_case in test_cases:
        d1 = Date(test_case[0][0], test_case[0][1], test_case[0][2])
        d2 = Date(test_case[1][0], test_case[1][1], test_case[1][2])
        d1.next()
        assert date.compare(d1, d2) == 0

    try:
        d1 = Date(31, 12, 2099)
        d1.next()
        assert False, "Failed to raise InvalidDate when needed during 'next' operation"
    except InvalidDate:
        None

def test_previous():
    assert False, "test_previous not implemented"

def test_advance():
    assert False, "test_advance not implemented"

def test_relational():
    test_cases = [                     #    EQ     NE     LT     LE     GT     GE
        ((15,  1, 2000), (15,  1, 2000),  True, False, False,  True, False,  True),
        ((31,  1, 2000), ( 1,  2, 2000), False,  True,  True,  True, False, False),
        (( 1,  2, 2000), (31,  1, 2000), False,  True, False, False,  True,  True),
        ((31, 12, 2000), ( 1,  1, 2001), False,  True,  True,  True, False, False),
        (( 1,  1, 2001), (31, 12, 2000), False,  True, False, False,  True,  True) 
    ]
    for test_case in test_cases:
        d1 = Date(test_case[0][0], test_case[0][1], test_case[0][2])
        d2 = Date(test_case[1][0], test_case[1][1], test_case[1][2])
        assert (d1 == d2) == test_case[2]
        assert (d1 != d2) == test_case[3]
        assert (d1 <  d2) == test_case[4]
        assert (d1 <= d2) == test_case[5]
        assert (d1 >  d2) == test_case[6]
        assert (d1 >= d2) == test_case[7]

def test_difference():
    assert False, "test_difference not implemented"