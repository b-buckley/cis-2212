#!/bin/python3

# Ben Buckley
# ELT-2212
# 9/28/2021

# homework-02.py takes a search string from the command line and returns an area,
# in square miles.  The string is used to query the OSM database via the Nominatim
# API.  We blindly take the first result, calculate the area of its bounding box
# and print it nicely for the user.

import sys
import requests

base_url = 'https://nominatim.openstreetmap.org/search?'

def geocode(address, format='json', limit=1, **kwargs):
    '''
    geocode() provides a bone simple wrapper for the OSM Nominatim API.
    It builds a dict of parameters, either passed to it or from defaults,
    and a search string made up of any paramters not matched to defined list.
    geocode() then calls Nominatim at the base url with the parameters and returns
    the JSON-formatted version of the response.

    Documentation: https://nominatim.org/release-docs/develop/api/Search/#parameters
    '''
    params = {
        "q":address,
        "format":'json',
        "limit":limit,
        **kwargs
    }

    response = requests.get(base_url, params=params)
    response.raise_for_status()
    return response.json()

# construct KWARGS out of command line params
if len(sys.argv) > 1:
    city_name = sys.argv[1]
else: # or help the user get it right
    print("USAGE: ./homework-02.py City Name\nCity names with spaces and special characters must be entered in quotes.")

result = geocode(city_name)[0]
#DEBUG: print("Found: ",result[0])

display_name = result["display_name"]

earth_circum = 24901 #in miles

boundingbox = result["boundingbox"]
height_degs = abs(float(boundingbox[0]) - float(boundingbox[1])) #calculate delta latitude
height_miles = earth_circum * (height_degs/360) #calculate the latitude arc length, in miles
width_degs = abs(float(boundingbox[2]) - float(boundingbox[3])) #calculate delta longitude
width_miles = earth_circum * (width_degs/360) #calculate the longitude arch length, in miles

area = height_miles * width_miles

print("The area of the OSM bounding box for "+display_name+" is ~",area,"square miles.")

# Attractive future refinements:
    # return list of possibles
    # let user choose
    #
    # more strucured input, taking advantage of cl long args and the sub-fields of OSM data
    #
    # check user input against a list of cities, or against other OSM data for object type
    #   to exclude, e.g.: houses
    #
    # account for the curvature of the earth
    #
    # use a totally different data source with city boundaries and generators to "carve" away
    #   bounding box area to get a much better approximation.
