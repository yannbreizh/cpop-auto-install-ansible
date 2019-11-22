#!/usr/bin/python
import sys, os, getopt, netifaces
from scipy import *

"""

This scripts aims at selecting a network interface within a group.
As an example, with the following network configuration:
    itf_mac['eno1'] = '80:30:e0:2d:71:b8'
    itf_mac['eno2'] = '80:30:e0:2d:71:b9'
    itf_mac['eno3'] = '80:30:e0:2d:71:ba'
    itf_mac['eno4'] = '80:30:e0:2d:71:bb'
    itf_mac['eno5'] = '48:df:37:83:09:d0'
    itf_mac['eno6'] = '48:df:37:83:09:d8'

The script identifies groups of interfaces based on MAC prefixes.
A group is defined by having the same first 5 bytes in the MAC address.
In the example above there qre 2 groups:
    '80:30:e0:2d:71': 4 interfaces have MAC starting with this prefix
    '48:df:37:83:09': 2 interfaces have MAC starting with this prefix
        
The script has 2 arguments:
    '-gx -ny': the script will look into a group of 'x' members and will select the element 'y' of this members list

The script constructs a dictionary 'prefix_mac' that includes all prefixes found with their occurence,
as well as interface information sorted in ascending on the MAC address:
prefix_mac : {
    '80:30:e0:2d:71': [4, [             # <- 4 MAC have this prefix
        ['eno1', '80:30:e0:2d:71:b8']   # |
        ['eno2', '80:30:e0:2d:71:b9']   # |--> the list of the 4 MAC
        ['eno3', '80:30:e0:2d:71:ba']   # |
        ['eno4', '80:30:e0:2d:71:bb']   # |
    ],
    '48:df:37:83:09': [2, [
        ['eno5', '48:df:37:83:09:d0']
        ['eno6', '48:df:37:83:09:d8']
    ]
}
"""

def main(argv):
    """
    command args analysis
    """
    try:
        opts, args = getopt.getopt(argv, "hg:n:", ["help=","grp=", "num="])
    except getopt.GetoptError:
        print('Usage: network-conf.py -g<MAC-group-length> -n<range-of-MAC-in-the group>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('network-conf.py -g<MAC-group-length> -n<range-of-MAC-in-the group>')
            print('  <MAC-group-length>: length of the MAC group')
            print('  <range-of-MAC-in-group>: range of the MAC to select within the group')
            sys.exit(2)
        elif opt in ("-g", "--group"):
            grp = arg
        elif opt in ("-n", "--number"):
            num = arg
    # print('num is', num)

    """
    get network interfaces info
    create a dictionnary with them
    """
    itf_dict = {}
    itf_mac = {}
    for iface in netifaces.interfaces():
        if iface == 'lo' or iface.startswith('vbox'):
            continue
        iface_details = netifaces.ifaddresses(iface)
        itf_dict[iface] = iface_details[netifaces.AF_LINK]
    for l in itf_dict:
        itf_mac[l] = itf_dict[l][0]['addr']
        # print(l, itf_mac[l])
    
    # for tests
    # itf_mac = {}
    # itf_mac['eno1'] = '80:30:e0:2d:71:b8'
    # itf_mac['eno2'] = '80:30:e0:2d:71:b9'
    # itf_mac['eno3'] = '80:30:e0:2d:71:ba'
    # itf_mac['eno4'] = '80:30:e0:2d:71:bb'
    # itf_mac['eno5'] = '48:df:37:83:09:d0'
    # itf_mac['eno6'] = '48:df:37:83:09:d8'

    # the prefix_mac dict contains a list [count, itf, mac]:
    #  count -> counts the number of times this prefix was found
    #  itf -> the interface that has the lowest MAC in this group
    #  mac -> the MAC address of the lowest itf
    # prefix_mac = {-1,['dummy','dummy']}
    prefix_mac = {}
    for itf in itf_mac:
        # print(itf, itf_mac[itf])
        prefix = itf_mac[itf][0:14]
        # print(prefix)
        changed = False
        for pfx in prefix_mac:
            if pfx == prefix:
                # this prefix was already found --> increment its count
                changed = True
                prefix_mac[pfx][0] += 1
                prefix_mac[pfx][1].append([itf, itf_mac[itf]])
                # if prefix_mac[pfx][2] > itf_mac[itf]:
                #     prefix_mac[pfx][2] = itf_mac[itf]
                #     prefix_mac[pfx][1] = itf
        if not changed:
            # prefix_mac[prefix] = [1, [itf, itf_mac[itf]]]
            prefix_mac[prefix] = [1, [[itf, itf_mac[itf]]]]
                
    # for tests
    # for p in prefix_mac:
    #     print(p, prefix_mac[p])

    # sort interface lists
    for pfx in prefix_mac:
        prefix_mac[pfx][1].sort()
    
    gotit = False
    for pfx in prefix_mac:
        if not gotit:
            length = prefix_mac[pfx][0]
            if length == int(grp):
                print(prefix_mac[pfx][1][int(num)][0])
                gotit = True

    if not gotit:
        print('none')

    exit(0)
    


if __name__ == "__main__":
    main(sys.argv[1:])



""" Get all IPv4 addresses for all interfaces. """
# from netifaces import interfaces, ifaddresses, AF_INET
# # to not take into account loopback addresses (no interest here)
# addresses = []
# for interface in interfaces():
#     config = ifaddresses(interface)
#     # AF_INET is not always present
#     if AF_INET in config.keys():
#         for link in config[AF_INET]:
#             # loopback holds a 'peer' instead of a 'broadcast' address
#             if 'addr' in link.keys() and 'peer' not in link.keys():
#                 addresses.append(link['addr']) 
# print addresses


# import sys
# import json

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print '1st Argument :', str(sys.argv[0])

# args=''
# for arg in str(sys.argv):
#     args+=arg
# print args
#your_json = '["foo", {"bar":["baz", null, 1.0, 2]}]'
#parsed = json.loads(your_json)
# parsed = json.loads(args)
# print(json.dumps(args, indent=2, sort_keys=True))