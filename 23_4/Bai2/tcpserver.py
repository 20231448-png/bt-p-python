
import socket

HOST = '127.0.0.1'
PORT = 8091

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Server đang chạy...")

conn, addr = server.accept()

data = conn.recv(1024).decode()
a, b = map(int, data.split())

tong = a + b
print(f"Tính: {a} + {b} = {tong}")

conn.send(str(tong).encode())

conn.close()
server.close()