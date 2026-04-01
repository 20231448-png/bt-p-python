n = int(input("Nhập n: "))

i = 1
giaithua = 1

while i <= n:
    giaithua = giaithua * i
    i = i + 1

print("Giai thừa của", n, "là:", giaithua)