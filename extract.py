import json
import re
import ujson
import pprint


f = ujson.load(open('scraped_data/drexel_best.json'))


# pprint.pprint(f, depth=2)
term = "Spring Quarter 14-15"
course = "MATH".upper()  # technically also Semester?
number = "101"
joined = "ECON 201".upper()


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
    return_dict = {}
    for term in json:
        for course in json[term].keys():
            for num in json[term][course].keys():
                if num == search:
                    return_dict[course] = {num: json[term][course][num]}

    return return_dict


def joined_search(json, search):
    '''returns search from CLASS ###'''
    split_text = re.split(" ", search)
    if len(split_text) != 2:
        return "Please enter a valid course description (ie. MATH 101)"
    for item in split_text:
        if len(item) == 3 and item.isdigit() is True:
            number = item
        else:
            course = item
    number_dict = all_number_return(json, number)
    return search_class(number_dict, course)


pprint.pprint(joined_search(f, joined))
