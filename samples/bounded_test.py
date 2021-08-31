#!/usr/bin/python

import bounded

my_list = bounded.BoundedList(3)
my_list.append(1)
my_list.append(2)
my_list.append(3)

if len(my_list) != 3:
    print("The length of my_list is wrong!")

if my_list[0] != 1 or my_list[1] != 2 or my_list[2] != 3:
    print("The values stored in my_list are wrong!")
    
my_list[0] = 4
my_list[1] = 5
my_list[2] = 6

if my_list[0] != 4 or my_list[1] != 5 or my_list[2] != 6:
    print("The values stored in my_list after updating it are wrong!")
    
my_list.append("BADNESS!")

