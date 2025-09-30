#!/usr/bin/env python3
"""
main.py
SSH into a list of Linux lab VMs and collect network configuration / troubleshooting outputs.
Saves output per-host as backups/<hostname>_<timestamp>.txt

Security notes:
 - inventory.json should contain host, username, password (or use SSH keys)
 - inventory.json is added to .gitignore in the repo template below
"""

import json
import argparse
import os
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
import paramiko
import socket

# -----------------------
# Configuration
# -----------------------
DEFAULT_COMMANDS = [
    "hostname",
    "uname -a",
    "uptime",
    "ip addr",
    "ip route",
    "ss -tunap",
    "cat /etc/hosts || true",
    "cat /etc/network/interfaces || true",
    "sudo iptables-save || true"
]

# -----------------------
# Helpers
# -----------------------
def load_inventory(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"Inventory not found: {path}")
    with path.open() as fh:
        data = json.load(fh)
    if not isinstance(data, list):
        raise ValueError("Inventory must be a JSON array.")
    return data

def make_client(host, port, username, password, timeout=10):
    client = paramiko.SSHClient()
    # Auto add host keys — for lab use only. In production, use known_hosts.
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, port=port, username=username, password=password, timeout=timeout)
    return client

def gather_for_device(device, commands, backups_dir):
    host = device.get("host")
    port = int(device.get("port", 22))
    username = device.get("username")
    password = device.get("password")
    name = f"{host}".replace(":", "_")

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_path = backups_dir / f"{name}_{ts}.txt"
    backups_dir.mkdir(parents=True, exist_ok=True)

    header = f"# Backup for {host} at {ts} UTC\n"

    try:
        client = make_client(host, port, username, password)
    except (paramiko.ssh_exception.AuthenticationException, paramiko.ssh_exception.SSHException) as e:
        return {"host": host, "ok": False, "error": f"SSH error: {e}"}
    except socket.timeout as e:
        return {"host": host, "ok": False, "error": f"Timeout: {e}"}
    except Exception as e:
        return {"host": host, "ok": False, "error": str(e)}

    try:
        with out_path.open("w", encoding="utf-8") as fh:
            fh.write(header + "\n")
            for cmd in commands:
                fh.write(f"\n$ {cmd}\n")
                stdin, stdout, stderr = client.exec_command(cmd, timeout=30)
                # Wait for command to finish and read output
                stdout_text = stdout.read().decode("utf-8", errors="replace")
                stderr_text = stderr.read().decode("utf-8", errors="replace")
                if stdout_text:
                    fh.write(stdout_text)
                if stderr_text:
                    fh.write("\n[stderr]\n")
                    fh.write(stderr_text)
        client.close()
        return {"host": host, "file": str(out_path), "ok": True}
    except Exception as e:
        try:
            client.close()
        except Exception:
            pass
        return {"host": host, "ok": False, "error": str(e)}

# -----------------------
# CLI
# -----------------------
def main():
    parser = argparse.ArgumentParser(description="Collect network state from lab VMs via SSH")
    parser.add_argument("--inventory", "-i", type=Path, default=Path("inventory.json"),
                        help="Path to inventory JSON (array of device objects)")
    parser.add_argument("--backup-dir", "-b", type=Path, default=Path("backups"),
                        help="Directory to store backups")
    parser.add_argument("--concurrency", "-j", type=int, default=1,
                        help="Number of parallel SSH connections")
    parser.add_argument("--commands", "-c", nargs="*", default=None,
                        help="Commands to run (default set used if omitted)")
    args = parser.parse_args()

    devices = load_inventory(args.inventory)
    commands = args.commands if args.commands else DEFAULT_COMMANDS
    results = []

    if args.concurrency > 1:
        with ThreadPoolExecutor(max_workers=args.concurrency) as ex:
            futures = {ex.submit(gather_for_device, d, commands, args.backup_dir): d for d in devices}
            for fut in as_completed(futures):
                results.append(fut.result())
    else:
        for d in devices:
            results.append(gather_for_device(d, commands, args.backup_dir))

    ok = [r for r in results if r.get("ok")]
    fail = [r for r in results if not r.get("ok")]

    print(f"Completed: {len(ok)} succeeded, {len(fail)} failed")
    if fail:
        print("Failures:")
        for f in fail:
            print(" -", f)

if __name__ == "__main__":
    main()
