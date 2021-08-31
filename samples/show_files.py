#!/usr/bin/python

import os

def get_file_list(directory_name):
    result = []
    raw_names = os.listdir(directory_name)
    for name in raw_names:
        if os.path.isdir(name):
            result = result + get_file_list(directory_name + "\\" + name)
        else:
            result.append(directory_name + "\\" + name)
    return result

# Output the result in a semi-nice way. The list itself can be printed, but it's formatted
# in Python style and that's kinda ugly for end users.
for file_name in get_file_list("."):
    print(file_name)


