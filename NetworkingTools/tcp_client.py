"""
Countless times during pen test, you need to whip up TCP cleint to test for

services, send garbage data, fuzz, or perform any other related tasks

if u are working within the confines of large enterprise environment, you won't have

the luxury of using networking tools or compilers and sometimes you'll be missing

the absolute basiss like the ability to copy/paste

This is where being able to create TCP client comes extremely i handy

"""

import socket

target_host = "127.0.0.1"
target_port = 9998

# create a socket object
""" AF_INET(indicats this is IPv4 address or hostname)  SOCK_STREAM(Indicates this will be a TCP client)"""
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
client.connect((target_host,target_port))

# send some data
client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

# receive some data
response = client.recv(4096)

print(response.decode())

# close connection
client.close()


"""
NB: This code makes some serious assumptions about the socket that you definitely want to be aware of

1. first one is our connection will always succeed
2. second is that the server expects us to send data first(some servers expect to send data t you first and wait for your response)
3.the server will always return data to us in a timly fashion
"""