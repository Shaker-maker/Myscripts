
import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

# the execute function receives a command, runs it, and returns the output string
# subprocess library provides a powerful process creation interface that gives you ways to interact with client programs

# in this case, I am using check_output method, which runs a command on the local operating system and then returns output from the command



class NetCat():
    def __init__(self, args, buffer=None):
        self.args = args
        # self.buffer contains the data to be sent when the connection is established
        self.buffer = buffer

        # create a TCP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # set options for the socket
        # SOL_SOCKET - socket level where option is applied. It is a constant representing the socket layer itself.
        # SO_REUSEADDR - allows a port to bind a port that is in TIME_WAIT state without waiting for it to expire
        # 1 - to enable SO_REUSEADDR option
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self):
        # connecting to the server
        self.socket.connect((self.args.target, self.args.port))

        # sending initial data if there is any
        if self.buffer:
            # if the buffer is not empty, send its content to the server using .send() method
            self.socket.send(self.buffer)

        try:
            # Receiving and Sending data in a loop
            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break

                if response:
                    print(response)
                    buffer = input('>')
                    buffer += '\n'

                    self.socket.send(buffer.encode())

        except KeyboardInterrupt:
            print("User terminated")
            self.socket.close()
            sys.exit()


    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)

        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(
                target = self.handle, args= (client_socket, )
            )
            client_thread.start()


    # logic to perform file uploads, execute commands, and create an interactive shell


    def handle(self, client_socket):
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())

        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data :
                    file_buffer += data
                else:
                    break
                with open(self.args.upload, 'wb') as f:
                    f.write(file_buffer)
                message = f'Saved file { self.args.upload}'
                client_socket.send(message.encode())

        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'BHP: #> ')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)

                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
                except Exception as e:
                    print(f'SERVER KILLED!!!! {e}')
                    self.socket.close()
                    sys.exit()



def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return

    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)

    return output.decode()


# main block for command-line arguments and calling the rest of the functions

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='BHP Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(''' 
            Example:
                netcat.py -t 192.168.1.108 -p 5555 -l -c # command shell
                netcat.py -t 192.168.1.108 -p 5555 -l -u=mytext.txt # upload a file
                netcat.py -t 192.168.1.108 -p 5555 -l -e="cat /etc/passwd" # execute command
                echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 # echo text to the server port 135
                netcat.py -t 192.168.1.108 -p 5555 # connect to the server
        ''')
    )

    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    parser.add_argument('-t', '--target', default='192.168.1.108', help='specified IP address')
    parser.add_argument('-u', '--upload', help='upload file')

    # parse the arguments
    args = parser.parse_args()

    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()




    



    

    nc = NetCat(args, buffer.encode())
    nc.run()



                    
                        


        

                     
                       




   
