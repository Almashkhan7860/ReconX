#!/usr/bin/env python3
# ============================================
#   ReconX - OSINT & Recon Tool
#   By: Almash Coder
#   For: Educational & CTF Purposes Only
# ============================================

import socket
import requests
import sys
import json
from colorama import Fore, Style, init

# Advanced libraries handles inside try blocks to prevent crash if not installed
try:
    import whois
except ImportError:
    whois = None

try:
    import dns.resolver
except ImportError:
    dns.resolver = None

init(autoreset=True)

BANNER = f"""
{Fore.GREEN}
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗  ██╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║╚██╗██╔╝
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║ ╚███╔╝ 
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║ ██╔██╗ 
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██╔╝ ██╗
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝
{Fore.YELLOW}      OSINT & Recon Tool | By Almash Coder
{Fore.RED}      [ Educational & CTF Purposes Only ]
{Style.RESET_ALL}
"""

def get_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        print(f"{Fore.GREEN}[✓] IP Address : {ip}{Style.RESET_ALL}")
        return ip
    except Exception:
        print(f"{Fore.RED}[!] IP nahi mila{Style.RESET_ALL}")
        return None

def ip_info(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = r.json()
        if data.get("status") == "success":
            print(f"{Fore.CYAN}")
            print(f"[✓] Country   : {data.get('country')}")
            print(f"[✓] City      : {data.get('city')}")
            print(f"[✓] Region    : {data.get('regionName')}")
            print(f"[✓] ISP       : {data.get('isp')}")
            print(f"[✓] Org       : {data.get('org')}")
            print(f"[✓] Timezone  : {data.get('timezone')}")
            print(f"[✓] Latitude  : {data.get('lat')}")
            print(f"[✓] Longitude : {data.get('lon')}")
            print(Style.RESET_ALL)
        else:
            print(f"{Fore.RED}[!] Invalid IP mapping metadata.{Style.RESET_ALL}")
    except Exception:
        print(f"{Fore.RED}[!] IP info nahi mila{Style.RESET_ALL}")

def whois_lookup(domain):
    if not whois:
        print(f"{Fore.RED}[!] Python 'python-whois' module not installed. Run: pip install python-whois{Style.RESET_ALL}")
        return
    try:
        w = whois.whois(domain)
        print(f"{Fore.CYAN}")
        print(f"[✓] Domain Name  : {w.get('domain_name')}")
        print(f"[✓] Registrar    : {w.get('registrar')}")
        print(f"[✓] Created      : {w.get('creation_date')}")
        print(f"[✓] Expires      : {w.get('expiration_date')}")
        print(f"[✓] Updated      : {w.get('updated_date')}")
        print(f"[✓] Name Servers : {w.get('name_servers')}")
        print(Style.RESET_ALL)
    except Exception:
        print(f"{Fore.RED}[!] Whois info nahi mila{Style.RESET_ALL}")

def dns_lookup(domain):
    if not dns.resolver:
        print(f"{Fore.RED}[!] Python 'dnspython' module not installed. Run: pip install dnspython{Style.RESET_ALL}")
        return
    record_types = ["A", "MX", "NS", "TXT", "CNAME"]
    print(f"{Fore.CYAN}")
    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            for ans in answers:
                print(f"[✓] {rtype:6} : {ans}")
        except Exception:
            print(f"[-] {rtype:6} : Nahi mila")
    print(Style.RESET_ALL)

def http_headers(domain):
    try:
        r = requests.get(f"http://{domain}", timeout=5, headers={'User-Agent': 'Mozilla/5.0'})
        print(f"{Fore.CYAN}")
        for key, val in r.headers.items():
            print(f"[✓] {key}: {val}")
        print(Style.RESET_ALL)
    except Exception:
        print(f"{Fore.RED}[!] Headers nahi mile{Style.RESET_ALL}")

def subdomain_scan(domain):
    subdomains = [
        "www", "mail", "ftp", "admin", "blog",
        "dev", "test", "api", "shop", "portal",
        "cpanel", "webmail", "smtp", "pop", "ns1", "ns2"
    ]
    print(f"{Fore.CYAN}[*] Subdomains check ho rahe hain...{Style.RESET_ALL}\n")
    found = []
    for sub in subdomains:
        try:
            full = f"{sub}.{domain}"
            ip = socket.gethostbyname(full)
            print(f"{Fore.GREEN}[✓] Found : {full} → {ip}{Style.RESET_ALL}")
            found.append(full)
        except Exception:
            pass
    if not found:
        print(f"{Fore.RED}[!] Koi subdomain nahi mila{Style.RESET_ALL}")

def full_scan(domain):
    print(f"\n{Fore.YELLOW}{'═'*50}")
    print(f"  🔍 Full Recon: {domain}")
    print(f"{'═'*50}{Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}[1] IP Address{Style.RESET_ALL}")
    ip = get_ip(domain)

    if ip:
        print(f"\n{Fore.YELLOW}[2] Location Info{Style.RESET_ALL}")
        ip_info(ip)

    print(f"\n{Fore.YELLOW}[3] WHOIS Info{Style.RESET_ALL}")
    whois_lookup(domain)

    print(f"\n{Fore.YELLOW}[4] DNS Records{Style.RESET_ALL}")
    dns_lookup(domain)

    print(f"\n{Fore.YELLOW}[5] HTTP Headers{Style.RESET_ALL}")
    http_headers(domain)

    print(f"\n{Fore.YELLOW}[6] Subdomains{Style.RESET_ALL}")
    subdomain_scan(domain)

    print(f"\n{Fore.GREEN}[✓] Full Scan Complete!{Style.RESET_ALL}")

def main():
    print(BANNER)
    while True:
        print(f"\n{Fore.CYAN}{'─'*45}")
        print(f"  1. 🌐 IP Address Nikalo")
        print(f"  2. 📍 IP Location Info")
        print(f"  3. 📋 WHOIS Lookup")
        print(f"  4. 🔎 DNS Records")
        print(f"  5. 📡 HTTP Headers")
        print(f"  6. 🔍 Subdomain Scanner")
        print(f"  7. 💥 Full Scan (Sab ek saath)")
        print(f"  8. 🚪 Exit")
        print(f"{'─'*45}{Style.RESET_ALL}")

        choice = input(f"\n{Fore.YELLOW}[ReconX]> {Style.RESET_ALL}").strip()

        if choice in ["1","2","3","4","5","6","7"]:
            domain = input(f"{Fore.YELLOW}Domain daalo (e.g. google.com): {Style.RESET_ALL}").strip()
            # Clean protocol layers safely
            domain = domain.replace("https://","").replace("http://","").replace("www.","").split('/')[0]

            if not domain:
                print(f"{Fore.RED}[!] Domain query empty!{Style.RESET_ALL}")
                continue

            if choice == "1": get_ip(domain)
            elif choice == "2":
                ip = get_ip(domain)
                if ip: ip_info(ip)
            elif choice == "3": whois_lookup(domain)
            elif choice == "4": dns_lookup(domain)
            elif choice == "5": http_headers(domain)
            elif choice == "6": subdomain_scan(domain)
            elif choice == "7": full_scan(domain)

        elif choice == "8":
            print(f"{Fore.RED}\n[!] Thanks for use Bro ! 👋{Style.RESET_ALL}")
            sys.exit()
        else:
            print(f"{Fore.RED}[!] Wrong choice!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
