#!/usr/bin/python

class BoundedList:
    
    # Create an empty list and store the bound on its size.
    def __init__(self, maximum_size):
        self.maximum_size = maximum_size
        self.raw_list = []

    def append(self, item):
        if len(self.raw_list) == self.maximum_size:
            # In real life an exception should probably be raised here.
            print("You attempted to extended a BoundedList beyond its maximum size!")
        else:
            self.raw_list.append(item)
            
    def __len__(self):
        return len(self.raw_list)
        
    def __getitem__(self, index):
        return self.raw_list[index]
        
    def __setitem__(self, index, value):
        self.raw_list[index] = value
        
