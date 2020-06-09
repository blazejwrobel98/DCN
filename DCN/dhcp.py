import time
import os
from os import path
import shutil
import nmap
import config

def GetInfoAboutDHCPserv():
    print('DHCP server checking, please wait...')
    time.sleep(1)
    stream = os.popen('service isc-dhcp-server status | grep Active:')
    output = stream.read()
    str(output)
    match = '(running)'
    if(match in output):
        print('DHCP server is running, checking hosts...')
    else:
        print('DHCP server is NOT running, let me check what happend')
        time.sleep(1)
        if path.exists("/etc/dhcp/dhcpd.conf")==True:
            print('Configuration file exists')
            shutil.copy('configuration/dhcpd.conf', '/etc/dhcp')
            print('Configuration file copied into /etc/dhcp')
            shutil.copy('configuration/isc-dhcp-server', '/etc/default')
            print('Configuration file copied into /etc/default')
            os.popen('service isc-dhcp-server force-reload')
            print('restarting service... TRY AGAIN')
            GetInfoAboutDHCPserv()

def ScanHosts():
        nm = nmap.PortScanner()
        nm.scan(config.Nmap_scan['range'], arguments='-sP -n')
        hosts = {}
        for h in nm.all_hosts():
            if 'mac' in nm[h]['addresses'] and "00:03:0F" in nm[h]['addresses']["mac"]:
                print(nm[h]['addresses'])
                hosts[nm[h]['addresses']["ipv4"]] = nm[h]['addresses']["mac"]
        return hosts

def ScanIsAlive(IP):
    nm = nmap.PortScanner()
    nm.scan(IP,config.Nmap_scan['port'])
    hosts = nm.all_hosts()
    return hosts
