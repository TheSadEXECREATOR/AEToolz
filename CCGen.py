#!/data/data/com.termux/files/usr/bin/env python3
# CCGen.py – BlackTechX – Luhn-valid plastic factory
import os,sys,time,random,csv
from datetime import datetime
from colorama import Fore,init
init(autoreset=True)

LOGO=r"""
  ____ ____      _    ____ _____ _____ ____  
 / ___|  _ \    / \  / ___|_   _| ____|  _ \ 

| |   | |_) |  / _ \| |     | | |  _| | |_) |
| |___|  __/  / ___ \ |___  | | | |___|  _ < 
 \____|_|    /_/   \_\____| |_| |_____|_| \_\
         UNLIMITED PLASTIC GENERATOR
"""

# ---- bins ----
BINS={
    "VISA":["4"]+[f"4{x}" for x in range(0,10**5,1000)],
    "MASTERCARD":["5"]+[f"5{x}" for x in range(10**4,10**5,1000)],
    "AMEX":["34","37"],
    "DISCOVER":["6011"]
}
BANKS=["JPMORGAN CHASE","BANK OF AMERICA","CITIBANK","WELLS FARGO","CAPITAL ONE","BARCLAYS"]
MONTHS=[f"{m:02d}" for m in range(1,13)]
YEARS=[str(y)[-2:] for y in range(datetime.now().year,datetime.now().year+8)]

def luhn(num):
    digs=[int(d) for d in str(num)]
    for i in range(len(digs)-2,-1,-2):
        digs[i]*=2
        if digs[i]>9:digs[i]-=9
    return sum(digs)%10==0

def gen_cc(pre,length=16):
    while True:
        core=str(pre)+"".join([str(random.randint(0,9)) for _ in range(length-len(str(pre))-1)])
        check=(10-(sum(int(d) for d in core)%10))%10
        full=core+str(check)
        if luhn(full):return full

def gen_card(brand):
    pre=random.choice(BINS[brand])
    cc=gen_cc(pre,15 if brand=="AMEX" else 16)
    cvv=str(random.randint(100,9999))[:3 if brand!="AMEX" else 4]
    exp=f"{random.choice(MONTHS)}/{random.choice(YEARS)}"
    zip_code=str(random.randint(10000,99999))
    bank=random.choice(BANKS)
    balance=round(random.uniform(50,15000),2)
    return{"CARD":cc,"BRAND":brand,"BANK":bank,"CVV":cvv,"EXPIRY":exp,"ZIP":zip_code,"BALANCE":balance}

def main():
    os.system("clear")
    print(Fore.RED+LOGO)
    try:
        count=int(input(f"{Fore.CYAN}[?] How many cards to generate: ").strip())
    except ValueError:
        print(f"{Fore.RED}[!] Invalid number – fuck off.");sys.exit(1)
    brand_pick=input(f"{Fore.CYAN}[?] Brand (VISA/MASTERCARD/AMEX/DISCOVER/ALL): ").strip().upper()
    brands=list(BINS.keys()) if brand_pick=="ALL" else [brand_pick]
    outfile=f"ccs_{int(time.time())}.csv"
    with open(outfile,"w",newline='') as f:
        writer=csv.writer(f)
        writer.writerow(["CARD","BRAND","BANK","CVV","EXPIRY","ZIP","BALANCE"])
        for _ in range(count):
            b=random.choice(brands)
            card=gen_card(b)
            writer.writerow(card.values())
            print(f"{Fore.GREEN}[+] {card['CARD']} | {card['CVV']} | {card['EXPIRY']} | ${card['BALANCE']}")
    print(f"\n{Fore.CYAN}[+] Saved {count} cards to {outfile}")

if __name__=="__main__":
    try:main()
    except KeyboardInterrupt:print(f"{Fore.RED}\n[!] Aborted");sys.exit()
