import ast

# đọc bộ mật mã
with open("cipher.txt", "r", encoding="utf-8") as f:
    cipher = ast.literal_eval(f.read())

# đọc file cần mã hóa
with open("input.txt", "r", encoding="utf-8") as f:
    text = f.read()

encoded = ""

for ch in text:
    if ch in cipher:
        encoded += cipher[ch]
    else:
        encoded += ch

# ghi file mã hóa
with open("encoded.txt", "w", encoding="utf-8") as f:
    f.write(encoded)

print("Đã tạo file encoded.txt")