"""standard multithreaded TCP server
"""
import socket
import threading

IP = '0.0.0.0'
PORT = 9998

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen(5)
    print(f'[*] Listening on {IP} : {PORT}')

    while True:
        client, address = server.accept()
        print(f'[*] Accepted connection from {address[0]} : {address[1]}')
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start() # start a thread to handle client conection at which point the main server loop is ready to handle another incoming conection

def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)
        print(f'[*] Received: {request.decode("utf-8")}')
        sock.send(b'ACK')


if __name__ == '__main__':
    main()


"""
when the client connects, we receive the client socket in the client variable and remote
connection details in the address variable

we then create a new thread object that points to our handle_client function and we 
pass our client_socket as  an argument
"""