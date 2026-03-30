import time

namsinh = int(input("Nhập năm sinh: "))

x = time.localtime()
year = x[0]

tuoi = year - namsinh

print(f"Năm sinh {namsinh}, vậy bạn {tuoi} tuổi")