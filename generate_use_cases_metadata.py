#!/usr/bin/env python
#
# Python file to read all use case JSONs in the direcory and generate a 
# single use cases metadata file for Neptune use-cases page.

import simplejson as json
import os
import sys

from os import listdir
from os.path import isfile, join

# Get all the JSON files in this directory and subdirectories.
directory = os.path.dirname(os.path.realpath(sys.argv[0]))
files = []
for (dirpath, dirnames, filenames) in os.walk(directory):
    if '.git' in dirpath:
        continue
    files.extend([dirpath + "/" + f for f in filenames if '.json' in f and 'use-cases.json' not in f])
print "Processing ", len(files), " use cases."

final_json = []
for f in files:
    with open(f) as data_file:    
        print "Processing ", f
        head, name = os.path.split(f)
        category = os.path.basename(head) 
        data = json.load(data_file)
        if 'tags' not in data:
            continue
        usecase = {}
        print category, name
        if 'tags' in data:
            usecase['tags'] = data['tags'] 
        if 'tagline' in data:
            usecase['tagline'] = data['tagline']
        if 'trigger' in data:
            usecase['trigger'] = data['trigger']
        if 'action_group' in data:
            usecase['action_group'] = data['action_group']
            template_details = {'id': "", 'category': category, 'name': name}
            usecase['action_group']['template'] = template_details
        if 'video' in data:
            usecase['video'] = data['video']
        final_json.append(usecase)

# Remove the existing use-cases.json file
usecases_file = "use-cases.json"
os.remove(usecases_file)
outfile = open(usecases_file, "w")
outfile.write(json.dumps(final_json, indent=4, sort_keys=True))
outfile.close()
print "Done generating the use-cases.json file"

