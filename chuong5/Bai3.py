n = int(input("Nhập n: "))

i = 2
laSNT = True

while i <= n // 2:
    if n % i == 0:
        laSNT = False
        break
    i = i + 1

if n < 2:
    laSNT = False

if laSNT:
    print("Đây là số nguyên tố")
else:
    print("Không phải số nguyên tố")