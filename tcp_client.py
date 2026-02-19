"""
countless times during pen tests, we have needed to whip up a TCP client
to test for services, send garbage data, fuzz.
if you're working within confines of large envt, you wont have thw luxury
of usind networking tools or compilers and sometimes you'll be missing
the absolute basics like the ability to copy/paste or connect to the interner
this is where being able to quickly create a TCP client comes in extremely handy
"""

import socket

target_host = "127.0.0.1"
target_port = 9998

# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""we create a socket object with AF_INET and SOCK_STREAM paramaters
AF_INET - indicates we'll use a standard IPv4 address or Hostname
SOCK_STREAM - indicates this will be a TCP client
"""

# connect the client
client.connect((target_host, target_port))

# send some data
# /client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")
client.send(b"Hello, server!!")

# receive some data
response = client.recv(4096)
print(f"Server Response : {response.decode()}")
client.close()

"""
the code above makes some serious assumptions about sockets
1.our connection will always succeed
2.the server expects us to send data first(some servers expects to send data to you first and await ypur response)
3.the server will always return data to us in timely fashion

we make these assumptions largely for simplicity sake
"""