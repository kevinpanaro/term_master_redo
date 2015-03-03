import json
import re
import ujson
import pprint


f = ujson.load(open('scraped_data/drexel_best.json'))


# pprint.pprint(f, depth=2)
term = "Spring Quarter 14-15"
course = "MATH" # technically also Semester?
number = "101"


def search_class(json, search):
    '''returns class dictionary (add technically term)'''
    temp_jawn = []
    for size in range(len(json)):
        if json.keys()[size] == search:
            return json[search]
    last_key = json.keys()[size]
    return search_class(json[last_key], search)
        

def all_number_return(json, search):
    '''returns all classes with number XXX'''
    class_number_dict = {}
    for term in json:
        for course in json[term].keys():
            for num in json[term][course].keys():
                if num == search:
                    class_number_dict[course] = {num: json[term][course][num]}

    return class_number_dict
        



