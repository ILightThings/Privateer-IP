import os
import argparse
import socket
import dns.resolver
import re
import json
import whois
import requests
from bs4 import BeautifulSoup

dnsservers = {"Hosts File":"127.0.0.1",
              "Canada, Ontario, Mississauga":"72.139.50.226",
              "Canada, BC, Vancover":"137.82.1.1",
              "France, Paris":"194.98.65.65",
              "USA, New York":"185.213.26.187",
              "Japan, Toykio":"202.248.20.133",
              "General, Cloud Flare":"1.1.1.1",
              "General, Google":"8.8.8.8",
              "General, Quad 9":"9.9.9.9",
              }
dnsservers1 = {"Canada, Qubec, Montreal":"184.149.50.25",
              "Canada, Ontario, Toronto":"72.139.50.226",
              "Canada, Albera, Edmonton":"209.29.150.135",
              "France, Paris":"194.98.65.65",
              "USA, New York":"185.213.26.187",
              "Japan, Tokyo":"202.248.20.133",
              "General, Cloud Flare":"1.1.1.1",
              "General, Google":"8.8.8.8",
              "General, Quad 9":"9.9.9.9",
              }
thelookup = dns.resolver.Resolver()
site = "***REMOVED***"
ip_regex = re.compile("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}")



def globalDNS(domain):
    resolvedIPs = []
    print("### GLOBAL DNS LOOKUP  (Determines if the site is multihosted)")
    for x in dnsservers:
        print(f"[x] {x: <30}",end="")
        try:
            thelookup.nameservers = [dnsservers[x]]
            answer = str(thelookup.resolve(domain,"A").response).split(';')
            ipfind = re.findall(ip_regex,answer[2])[0]
            resolvedIPs.append(ipfind)
            print(f"{ipfind: <20}")
        
                
        except dns.exception.Timeout:
            print(f"DNS Server unreachable")
        except dns.resolver.NoAnswer:
            print(f"Could no record of {site} at {dnsservers[x]}")
        except dns.resolver.NoNameservers:
            print("Not found")
    return (list(set(resolvedIPs)))
        
def whoisIPLookup(ipList):
    print("\r\n### WHOIS LOOKUP   (Determines who owns the IP)")
    for ip in ipList:
        w = whois.whois(ip)
        entry = w['domain_name'] or w['org'] or w['name']  or f"Whois Entry not found for this {ip}"
            
        print(f"[x] {ip: <30}{entry}")

def requestByIP(ipList):
    print("\r\n### REQUEST PAGE BY IP  (Determines if there is virtual hosting)")
    q = requests.get("http://"+site)
    qs = BeautifulSoup(q.text,features="html.parser")
    print(f"[x] http://{site:<30}   {'Page Title: ' + qs.find('title').string}")
    for ip in ipList:
        r = requests.get("http://"+ip)
        rs = BeautifulSoup(r.text,features="html.parser")
        print(f"[x] http://{ip:<30}   {'Page Title: ' + rs.find('title').string}")
    
    
print(f"###### {site}")
ipList = globalDNS(site)
whoisIPLookup(ipList)
requestByIP(ipList)

    
    
    

