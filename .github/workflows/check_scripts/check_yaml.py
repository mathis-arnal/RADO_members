#!/usr/bin/env python3

import argparse
import re
import sys
import yaml
import pathlib

def validate_category(d,f):
    for key in d:
        if key.lower() != key:
           print (key + " must be lower case!")
           return False
    return True 

def validate_orcid(d, f):
    regex = re.compile(r'^(\d{4}-){3}\d{3}[\dX]$')
    try:
        return re.search(regex, d['orcid'])
    except KeyError:
        return True
    except TypeError:
        return True

def validate_url(d, f):
    regex = re.compile(r'^https?://')
    if 'homepage' in d.keys():
        if d['homepage'] is not None:
            if re.search(regex, d['homepage']):
                return True
            else: # case value do not follow specification
                return False
        else: # case no value provided for homepage tag
            return True
    else: # case no homepage tag
        return True
    



# Just add checks here, key should be error message, value is a function that returns true if everything is fine.
checks = {
    'category has to be all lower case': validate_category,
    'invalid orcid': validate_orcid,
    'invalid homepage': validate_url
}

def check_file(file):
    num_errors = 0
    with open(file) as fh:
        res = yaml.safe_load(fh)
        for check in checks:
            if not checks[check](res, file):
                print("File {} fails test '{}'".format(file, check))
                num_errors += 1

    return num_errors

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', metavar='FILES', nargs='*',
            default=(),
            help='files to check')

    args = parser.parse_args()

    num_errors = 0
    for file in args.files:
        print ("check " + file)
        num_errors += check_file(file)

    if num_errors == 0:
        print("Success, all checks succeeded")
    else:
        print("Some failures, please fix")
        sys.exit(1)


if __name__ == '__main__':
    run()
