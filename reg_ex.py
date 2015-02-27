__author__ = 'igor.medvyedyev'

import re
import sys
import getopt


def Find(pat, text):
    match = re.findall(pat, text)
    if match:
        print(match)
        #for group in match.groups():
        #    print(group)
    else:
        print('not found')

    # tup = (1, 2, 3)
    # dig = 5
    # print("tuple %s, %d" % (str(tup), dig))


def check_file_name(file_name):

    try:
        f = open(file_name, 'r')
    except IOError:
        print('cannot open input file', file_name)
    else:
        print(file_name, 'has', len(f.readlines()), 'lines')
        f.close()

    match = re.search(r'[\w\s]*Baby[\w\s]*20\d\d', file_name)

    if match:
        return True

if __name__ == "__main__":
    # str1 = '<pp><b>Vikipedia</b> - free enciklopedia<i>any</i> can modify text.</pp>'
    # Find(r'<.*?>', str1)


    optlist, args = getopt.getopt(sys.argv[1:], 's', ['summary'])

    if args and check_file_name(args[0])

        f = open(args[0], "r")
        with open(args[0]) 

    else:
        print("Please arg input file")







