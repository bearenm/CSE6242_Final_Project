# -*- coding: utf-8 -*-

import os
import pandas as pd
import json
#from itertools import combinations

WC=pd.read_csv('fake_data.csv')

# start a new flare.json document
flare = dict()
flare = {"name":"flare", "children": []}
d = flare

for line in WC.values:
    h1 = line[0]
    h2 = line[1]
    h3 = line[2]
    h4 = line[3]
    h5 = line[4]
    # make a list of keys
    h1_l = []
    for item in d['children']:
        h1_l.append(item['name'])

    # if 'the_parent' is NOT a key in the flare.json yet, append it
    if not h1 in h1_l:
        d['children'].append({"name":h1, "children":[{"name":h2, "children":[{"name":h3, "children":[{"name":h4, "size":h5}]}]}]})

    # if 'the_parent' IS a key in the flare.json, add a new child to it
    else:
        h2_l = []        
        for item in d['children'][h1_l.index(h1)]['children']:
            h2_l.append(item['name'])
        #print sub_list

        if not h2 in h2_l:
            d['children'][h1_l.index(h1)]['children'].append({"name":h2, "children":[{"name":h3, "children":[{"name":h4, "size":h5}]}]})
        else:
            h3_l = []        
            for item in d['children'][h1_l.index(h1)]['children'][h2_l.index(h2)]['children']:
                h3_l.append(item['name'])
            
            if not h3 in h3_l:
                d['children'][h1_l.index(h1)]['children'][h2_l.index(h2)]['children'].append({"name":h3, "children":[{"name":h4, "size":h5}]})
            else:
                d['children'][h1_l.index(h1)]['children'][h2_l.index(h2)]['children'][h3_l.index(h3)]['children'].append({"name":h4, "size":h5})


flare = d


# export the final result to a json file
with open('example.json', 'w') as outfile:
    json.dump(flare, outfile,indent=1)
