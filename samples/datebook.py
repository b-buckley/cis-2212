#
# This script manages a simple datebook.
#

import sys
import time

class DatebookItem:
    def __init__(self, raw_time, description):
        self.time = raw_time
        self.text = description

    def display(self):
        print(time.ctime(self.time), ", ", self.text)

    def dump(self, output):
        output.write(("%s" % self.time) + "|" + self.text + "\n")

      
class Datebook:
    def __init__(self):
        self.items = []
        self.filename = "datebook.dat"

        # Should have a better way to specify the datebook filename.
        try:       
            input = open(self.filename, "r")
            for line in input.readlines():

                # What happens here if I get an empty line? Bad things?            
                if line[-1] == '\n': line = line[:-1]
                fields = line.split('|')

                # Should check to be sure there are two fields first.            
                new_item = DatebookItem(float(fields[0]), fields[1])
                self.items.append(new_item)
            
            input.close()
        except FileNotFoundError:
            print("Warning: datebook.dat not found; datebook is empty")

    def append(self, new_item):
        self.items.append(new_item)

    def display(self):
        counter = 1
        for item in self.items:
            print(counter, end=': ')
            counter += 1
            item.display()

    def dump(self):
        output = open(self.filename, "w")
        for item in self.items:
            item.dump(output)

        output.close()        

#
# Helper functions
#

def display_menu():
    print()
    print("0) Quit")
    print("1) Add Item\n")
    print("Choice?")
    result = sys.stdin.readline()
    if result[-1] == '\n': result = result[:-1]
    return int(result)

#
# The main script
#
mybook = Datebook()
while True:
    mybook.display()
    choice = display_menu()

    if choice == 0:
        mybook.dump()
        sys.exit()

    if choice == 1:
        print("Enter Item Text:", end=' ')
        text_result = sys.stdin.readline()
        if text_result[-1] == '\n': text_result = text_result[:-1]
        print("Enter Item Date:", end=' ')
        date_result = sys.stdin.readline()
        if date_result[-1] == '\n': date_result = date_result[:-1]
        # Here is where I have to parse the date string.
        new_item = DatebookItem(time.time(), text_result)
        mybook.append(new_item)
