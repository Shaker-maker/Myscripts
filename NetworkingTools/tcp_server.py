import socket
# allows the server to handle multiple clients at once by using threads
import threading

# 0.0.0.0  -- tells the server to listen on all available interfaces(loobac, LAN, etc)
IP ='0.0.0.0'
PORT = 9998 # here is where the server will wait for connections

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen(5)

    print(f'[*] Listenig on {IP}:{PORT}')

    while True:
        client, address = server.accept()
        print(f'[*] Accepted connection from {address[0]} : {address[1]}')
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()


def handle_client(client_socket):
    """It's a context manager — handles sock.close() for you when you're done.
        sock is now the tool you use to talk to the client."""
    with client_socket as sock:
        request = sock.recv(1024)
        print(f'[*] Received: {request.decode("utf-8")}')
        sock.send(b'ACK')


if __name__ =="__main__":
    main()