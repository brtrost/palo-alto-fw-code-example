# Written by -  Brian Trost, trostb@gmail.com
# Description - Get firewall info through panorama
# Date - February 13th, 2019

import string, getpass, argparse, urllib3, ssl, os, sys, requests
from xml.dom import minidom
import xml.etree.ElementTree as ET
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Handler for the command line arguments, if used.
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--querytarget", help="IP address of the panorama")
parser.add_argument("-k", "--apikey", help="API Key")
parser.add_argument("-u", "--username", help="User login")
parser.add_argument("-p", "--password", help="Login password")
args = parser.parse_args()

if args.querytarget:
    querytarget = args.querytarget
else:
    querytarget = raw_input("Enter the IP of the panorama: ")

def printdes(s,o=''):
    print ("\n  " + sys.argv[0] + " - " + s)
    olist = o.split(",")
    if 'printul' in olist:
        tl = len(sys.argv[0]) + len(s) + 7
        print("-"*tl)
    else:
        print("")

def send_api_request(url, values):
    try:
        response = requests.get(url, params=values, verify=False)
        return response.text
    except:
        raise ValueError("API call not successful.")

def get_api_key(hostname, username, password):
    try:
        url = 'https://' + hostname + '/api'
        values = {'type': 'keygen', 'user': username, 'password': password}
        response = requests.get(url, params=values, verify=False)
        parsedresponse = minidom.parseString(response.text)
        return parsedresponse.getElementsByTagName('key')[0].firstChild.nodeValue
    except:
        raise ValueError("Unable to generate API key from panorama.")

def fetch_api_key():
    try:
        if args.apikey:
            apikey = args.apikey
        else:
            if args.username:
                username = args.username
            else:
                username = raw_input("Enter the user login:  ")
            if args.password:
                password = args.password
            else:
                password = getpass.getpass(prompt="Enter the password:  ")

            return get_api_key(querytarget,username,password)
    except:
        raise ValueError("Unable to obtain API key from program arguments or panorama.")

def main():

    apikey = fetch_api_key()
    printdes("show devices and check zone settings",o='printul')

    cmd = '<show><system><info></info></system></show>'
    showcmd = {'type':'op', 'cmd':cmd, 'key':apikey}

    url = "https://%s/api" % querytarget
    print "Target device " + querytarget + "\n"

    showsysteminfoxml = ET.fromstring(send_api_request(url,showcmd))
    model = showsysteminfoxml.find('result').find('system').find('model').text

    panoramamodel = ['M-100','M-500','M-200','M-600']

    if model in panoramamodel:
        cmd = '<show><devices><connected></connected></devices></show>'
        renamedict = {'type':'op', 'cmd':cmd, 'key':apikey}

        url = "https://%s/api" % querytarget
        print "Querying...." + url + "\n"

        showconn = ET.fromstring(send_api_request(url,renamedict))

        for child in showconn.findall('.//devices/entry'):
            serial = child.find('serial').text
            hostname = child.find('hostname').text
            hip = child.find('ip-address').text
            model = child.find('model').text

            state = child.find('ha').find('state').text

            if state == 'active':
                xpath = '/config/devices/entry[@name=\'localhost.localdomain\']/vsys'
                lookupdict = {'type': 'config', 'action': 'get', 'key':apikey, 'xpath':xpath, 'target':serial}
                zpp = ''

                url = "https://%s/api" % querytarget
                print("%s - %s - %s - %s\n" % (hostname,serial,hip,model))
                y = ET.fromstring(send_api_request(url,lookupdict).encode('utf-8'))
                print(" Finding VSYS")

                for vsysentry in y.findall('.//vsys/entry'):
                    print(" - Found VSYS entry %s - %s" % (vsysentry.get('name'),vsysentry.find('display-name').text))
                print("")
    else:
        print("Not a panorama device, exiting.\n")

if __name__ == '__main__':
    main()
