# PortLens Beginner Guide

This guide assumes you know nothing. Follow it from top to bottom. Examples use **Windows + PowerShell**, with Linux notes where they differ.

## Contents

1. [What you have](#1-what-you-have)
2. [Do I need to change any code?](#2-do-i-need-to-change-any-code)
3. [Set up on your computer](#3-set-up-on-your-computer)
4. [Add the files to your Git repo](#4-add-the-files-to-your-git-repo)
5. [Use the port scanner](#5-use-the-port-scanner)
6. [Use Guard mode](#6-use-guard-mode)
7. [Where you can (and cannot) use this tool](#7-where-you-can-and-cannot-use-this-tool)
8. [Troubleshooting](#8-troubleshooting)

---

## 1. What you have

| File | What it does |
|---|---|
| `port_scanner.py` | **Scanner.** Checks which ports are open on a computer. |
| `guard.py` | **Guard.** Watches your own computer for people probing it, flags them, and can block them. |
| `requirements.txt` | Lists extra packages to install. PortLens needs **none**, so this file only holds notes. |
| `README.md` | Short project overview. |
| `LICENSE` | MIT license (you must put your name in it). |
| `.gitignore` | Tells Git which files to leave out of the repo. |
| `GUIDE.md` | This file. |

**Key idea:** a *port* is like a numbered door on a computer. Each service (website, remote desktop, SSH) uses its own door. The scanner knocks on doors to see which are open. Guard waits behind fake doors and notes who knocks.

---

## 2. Do I need to change any code?

**Mostly no.** The tool detects your operating system by itself:

- Windows uses `netsh` to block IPs.
- Linux uses `iptables` to block IPs.
- macOS can scan and flag, but cannot block automatically.

Everything you might want to customize can be done with **command options**, with no code editing. Only do the optional edits below if you want different permanent defaults.

### Things you should change (not code)

1. **`LICENSE`**: replace `<Your Name>` with your real name.
2. **`README.md`**: replace `<your-username>` with your GitHub username in the clone URLs.

### Optional code edits

**How to open a file for editing:** right-click the file, choose *Open with*, then *Notepad* (or VS Code if you have it). Edit, then press `Ctrl+S`.

#### A. Change the default trap ports for Guard

Open `guard.py` and find this line near the top (use `Ctrl+F` and search for `DEFAULT_TRAP_PORTS`):

```python
DEFAULT_TRAP_PORTS = "21,23,2222,5900,8081,8888"
```

Replace the numbers with ports you want to use as traps. Rules for choosing:

- Pick ports **not already used** by programs on your computer. Used ports are skipped automatically with a message.
- Separate ports with commas, no spaces. Ranges like `8081-8090` also work.
- Do not use port `80` or `443` if you run a website on this machine.

To see which ports are already in use on Windows:

```powershell
netstat -ano | findstr LISTENING
```

#### B. Change the default scan range in the scanner

Open `port_scanner.py`, search for `"1-1024"` and change it, for example to `"1-10000"`:

```python
parser.add_argument("-p", "--ports", default="1-1024",
```

#### C. Change where flagged IPs are saved

By default they go into `flagged_ips.json` next to `guard.py`. To use another place, set an environment variable instead of editing code:

```powershell
$env:PORTLENS_DB = "C:\Users\YourName\Documents\flagged.json"
```

#### D. Change when Guard flags someone

Do **not** edit the code. Use options:

```powershell
python guard.py listen --threshold 3 --scan-threshold 2 --window 120
```

- `--threshold 3`: flag after 3 attempts
- `--scan-threshold 2`: flag when 2 different ports are touched
- `--window 120`: counted within 120 seconds

### Step that depends on your network: whitelist your router

Your router and your own devices must never be blocked. Find your router address:

```powershell
ipconfig
```

Look for **Default Gateway** (often `192.168.0.1` or `192.168.1.1`). Then run:

```powershell
python guard.py whitelist add 192.168.1.1
```

Replace `192.168.1.1` with your gateway. Repeat for any other device you always trust (your phone, your other PC).

---

## 3. Set up on your computer

### Step 1: Install Python

1. Check if you have it:
   ```powershell
   python --version
   ```
   If you see `Python 3.9` or higher, skip to Step 2. If you get "not recognized", try `py --version`.
2. Otherwise download Python from https://www.python.org/downloads/ and run the installer.
3. **Tick "Add Python to PATH"** on the first screen, then click *Install Now*.
4. Close PowerShell, open a new one, and check `python --version` again.

### Step 2: Put the files in a folder

1. Create a folder, for example `C:\Users\YourName\portlens`.
2. Put these files in it: `port_scanner.py`, `guard.py`, `requirements.txt`, `README.md`, `LICENSE`, `.gitignore`, `GUIDE.md`.
   > `guard.py` and `port_scanner.py` **must be in the same folder**.

### Step 3: Open PowerShell inside that folder

Open the folder in File Explorer, click the address bar, type `powershell`, press Enter.

Or from any PowerShell window:

```powershell
cd C:\Users\YourName\portlens
```

### Step 4: (Optional) install requirements

```powershell
pip install -r requirements.txt
```

This does nothing harmful and installs nothing, because PortLens needs no extra packages.

### Step 5: Test that it works

```powershell
python port_scanner.py 127.0.0.1 -p 1-1024
python guard.py --help
```

If both print results or help text, you are ready.

### Opening PowerShell as Administrator (needed for blocking and reading logs)

Click Start, type `PowerShell`, right-click **Windows PowerShell**, choose **Run as administrator**, then `cd` to your folder again.

---

## 4. Add the files to your Git repo

**Use the same repo.** Guard is part of PortLens, so there is no reason to create a new one. Only create a second repo if you later want to publish Guard as a separate project.

### Step 1: Install Git (once)

```powershell
winget install --id Git.Git -e --source winget
```

Close and reopen PowerShell, then check:

```powershell
git --version
```

### Step 2: Tell Git who you are (once)

```powershell
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

### Step 3A: If your PortLens repo already exists on your computer

```powershell
cd C:\Users\YourName\portlens
git add .
git commit -m "Add Guard mode, guide and .gitignore"
git push
```

### Step 3B: If you have NOT created the repo yet

1. On https://github.com click **New repository**, name it `portlens`, leave everything else empty, click **Create**.
2. In PowerShell, inside your folder:

```powershell
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/portlens.git
git push -u origin main
```

GitHub may open a browser window asking you to sign in. Do that once.

### Important: never commit `flagged_ips.json`

It contains IP addresses of people who probed you. The included `.gitignore` already excludes it, so it will not be uploaded.

---

## 5. Use the port scanner

```powershell
python port_scanner.py <target> [options]
```

| Goal | Command |
|---|---|
| Scan your own PC (common ports) | `python port_scanner.py 127.0.0.1` |
| Scan specific ports | `python port_scanner.py 127.0.0.1 -p 22,80,443,3389` |
| Scan everything | `python port_scanner.py 127.0.0.1 -p 1-65535 -t 300` |
| Scan another device on your home network | `python port_scanner.py 192.168.1.20` |
| Try to read service banners | `python port_scanner.py 127.0.0.1 -b` |

**Reading the results:** every port listed is **open**. A port you do not recognize deserves a look. Common ones:

| Port | Usually |
|---|---|
| 22 | SSH (remote command line) |
| 80 / 443 | Website |
| 445 / 139 | Windows file sharing |
| 3389 | Windows Remote Desktop (RDP) |
| 3306 | MySQL database |

Remote Desktop (3389) open to the internet is a very common attack target. Close it if you do not use it.

---

## 6. Use Guard mode

Guard has two ways of catching intruders. Use either or both.

### Mode 1: Trap ports (`listen`)

```powershell
python guard.py listen
```

Guard opens decoy ports and waits. Real users never visit them, so anyone who touches several in a short time is probably scanning you. Stop with `Ctrl+C`.

**Windows will show a firewall popup**: click **Allow access**, otherwise knocks never reach Guard.

**How to test it safely:**

1. Run `python guard.py listen -p 8081,8082,8083` on your PC.
2. Find your PC's address with `ipconfig` (look for *IPv4 Address*).
3. From **another device on your network** (a second computer running PortLens, or a phone port-scanner app), scan your PC: `python port_scanner.py <your-PC-IP> -p 8081-8083`.
4. Guard prints `FLAGGED` and the other device's IP.

Scanning from the same PC (`127.0.0.1`) is deliberately ignored, because Guard never flags itself.

### Mode 2: Failed logins (`logs`)

Open PowerShell **as Administrator**, then:

```powershell
python guard.py logs --hours 24 --threshold 5
```

This reads Windows' own record of failed sign-ins and flags any IP with 5 or more failures in the last 24 hours. It only finds something if a service like Remote Desktop is reachable from outside. On a normal home PC behind a router, you will usually see nothing, which is good.

On Linux: `sudo python3 guard.py logs`

### Review, block, undo

```powershell
python guard.py list                           # who is flagged
python guard.py block 203.0.113.50 --dry-run   # preview, changes nothing
python guard.py block 203.0.113.50             # block (asks "y/N")
python guard.py unblock 203.0.113.50           # undo
```

Always run `--dry-run` first until you are comfortable. To see the blocks Windows created, open **Windows Defender Firewall with Advanced Security**, then **Inbound Rules**, and look for names starting with `PortLens_Block_`.

**If you ever block the wrong IP:** run `python guard.py unblock <ip>`, then `python guard.py whitelist add <ip>` so it never happens again.

---

## 7. Where you can (and cannot) use this tool

Port scanning is a normal skill used by network administrators and security professionals. The rule is simple: **only scan what you own or have permission to test.** Unauthorized scanning can break laws and the terms of internet providers and hosting companies.

### Fine to use on

- Your own computer, laptop, or Raspberry Pi
- Your home network and devices you own
- Your own server or VPS (check your provider's rules first; most allow scanning your own server)
- Virtual machines and practice labs you set up yourself
- Systems you have **written permission** to test, such as a client or employer who agreed in writing
- Deliberately vulnerable practice targets such as `scanme.nmap.org` (explicitly offered for testing; keep the scan small and polite)
- Training platforms that allow it, such as Hack The Box or TryHackMe, within their rules

### Do not use on

- Someone else's computer, home network, or website without permission
- Your school, university, or workplace network unless the IT team has approved it
- Random internet addresses "just to see"
- Public Wi-Fi or hotel networks

### Best places to use Guard

| Situation | Useful? |
|---|---|
| Linux VPS or server with SSH open to the internet | **Very.** Brute-force attempts are constant. |
| Windows PC or server with Remote Desktop exposed | **Very.** |
| Raspberry Pi or home server with port forwarding | Yes |
| Normal home PC behind a router | Little to find, but fine for learning and testing |

Guard is **one layer of defense**. For real servers also use strong passwords or keys, keep software updated, and keep a firewall on. Attackers can change IP addresses, so blocking one is not a full solution.

---

## 8. Troubleshooting

| Problem | Fix |
|---|---|
| `python` is not recognized | Reinstall Python and tick **Add Python to PATH**, or use `py` instead of `python`. |
| `git` is not recognized | Install Git (section 4), then reopen PowerShell. |
| `ModuleNotFoundError: port_scanner` | `guard.py` and `port_scanner.py` must be in the same folder, and you must run the command from that folder. |
| "Administrator rights are required" | Reopen PowerShell with **Run as administrator**. |
| Guard says "Skipping port ...: address already in use" | Another program uses that port. Pick different ports with `-p`. |
| Guard never flags anything | Allow Python in the Windows Firewall popup, and test from a different device (not `127.0.0.1`). |
| `logs` finds nothing on Windows | Run as Administrator. Having no failed logins is also a possible (good) result. |
| Scan seems slow | Lower the timeout: `--timeout 0.2`, or raise threads: `-t 300`. |
| PowerShell blocks scripts when activating a venv | Run `Set-ExecutionPolicy -Scope Process Bypass`, then try again. |
| Port scan shows nothing open on a device you know has services | The device's firewall may be hiding them. That is normal. |

Still stuck? Copy the exact error message and ask for help with it.
