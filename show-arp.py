# Written by -  Brian Trost, trostb@gmail.com
# Description - Run op command on firewall
# Date - Feb 13th, 2018

import string, getpass, argparse, urllib3, ssl, requests, sys
from xml.dom import minidom
import xml.etree.ElementTree as ET
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Handler for the command line arguments, if used.
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--firewall", help="IP address of the firewall")
parser.add_argument("-i", "--interface", help="Interface")
parser.add_argument("-k", "--apikey", help="API Key")
parser.add_argument("-u", "--username", help="User login")
parser.add_argument("-p", "--password", help="Login password")
args = parser.parse_args()

if args.firewall:
    firewall = args.firewall
else:
    firewall = raw_input("Enter the name or IP of the firewall: ")
if args.interface:
    interface = args.interface.strip()
else:
    interface = 'all'

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
        raise ValueError("Unable to generate API key from firewall.")

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

            return get_api_key(firewall,username,password)
    except:
        raise ValueError("Unable to obtain API key from program arguments or firewall.")

def main():

    apikey = fetch_api_key()
    printdes("show arp with cleaned up output")
    cmd = '<show><arp><entry name = \'%s\'/></arp></show>' % (interface)
    opdict = {'type':'op', 'cmd':cmd, 'key':apikey}

    url = "https://%s/api" % firewall

    showarpxml = ET.fromstring(send_api_request(url,opdict))

    for entry in showarpxml.findall('.//result'):
        total = entry.find('total').text
    print ("Total arp entries: %s\n" % total)

    for entry in showarpxml.findall('.//entry'):
        ip = entry.find('ip').text
        mac = entry.find('mac').text
        net = entry.find('interface').text
        ttl = entry.find('ttl').text
        print(ip + " - " + mac + " - " + net + " - " + ttl)
    print("\n")

if __name__ == '__main__':
    main()
