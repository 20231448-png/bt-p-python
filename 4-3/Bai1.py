n = int(input("Nhập số dòng cần đọc: "))

with open("data.txt", "r", encoding="utf-8") as f:
    for i in range(n):
        line = f.readline()
        if not line:
            break
        print(line.strip())