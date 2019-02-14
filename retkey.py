# Written by -  Brian Trost, btrost@paloaltonetworks.com
# Description - Get API key from file
# Date - February 14th, 2019

import string, os

def read_key_file(host):
    try:
        pwfile = '.panconfkeystore'
        f = open(os.path.expanduser('~') + "/" + str(pwfile))
        s = f.readlines()
        f.close()
        for line in s:
            if line.split(":")[0] == host:
                return line.split(":")[1].strip()
        return False
    except:
        return False
