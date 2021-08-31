#!/usr/bin/python

def list_stats(some_list):
    total   = 0
    maximum = some_list[0]
    minimum = some_list[0]
    for item in some_list:
        total = total + item
        if item > maximum: maximum = item
        if item < minimum: minimum = item
    return (float(total)/float(len(some_list)), maximum, minimum)

# Just a quick and dirty example to check the above function.
(total, maximum, minimum) = list_stats([1, 2, 3, 4])

print("Average = ", total)
print("Maximum = ", maximum)
print("Minimum = ", minimum)

