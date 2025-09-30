# ssh-network-auditor

This project demonstrates **network automation** by connecting to multiple Linux VMs over SSH, collecting system/network information, and saving it as timestamped backup files.

- **Version 1 (Manual Lab Setup)** – VirtualBox VMs were created and configured manually.  
- **Version 2 (Automated with Vagrant)** – The lab environment is fully reproducible using Vagrant. With a single command, two Kali Linux VMs are provisioned and ready for automation.


##  Project Purpose
Network engineers often need to back up device or server configurations. Doing this manually is time-consuming and error-prone.  
This project automates the process:
- Connects to multiple hosts via SSH  
- Runs diagnostic/network commands  
- Saves the results into organized backup files  

---

## Tools & Technologies
- **Python 3** – scripting language  
- **Paramiko** – SSH automation library  
- **JSON** – inventory of devices/credentials  
- **Vagrant** – automated VM provisioning  
- **VirtualBox** – VM provider for Vagrant  
- **Git & GitHub** – version control and documentation  

1. Prerequisites

    - Install VirtualBox
    - Install Vagrant
    - Install Python 3 (with paramiko):

```bash
pip install -r requirements.txt

```

2. Start the Lab

Run this inside the project folder:
```bash
vagrant up
```

This will:

    - Download the Kali Linux Vagrant box (first time only)
    - Create two VMs (kali-server at 192.168.56.101 and kali-client at 192.168.56.102)
    - Configure them on a private network

You can test access:
```bash
vagrant ssh kali-server
vagrant ssh kali-client
```

3. Configure Inventory

Use the default Vagrant credentials (vagrant / vagrant):
```bash

[
  {
    "host": "192.168.56.101",
    "username": "vagrant",
    "password": "vagrant"
  },
  {
    "host": "192.168.56.102",
    "username": "vagrant",
    "password": "vagrant"
  }
]
```

4. Run the Python Script
```bash
python main.py -i inventory.json
```

5. Check Backups
Outputs are saved into backups/:
backups/
├── 192.168.56.101_20250930T120000Z.txt
├── 192.168.56.102_20250930T120500Z.txt