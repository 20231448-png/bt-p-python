n = int(input("Nhập n: "))

i = 1
tong = 0

while i < n:
    if i % 2 == 0:
        tong = tong + i
    i = i + 1

print("Tổng các số chẵn nhỏ hơn", n, "là:", tong)