"""
reasons you need TCP  proxy in 

1. forwaddng traffic to bounce- from host to host 
2. accessing network based software
3. when you are unable to run wireshark nor load drivers to sniff the loopback on windows

4. network segmentation will prevent you running your tools directly against your target host


"""

"""
the proxy has a few moving parts.

1. we need to display the communication between the local and remote machine to the console(hexdump)
2. we need to receive data from an incoming socket from either the local or remote machine(receive_from)
3.manage the traffic direction between remote and local machines(proxy handler)
4. we need to set up a listening socket and pass it to our proxy_handler(server_loop)

"""

import sys
import socket
import threading


HEX_FILTER = ''.join(
    [(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)]
)


def hexdump(src, length=16, show=True):
    if isinstance(src, bytes):
        src = src.decode()

    results = list()

    for i in range(0, len(src), length):
        word = str(src[i:i+length])
        printable = word.translate(HEX_FILTER)
        hexa = ' '.join([f'{ord(c): 02x}' for c in word])
        hexwidth = length*3
        results.append(f'{i:04x}  {hexa:<{hexwidth}} {printable}')

    
    if show:
        for line in results:
            print(line)

    else:
        return results


