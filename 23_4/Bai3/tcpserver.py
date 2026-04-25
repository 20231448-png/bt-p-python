import socket
import re

def check_password(pw):
    if len(pw) < 6 or len(pw) > 12:
        return False
    if not re.search("[a-z]", pw):
        return False
    if not re.search("[A-Z]", pw):
        return False
    if not re.search("[0-9]", pw):
        return False
    if not re.search("[$#@]", pw):
        return False
    return True

HOST = '127.0.0.1'
PORT = 8092

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Server chạy...")

conn, addr = server.accept()

data = conn.recv(1024).decode()
passwords = data.split(',')

valid = [pw for pw in passwords if check_password(pw)]

conn.send(",".join(valid).encode())

conn.close()
server.close()