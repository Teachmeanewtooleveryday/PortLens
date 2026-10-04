#!/usr/bin/env python3
"""
Simple multithreaded TCP port scanner.

Only scan hosts you own or have explicit permission to test.

Examples:
    python port_scanner.py 127.0.0.1
    python port_scanner.py 192.168.1.10 -p 1-1024
    python port_scanner.py example.local -p 22,80,443,8000-8100 -t 200 -b
"""

import argparse
import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def parse_ports(spec: str) -> list[int]:
    """Parse '22,80,100-200' into a sorted list of unique ports."""
    ports = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = part.split("-", 1)
            start, end = int(start), int(end)
            if start > end:
                raise ValueError(f"Invalid range: {part}")
            ports.update(range(start, end + 1))
        else:
            ports.add(int(part))
    if not ports or min(ports) < 1 or max(ports) > 65535:
        raise ValueError("Ports must be between 1 and 65535")
    return sorted(ports)


def service_name(port: int) -> str:
    try:
        return socket.getservbyport(port, "tcp")
    except OSError:
        return "unknown"


def grab_banner(sock: socket.socket) -> str:
    """Try to read a short banner from an open connection."""
    try:
        sock.settimeout(1.0)
        data = sock.recv(128)
        return data.decode(errors="replace").strip().replace("\n", " ")
    except (socket.timeout, OSError):
        return ""


def scan_port(host: str, port: int, timeout: float, banner: bool):
    """Return (port, banner) if open, otherwise None."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            if sock.connect_ex((host, port)) == 0:
                return port, (grab_banner(sock) if banner else "")
    except OSError:
        pass
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Simple TCP port scanner")
    parser.add_argument("target", help="Hostname or IPv4 address")
    parser.add_argument("-p", "--ports", default="1-1024",
                        help="Ports, e.g. 80,443,1-1024 (default: 1-1024)")
    parser.add_argument("-t", "--threads", type=int, default=100,
                        help="Number of threads (default: 100)")
    parser.add_argument("--timeout", type=float, default=0.5,
                        help="Connection timeout in seconds (default: 0.5)")
    parser.add_argument("-b", "--banner", action="store_true",
                        help="Attempt to grab service banners")
    args = parser.parse_args()

    try:
        ports = parse_ports(args.ports)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    try:
        ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print(f"Error: could not resolve {args.target}", file=sys.stderr)
        return 2

    print(f"Scanning {args.target} ({ip}) - {len(ports)} ports")
    start = time.time()
    results = []

    try:
        with ThreadPoolExecutor(max_workers=args.threads) as pool:
            futures = [pool.submit(scan_port, ip, p, args.timeout, args.banner)
                       for p in ports]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)
    except KeyboardInterrupt:
        print("\nScan interrupted.")

    results.sort()
    print(f"\n{'PORT':<8}{'SERVICE':<16}BANNER")
    for port, banner in results:
        print(f"{port:<8}{service_name(port):<16}{banner}")

    print(f"\n{len(results)} open port(s) found in {time.time() - start:.2f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
