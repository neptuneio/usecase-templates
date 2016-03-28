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
        if not 'tags' in data:
            print "Ignoring ", f, " since it does not have tags."
            continue
        usecase = {}
        print category, name
        if 'tags' in data:
            usecase['tags'] = data['tags']
        if 'tagline' in data and len(data['tagline']) > 0:
            usecase['tagline'] = data['tagline']
        elif 'rule_template' in data and 'RuleName' in data['rule_template']:
            usecase['tagline'] = data['rule_template']['RuleName'] 
        if 'trigger' in data:
            usecase['trigger'] = data['trigger']
        if 'action_group' in data:
            if 'template' in data['action_group'] and 'index' in data['action_group']['template']:
                usecase['index'] = data['action_group']['template']['index']
            else:
                usecase['index'] = 999

            usecase['action_group'] = data['action_group']
            template_details = {'id': "", 'category': category, 'name': name}
            usecase['action_group']['template'] = template_details
        if 'video' in data:
            usecase['video'] = data['video']
        final_json.append(usecase)

# Sort the usecases based on index.
final_json = sorted(final_json, key=lambda usecase: usecase['index'])

# Remove the existing use-cases.json file
usecases_file = "use-cases.json"
os.remove(usecases_file)
outfile = open(usecases_file, "w")
outfile.write(json.dumps(final_json, indent=4, sort_keys=True))
outfile.close()
print "Done generating the use-cases.json file"

