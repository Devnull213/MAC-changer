#!/usr/bin/env python3

import subprocess
import re
import argparse
   

def change_mac(interface, new_mac):
    ''' Change the virtual MAC by another
        passed as parameter'''

        # Validate address format

    mac_validate = '[A-Fa-f\d:]{17}'
    if re.search(mac_validate, new_mac):
        pattern = 'ether\s([\da-fA-F:]+)'

        # Running processes in order to get the current address

        ifconfig_output = subprocess.run(['ifconfig', interface ], capture_output=True)
        current_mac= ifconfig_output.stdout.decode()
        old_mac = re.search(pattern, current_mac)

        # Running processes to make the change

        subprocess.run(['sudo', 'ifconfig', interface, 'down'])
        subprocess.run(['sudo', 'ifconfig', interface, 'hw', 'ether', f'{new_mac}'])
        subprocess.run(['sudo', 'ifconfig', interface, 'up'])
        check = subprocess.run(['ifconfig', interface ], capture_output=True)
        check_exit_status = check.returncode

        # Checking the result of the change and getting the new address 

        if check_exit_status == 0:
            print('The process has been succesfull.\n')
            new_ifconfig_output = subprocess.run(['ifconfig', interface ], capture_output=True)
            new_current_mac = new_ifconfig_output.stdout.decode()
            new_checked_mac = re.search(pattern, new_current_mac)

            # Printing the results

            print(f'The new MAC address is: {new_checked_mac[1]}\n')
            print('Printing the WLO1 fragment of ifconfig command: \n')
            print(check.stdout.decode())
            print('\n')
            print('Program finished')
        else:
            print('An error has ocurred\n')
            print('Program finished')
    else:
        print('Invalid MAC address')
        print('\n')
        print('Program finished')




parser = argparse.ArgumentParser()
parser.description = 'This command let you change your wlan MAC address.'
parser.add_argument('interface', help='Interface to change its MAC address.')
parser.add_argument('mac', help='New MAC address.')
args = parser.parse_args()


change_mac(args.interface, args.mac)






