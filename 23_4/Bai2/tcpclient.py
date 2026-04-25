import socket

HOST = '127.0.0.1'
PORT = 8091

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

a = input("Nhập a: ")
b = input("Nhập b: ")

client.send(f"{a} {b}".encode())

data = client.recv(1024).decode()
print("Tổng nhận từ server:", data)

client.close()