# 🔐 Python Cybersecurity Toolkit

A collection of hands-on cybersecurity tools built in Python to understand offensive and defensive security concepts from the ground up. Each tool was written from scratch as part of my self-directed learning journey toward a career in Cyber Security.

> ⚠️ **Disclaimer:** All tools in this repository are built strictly for **educational purposes** and **controlled lab environments**. Do not use against systems you do not own or have explicit permission to test. The author takes no responsibility for misuse.

---

## 📁 Tools Overview

### 🖧 1. Netcat Clone (`netcat.py`)
A fully functional Python reimplementation of the classic Netcat networking utility.

**Features:**
- Interactive command shell over TCP
- Remote file upload
- Execute commands on a remote machine
- Listen mode and connect mode
- Multithreaded client handling

**Usage:**
```bash
# Start a command shell listener
python netcat.py -t 192.168.1.108 -p 5555 -l -c

# Upload a file to a remote host
python netcat.py -t 192.168.1.108 -p 5555 -l -u=myfile.txt

# Execute a command on connect
python netcat.py -t 192.168.1.108 -p 5555 -l -e="cat /etc/passwd"

# Connect to a listener
python netcat.py -t 192.168.1.108 -p 5555
```

---

### 🔑 2. File Encryptor / Ransomware Simulator (`ransom.py`)
An educational tool demonstrating how ransomware operates at a cryptographic level.

**Features:**
- Password-based key derivation using **Scrypt** with random salt generation
- AES-grade symmetric encryption via **Fernet**
- Encrypts and decrypts individual files or entire folder trees recursively
- Salt stored separately for key reconstruction

**Usage:**
```bash
# Encrypt a file
python ransom.py path/to/file.txt -e -s 16

# Decrypt a file
python ransom.py path/to/file.txt -d

# Encrypt an entire folder
python ransom.py path/to/folder -e
```

**Why it was built:** To understand how encryption-based attacks work so defenders can detect, prevent, and respond to them effectively.

---

### ⌨️ 3. Keylogger (`keylogger.py`)
An educational keystroke capture tool demonstrating how credential-theft malware operates.

**Features:**
- Captures all keyboard input including special keys
- Reports logs via **email (SMTP/TLS)** or local text file at configurable intervals
- Runs as a background daemon thread
- Timestamps each logging session

**Usage:**
```bash
python keylogger.py  # Configure report method inside the script
```

**Why it was built:** To understand endpoint monitoring blind spots and how attackers capture credentials — essential knowledge for building effective defences.

---

### 🐚 4. Reverse Shell (`shell.py`)
A reverse shell server demonstrating firewall bypass techniques used in penetration testing.

**Features:**
- Target machine initiates the outbound connection (bypasses inbound firewall rules)
- Attacker machine listens for incoming connections and issues commands
- Demonstrates how attackers maintain access to compromised systems

**Why it was built:** To understand post-exploitation techniques and how network defences can be configured to detect and block reverse shell traffic.

---

### 🌐 5. TCP/UDP Networking Toolkit

A set of low-level network communication tools built to understand protocol fundamentals used in penetration testing.

| File | Description |
|------|-------------|
| `tcp_client.py` | Basic TCP client — connects, sends, and receives data |
| `tcpserver.py` | Multithreaded TCP server — handles multiple clients concurrently |
| `tcp_proxy.py` | TCP proxy with hex dump — intercepts and displays raw traffic between hosts |
| `udpclient.py` | UDP client — connectionless datagram communication |

**Usage:**
```bash
# Run the TCP server
python tcpserver.py

# Connect with the TCP client
python tcp_client.py
```

---

## 🛠️ Tech Stack

| Technology | Usage |
|------------|-------|
| Python 3 | All tools |
| `socket` | Network communication |
| `threading` | Concurrent connections |
| `cryptography` (Fernet, Scrypt) | File encryption |
| `keyboard` | Keystroke capture |
| `smtplib` | Email reporting |
| `argparse` | CLI interfaces |
| `subprocess` | Remote command execution |

---

## 🚀 Getting Started

### Prerequisites
```bash
pip install cryptography keyboard
```

### Clone the repo
```bash
git clone https://github.com/Shaker-maker/ctf-writeups.git
cd ctf-writeups
```

---

## 📚 Learning Resources

These tools were built with reference to:
- *Black Hat Python* by Justin Seitz & Tim Arnold
- Cisco Networking Academy — Introduction to Cybersecurity
- TryHackMe learning paths
- OWASP WebGoat & DVWA labs

---

## 👤 Author

**Alvin Wainaina Mwangi**  
Computer Science Student — Multimedia University of Kenya  
📧 wainainaalvin76@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/alvin-w-99a49a306)

---

*Built as part of an active self-directed cybersecurity learning journey — 2024/2025*
