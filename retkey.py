# Written by -  Brian Trost, trostb@gmail.com
# Description - Get API key from file
# Date - February 14th, 2019

import os.path


def read_key_file(host, keyfile='.panconfkeystore', splitchar=":", searchpos=0, retpos=1, includehomedir=True):
    if includehomedir == True:
        pathstring = os.path.expanduser('~') + "/" + str(keyfile)
    else:
        pathstring = keyfile
    with open(pathstring) as f:
        for line in f.readlines():
            if line.split(splitchar)[searchpos] == host:
                return line.split(":")[retpos].strip()
    raise Exception("Unable to find firewall in file, exiting now.")
