def kiem_tra_chia_het():
    # Nhập số nguyên dương
    n = int(input("Nhập số nguyên dương: "))

    # Kiểm tra chia hết cho 2
    if n % 2 == 0:
        print(f"{n} chia hết cho 2")
    else:
        print(f"{n} không chia hết cho 2")

    # Kiểm tra chia hết cho 3
    if n % 3 == 0:
        print(f"{n} chia hết cho 3")
    else:
        print(f"{n} không chia hết cho 3")

    # Kiểm tra chia hết cho cả 2 và 3
    if n % 2 == 0 and n % 3 == 0:
        print(f"{n} chia hết cho cả 2 và 3")
    else:
        print(f"{n} không chia hết cho cả 2 và 3")

kiem_tra_chia_het()