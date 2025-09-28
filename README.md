# ssh-network-auditor
Automates SSH collection of network state (IP config, routes, sockets, system info) from Linux-based lab devices. Built with Python &amp; Paramiko.

# Kali VM Network Backups (Lab)

This project demonstrates how to build a small virtual lab (two Kali VMs) and automate the collection of networking state from the lab using SSH. The goal is to show practical networking and automation skills in a reproducible way.

> **Important:** do **not** commit `inventory.json` with real credentials. Keep `inventory.example.json` in the repo and create a local `inventory.json` for testing.

## What this project does
- Collects network information and system state from two Kali VMs via SSH.
- Saves outputs (ip addresses, routes, socket lists, config files) as timestamped files in `backups/`.
- Demonstrates VM networking, SSH setup, and automation using Python + Paramiko.

## Lab architecture
- Kali-server (VM) — host: e.g., `192.168.56.102`
- Kali-client (VM) — host: e.g., `192.168.56.103`
- Both VMs attached to the same VirtualBox **Host-Only** network (or Internal network) so they share an L2/L3 segment.

## Prerequisites
- VirtualBox (or another hypervisor)
- Two Kali Linux VMs (Kali-server, Kali-client)
- Python 3.8+ on the host machine (or the VM chosen as controller)

## Steps to recreate the lab (concise)
1. Create two Kali VMs in VirtualBox.
2. Set network adapters:
   - Adapter 1: Host-only adapter (`vboxnet0`) for both VMs.
   - (Optional) Adapter 2: NAT for internet access.
3. Inside each VM:
   ```bash
   sudo apt update
   sudo apt install -y openssh-server
   sudo systemctl enable --now ssh
4. Assign temporary IPs (example):
    ```bash
    sudo ip addr add 192.168.56.101/24 dev eth0   # on Kali-server
    sudo ip addr add 192.168.56.102/24 dev eth0   # on Kali-client

5. Confirm connectivity from the host:
   ```bash
    ping -c3 192.168.56.102
    ping -c3 192.168.56.103
    ssh user@192.168.56.102

### Using the automation script

1. Create and activate a Python virtualenv:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt


2. Copy inventory.example.json → inventory.json and fill with your IPs & credentials.

3. Run:
    ```bash 
    python main.py --inventory inventory.json


4. Outputs will be in backups/ with files named <host>_YYYYMMDDTHHMMSSZ.txt.

Inventory format

inventory.json is a JSON array. Example:

    [
    {
        "host": "192.168.56.101",
        "port": 22,
        "username": "kaliuser",
        "password": "kaliPassword"
    }
    ]

## What the script collects (default)

    hostname
    uname -a
    uptime
    ip addr
    ip route
    ss -tunap
    /etc/hosts
    /etc/network/interfaces
    iptables-save (if available; may require sudo)

## Security notes

    The script uses paramiko.AutoAddPolicy() to automatically accept SSH host keys — fine in a private lab but not secure for production.

    For production-like repos, prefer SSH keys (no passwords) and a proper known_hosts/inventory approach.

    Never commit inventory.json with plaintext credentials.

## Possible improvements / next steps

    Switch to SSH key authentication and remove passwords from inventory.

    Add a small web UI or simple Flask app to view backups.

    Automate lab provisioning with Vagrant or Ansible.

    Show diffs between backups (e.g., nightly job) and commit diffs to a private Git or dashboard.
