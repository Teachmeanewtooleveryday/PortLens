# PortLens

A fast, lightweight, multithreaded TCP port scanner written in Python. No third-party dependencies required.

> **Legal notice:** Only scan systems you own or have explicit written permission to test. Unauthorized port scanning may be illegal in your jurisdiction. You are responsible for how you use this tool.

> **New to this?** Read the step-by-step [Beginner Guide](GUIDE.md).

## Features

- Multithreaded TCP connect scanning
- Flexible port selection (single ports, lists, and ranges)
- Service name detection for common ports
- Optional banner grabbing
- Configurable timeout and thread count
- **Guard mode:** detect who is probing your machine, flag them, and optionally block them
- Pure Python standard library

## Requirements

- Python 3.9 or newer
- Git (optional, only for cloning)

## Installation

### Linux / macOS

```bash
# Clone the repository
git clone https://github.com/<your-username>/portlens.git
cd portlens

# (Optional) create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies (none required, but kept for future additions)
pip install -r requirements.txt
```

### Windows (PowerShell)

```powershell
git clone https://github.com/<your-username>/portlens.git
cd portlens

# (Optional) create and activate a virtual environment
python -m venv venv
venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### Without Git

Download `port_scanner.py` and run it directly with Python. Nothing else needs to be installed.

## Usage

```bash
python port_scanner.py <target> [options]
```

| Option | Description | Default |
|---|---|---|
| `target` | Hostname or IPv4 address | required |
| `-p`, `--ports` | Ports to scan, e.g. `80,443,1-1024` | `1-1024` |
| `-t`, `--threads` | Number of concurrent threads | `100` |
| `--timeout` | Connection timeout in seconds | `0.5` |
| `-b`, `--banner` | Attempt to grab service banners | off |
| `-h`, `--help` | Show help | |

### Examples

```bash
# Scan the default port range on localhost
python port_scanner.py 127.0.0.1

# Scan specific ports and a range
python port_scanner.py 192.168.1.10 -p 22,80,443,8000-8100

# Scan all ports with more threads and a shorter timeout
python port_scanner.py 192.168.1.10 -p 1-65535 -t 300 --timeout 0.3

# Grab banners from open ports
python port_scanner.py scanme.example.com -p 21,22,25,80 -b
```

### Sample output

```
Scanning 127.0.0.1 (127.0.0.1) - 11 ports

PORT    SERVICE         BANNER
8765    unknown

1 open port(s) found in 1.00s
```

## Guard mode: detect, flag and block intruders

`guard.py` protects your own machine. It finds IPs that scan your ports or repeatedly fail to log in, flags them, and can block them with the operating system firewall. Keep it in the same folder as `port_scanner.py`.

Flagged IPs are stored in `flagged_ips.json` next to the script. Set the `PORTLENS_DB` environment variable to use a different location.

### 1. Trap-port listener

Opens unused ports and flags any IP that touches several of them quickly (port scan) or hits them repeatedly.

```bash
python guard.py listen -p 21,23,2222,5900
python guard.py listen --threshold 5 --scan-threshold 3 --window 60
```

Ports already used by real services are skipped automatically. On Windows, allow Python through the firewall when prompted, otherwise connection attempts never reach the listener.

### 2. Failed-login detection

Reads your system logs and flags IPs with too many failed logins (for example RDP or SSH brute-force attempts).

```bash
# Windows (run PowerShell as Administrator): Security log, event 4625
python guard.py logs --hours 24 --threshold 5

# Linux (run with sudo): /var/log/auth.log or /var/log/secure
sudo python3 guard.py logs --threshold 5
sudo python3 guard.py logs --log-file /path/to/auth.log
```

### 3. Review and block

```bash
python guard.py list                          # show flagged IPs
python guard.py block 203.0.113.50 --dry-run  # preview the firewall command
python guard.py block 203.0.113.50            # block (asks for confirmation)
python guard.py block --all-flagged           # block everything flagged
python guard.py unblock 203.0.113.50          # remove the block
```

Blocking needs **Administrator** (Windows, uses `netsh advfirewall`) or **root** (Linux, uses `iptables`/`ip6tables`). macOS can flag but not block automatically.

Add `--auto-block` to `listen` or `logs` to block flagged IPs without a prompt.

### Safety features

- Blocking asks for confirmation unless you pass `--yes` or `--auto-block`.
- Loopback addresses and your machine's own addresses are never flagged or blocked.
- Private LAN addresses are never auto-blocked, so a misbehaving router or PC cannot lock you out.
- Use the whitelist for IPs that must always be safe (your router, office, VPN):

```bash
python guard.py whitelist add 203.0.113.99
python guard.py whitelist list
python guard.py whitelist remove 203.0.113.99
```

### Limitations

- Only IPs that actually reach your machine can be seen. Traffic dropped by a router or firewall upstream will not show up.
- Attackers can spoof or rotate IP addresses, so treat blocking as one layer of defense, not a complete solution.
- Failed-login detection on Linux only parses SSH "Failed password" entries.

## How it works

PortLens performs a full TCP connect scan. For each port it attempts a complete TCP handshake using `connect_ex()`. If the connection succeeds, the port is reported as open. Scans run in parallel using a thread pool, which keeps large ranges fast.

Because it uses regular connections, it needs no administrator privileges, but it is also easier to detect than stealth scan techniques.

## Roadmap

- [ ] UDP scanning
- [ ] JSON / CSV export
- [ ] Progress bar
- [ ] IPv6 support
- [ ] CIDR range scanning

## Contributing

Contributions are welcome.

```bash
git checkout -b feature/my-feature
git commit -m "Add my feature"
git push origin feature/my-feature
```

Then open a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
