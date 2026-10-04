# PortLens

A fast, lightweight, multithreaded TCP port scanner written in Python. No third-party dependencies required.

> **Legal notice:** Only scan systems you own or have explicit written permission to test. Unauthorized port scanning may be illegal in your jurisdiction. You are responsible for how you use this tool.

## Features

- Multithreaded TCP connect scanning
- Flexible port selection (single ports, lists, and ranges)
- Service name detection for common ports
- Optional banner grabbing
- Configurable timeout and thread count
- Pure Python standard library

## Requirements

- Python 3.9 or newer
- Git (optional, only for cloning)

## Installation

### Linux / macOS

```bash
# Clone the repository
git clone https://github.com/<your-username>/portlens.git
cd PortLens

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
