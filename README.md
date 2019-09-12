# Hikxploit
hixploit is a python tool that will give you the opportunity to gather all hikvision cctv that are vulnerable to a specific exploit and then change its password
# Disclaimer
The tool can work even on windows with the specific version of the too
# Photo
![Alt text](https://github.com/M0tHs3C/Hikxploit/blob/master/foto.png?raw=true "Title")
# Install
get
```bash
git clone https://github.com/M0tHs3C/Hikxploit.git
```
pip
```bash
pip install shodan
pip install censys
```
# Usage
* 1 . Gather host with shodan (api needed)
* 2 . Gather host with censys.io (api needed)
* 3 . scan for up host
* 4 . scan for vuln host
* 5 . mass exploit all vuln CCTV
* 6 . select a CCTV'S ip to exploit
* 7 . random exploit CCTV from the vuln list
* 8 . install dependency
# Suggested query's
for shodan and censys the best query's for now is
```bash
App-webs 200 OK
App-webs 200 OK location.country_code: IT (works great by selecting where you wish to test)
```
# Tutorial
Hikxploit is a very simple tool, it may have some bugs but i'm working on to fix most of them
---1---
First you have to gather some host with censys or shodan 
in order to use this search engine you will need a key or two
the tool will probably ask you a key if it can't read from the file due to some permission failure
you can just copy paste the key on the tool or you can open up the api file in the tool folder and copy paste it on the first line of the tool
If you use shodan you will need only one line
If you use censys you will need two so you have to save it one line at a time.
--2--
After gathering some hosts you will need se if the hosts you gathered are really up
This function will test if the hosts can be pinged proving that is really up
--3--
After that we will need to test if all the host that we gathered are really vulnerable at the exploit
Some of them will not be vulnerable but no worries
remember, shodan like censys offer a basic free plan wich limit your search
there are really a lot of cameras still vulnerable to this exploit and this is bad
--After this step we are ready to exploit--
the other options are really self-explanatory
# Future update
im working on another exploit in order to amplify my tool by adding other exploit for other cameras from other companies


legal disclaimer: Usage of hikxploit for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program
