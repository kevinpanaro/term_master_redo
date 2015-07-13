import re
import ujson
import pprint
import json


f = ujson.load(open('fall_links.json'))



def search_all(f, search):
    '''given file (f) and search ("MATH", "101", or "MATH 101")
    returns json dictionary of the values that applies that'''
    # theres only ever one term right now, so this returns the only term
    for term in f.keys():
        terms = f[term]
    split_text = re.split(" ", search.upper())
    # determine search type and extract the goods (by deleting anythings that isn't the search string)
    if len(split_text) == 2:
        full = split_text
        cls = full[0]
        num = full[1]
        for item in terms.keys(): 
            if item != cls:
                del terms[item]
        for item in terms[cls].keys():
            if item != num:
                del terms[cls][item]
        return terms
    elif split_text[0].isdigit() is True:
        num = split_text
        for course in terms.keys():
            for num in f[term][course].keys():
                if num != search:
                    del terms[course][num]
        for item in terms.keys():
            if len(terms[item]) != 1:
                del terms[item]
        return terms
    else:
        cls = split_text[0]
        for course in terms.keys():
            if course != cls:
                del terms[course]
        return terms



# output = search_all(f, search)
# name_of_file = "temp2" + ".json"
# output_json = json.dumps(output)
# with open(name_of_file, "w") as f:
#     f.write(output_json)


## THIS ONLY PRINTS OUT STUFF AND IS NOT NEEDED FOR THE REST OF THE GOODS
# counter1 = 0
# counter2 = 0
# for b in output:
#     b = output[b]
#     b1 = output.keys()
#     for num in b:
#         c1 = b.keys()
#         c = b[num]
#         for cls in c:
#             crn = c[cls]
#             for cr in crn:
#                 print b1[counter1] + " "+ c1[counter2]
#                 det = crn[cr]
#                 out = cls + '\n' + "CRN: "+cr+ '\n' +det["days"] + ' ' + det["times"]+ '\n' +det["comments"]+ '\n' +'\n'
#                 print out
#         counter2 += 1
#     counter1 += 1  

# goes through each course dictionary in output dictionary   
def save_in_nice_file(output): 
    for course_name in output.keys():
        
        # from here, current_course_n, where n is how "deep" I am in the dictionary, is how I'll be labelling them.          
        current_course_1 = output[course_name]
        # finds course number in current course
        for course_num in current_course_1.keys():
            current_course_2 = current_course_1[course_num]
            for course_type in current_course_2.keys():
                current_course_3 = current_course_2[course_type]
                for course_crn in current_course_3.keys():
                    current_course_4 = current_course_3[course_crn]
                    print "course: " + course_name
                    print "num: " +course_num
                    print "type: " +course_type
                    print "crn: " + course_crn
                    for item in current_course_4.keys():
                        if str(item) == 'link' or str(item) =='building' or str(item) =='end_date' or str(item) =='start_date' or str(item) =='title' or str(item) == 'room' or str(item) == 'enroll' or str(item) == 'max_enroll':
                            pass
                        else:
                            print item + ": "+ current_course_4[item]
                        

                    print "\n"


if __name__ == '__main__':
    classes = ["ENGR 101", "PHYS 101", "EXAM 80"]
    for cls in classes:
        name_of_file = cls + ".txt"
        f = ujson.load(open('fall_links.json'))
        output = search_all(f, cls)
        save_in_nice_file(output)
        # with open(name_of_file, "w") as a:
        #     a.write(json.dumps(output))

# se = ["MATH 101"]
# with open(name_of_file, 'w') as a:

#     for cls in se:
#         print cls
#         f = ujson.load(open('fall_links.json'))
#         a.write(json.dumps(search_all(f, cls)))



