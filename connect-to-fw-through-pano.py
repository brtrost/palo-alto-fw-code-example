# Written by -  Brian Trost, trostb@gmail.com
# Description - Get firewall info through panorama
# Date - February 13th, 2019

import string
import getpass
import argparse
import urllib3
import ssl
import os
import sys
import requests
import logging
import xml.etree.ElementTree as ET
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

# Handler for the command line arguments, if used.
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--querytarget", help="IP address of the panorama")
parser.add_argument("-k", "--apikey", help="API Key")
parser.add_argument("-u", "--username", help="User login")
parser.add_argument("-p", "--password", help="Login password")
parser.add_argument("-l", "--log", default="INFO")

args = parser.parse_args()

try:
    lnum = getattr(logging, args.log.upper())
except:
    lnum = 20

logging.basicConfig(format='%(message)s', level=lnum)

if args.querytarget:
    querytarget = args.querytarget
else:
    querytarget = input("Enter the IP of the panorama: ")


def printdes(s, o=''):
    print ("\n  " + sys.argv[0] + " - " + s)
    if 'printul' in o.split(","):
        tl = len(sys.argv[0]) + len(s) + 7
        print("-"*tl)
    else:
        print("")


def send_api_request(url, values):
    try:
        return requests.get(url, params=values, verify=False).text
    except:
        raise ValueError("API call not successful.")


def get_api_key(hostname, username, password):
    try:
        url = 'https://' + hostname + '/api'
        values = {'type': 'keygen', 'user': username, 'password': password}
        response = requests.get(url, params=values, verify=False)
        return ET.fromstring(response.text).find('.//result/key').text
    except:
        raise ValueError("Unable to generate API key from firewall.")


def fetch_api_key():
    try:
        if args.apikey:
            apikey = args.apikey
        else:
            if args.username:
                username = args.username
            else:
                username = input("Enter the user login:  ")
            if args.password:
                password = args.password
            else:
                password = getpass.getpass(prompt="Enter the password:  ")

            return get_api_key(querytarget, username, password)
    except:
        raise ValueError("Unable to obtain API key from program arguments or panorama.")


def main():

    apikey = fetch_api_key()

    printdes("Example script", o='printul')

    cmd = '<show><system><info></info></system></show>'
    showcmd = {'type': 'op', 'cmd': cmd, 'key': apikey}

    url = "https://%s/api" % querytarget
    print ("Target device " + querytarget + "\n")

    showsysteminfoxml = ET.fromstring(send_api_request(url, showcmd))
    family = showsysteminfoxml.find('result/system/family').text

    panoramafamily = ['m']

    if family in panoramafamily:
        cmd = '<show><devices><connected></connected></devices></show>'
        connectiondict = {'type': 'op', 'cmd': cmd, 'key': apikey}

        url = "https://%s/api" % querytarget
        logging.info("Querying...." + url + "\n")

        showconn = ET.fromstring(send_api_request(url, connectiondict))

        for fw in showconn.findall('.//devices/entry'):
            serial = fw.find('serial').text
            hostname = fw.find('hostname').text
            hip = fw.find('ip-address').text
            model = fw.find('model').text

            state = fw.find('ha/state').text

            if state == 'active':
                xpath = '/config/devices/entry[@name=\'localhost.localdomain\']/vsys'
                vsysfinddict = {'type': 'config', 'action': 'get',
                                'key': apikey, 'xpath': xpath, 'target': serial}

                url = "https://%s/api" % querytarget
                logging.warning(" %s - %s - %s - %s\n" % (hostname, serial, hip, model))
                showvsys = ET.fromstring(send_api_request(url, vsysfinddict))
                logging.info(" Finding VSYS")

                for vsysentry in showvsys.findall('.//vsys/entry'):
                    logging.info(" - Found VSYS entry %s - %s" %
                                 (vsysentry.get('name'), vsysentry.find('display-name').text))
                print("")
    else:
        logging.info("Not a panorama device, exiting.\n")


if __name__ == '__main__':
    main()
