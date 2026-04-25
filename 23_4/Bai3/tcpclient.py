import socket

HOST = '127.0.0.1'
PORT = 8092

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

pw = input("Nhập các mật khẩu (cách nhau bằng dấu phẩy): ")

client.send(pw.encode())

data = client.recv(1024).decode()
print("Mật khẩu hợp lệ:", data)

client.close()