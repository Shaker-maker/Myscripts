# Python Programming for Hackers and Pentesters

> A collection of Python scripts designed for ethical hackers and penetration testers, focusing on **low-level network interactions**, **tools for testing services**, and **custom scripts** for penetration testing tasks.

## 📡 What's Inside

This repository contains Python scripts that assist in penetration testing and network security assessments. Whether you're in a **restricted environment** or just need to quickly test networking services, these tools have you covered.

### 🧰 Tools Included

| File              | Description                               |
|-------------------|-------------------------------------------|
| `tcp_client.py`   | A raw TCP client for sending and receiving packets over TCP connections. |
| `tcp_server.py`   | A multithreaded TCP server that listens for incoming connections and logs data. |
| `udp_client.py`   | A simple UDP client for sending and receiving datagrams. |
| `intro.txt`       | A quick guide on usage in enterprise pentests and low-level network testing. |

---

## ⚙️ How to Use

### Run TCP Server (listener)

```bash
python tcp_server.py


Send Request via TCP Client
bash

python tcp_client.py

Send Datagram via UDP Client
bash
python udp_client.py

Note: You can also modify the tcp_client.py to test external services like www.google.com by sending raw HTTP headers.


⚔️ Why This Matters
"Sometimes, you're deep in an enterprise network with no tools, no GUI, and no way to copy-paste... just a terminal and your wits."
This repo serves as your Swiss Army knife for when common tools like nmap, netcat, or Wireshark aren't available. It's built for hackers and pentesters who need quick solutions.


👨🏽‍💻 Author
Alvin — @Shaker-maker

Ethical hacker. Python enthusiast. Focused on low-level control and creative recon.



☠️ Disclaimer
This repo is for educational and ethical hacking purposes only. Do not use these scripts for unauthorized access or malicious activities.


