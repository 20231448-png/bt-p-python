import socket

HOST = '127.0.0.1'
PORT = 8090

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

client.send("From CLIENT TCP".encode())

data = client.recv(1024).decode()
print("Server trả:", data)

client.close()