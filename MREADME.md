# SQLInjector ✴️

A stealthy, stylish SQL injection vulnerability scanner and data extractor  
**Made with ❤️ by elGabir**

---

## Features

- **Stealth mode**: Random delays, user-agent switching to avoid easy detection
- **Stylish UI**: Cool colors, animated spinners, scorpion ASCII art
- **Automated Extraction**: Dumps table info if exploitable, saves all output
- **Sensitive Data Highlighting**: Finds lines with keywords: `admin`, `username`, `card`, `phone`, `email`, `log`, `auth`, `cookies`  
- **Easy one-command run**: Interactive prompt, minimal setup

---

## Usage Instructions

### 1. Clone and Install

```bash
# Clone this repo or copy Example.py and README.md into a folder
pip install requests colorama
```

### 2. Run the Tool

```bash
python Example.py
```

### 3. Interact

- **Paste target URL** (e.g., http://example.com/vuln.php)
- **Enter the GET parameter** to test (default is `id`)

### 4. Output

- **output.txt**: Full scan and extraction output  
- **sensitive_output.txt**: Only lines containing sensitive keywords (highlighted)

---

## Example Session

```plaintext
=== SQLInjector Stealth Scanner & Extractor ===
Paste target URL (e.g. http://site.com/vuln.php): http://testsite.com/item.php
URL parameter to test (default 'id'): item
[*] Running in stealth mode...

Scanning for SQLi... \
Scan complete!

Payload: ' OR 1=1-- --> VULNERABLE
Payload: " OR 1=1-- --> Not Vulnerable
...
[*] Vulnerability detected! Trying to extract data...
Extracting data... /
Extraction complete!

[*] Sensitive keywords found! Saving to sensitive_output.txt ...
[*] Sensitive Info Found:
   admin: root
   username: alice
   card: 1234-xxxx-xxxx-5678
...
```

---

## Recommended

- Only use against systems you have **explicit authorization** to test.
- Extend payloads and extraction in `Example.py` for more targets.
- Customize ASCII art, color themes, or UI as you wish!

---

## Credits

```plaintext
         ____            
        / . .\           
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
by elGabir
```
