import json
import re
import ujson
import pprint


data = ujson.load(open('drexel_best.json'))


pp = pprint.PrettyPrinter(indent=4)
pprint.pprint(data, depth=5)





