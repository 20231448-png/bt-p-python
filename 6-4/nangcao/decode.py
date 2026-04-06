import ast
import os

base = os.path.dirname(__file__)

cipher_file = os.path.join(base, "cipher.txt")
encoded_file = os.path.join(base, "encoded.txt")
decoded_file = os.path.join(base, "decoded.txt")

with open(cipher_file, "r", encoding="utf-8") as f:
    cipher = ast.literal_eval(f.read())

decode = {v:k for k,v in cipher.items()}

with open(encoded_file, "r", encoding="utf-8") as f:
    text = f.read()

result = ""

for ch in text:
    if ch in decode:
        result += decode[ch]
    else:
        result += ch

with open(decoded_file, "w", encoding="utf-8") as f:
    f.write(result)

print("Giải mã xong!")