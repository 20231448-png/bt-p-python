import math

def giai_phuong_trinh_bac_2():
    # Nhập các tham số a, b, c
    a = float(input("Nhập giá trị a: "))
    b = float(input("Nhập giá trị b: "))
    c = float(input("Nhập giá trị c: "))

    # Tính delta
    delta = b**2 - 4*a*c

    # Kiểm tra giá trị của delta
    if delta > 0:
        # Có hai nghiệm phân biệt
        x1 = (-b + math.sqrt(delta)) / (2*a)
        x2 = (-b - math.sqrt(delta)) / (2*a)
        print(f"Phương trình có hai nghiệm phân biệt: x1 = {x1}, x2 = {x2}")
    elif delta == 0:
        # Có một nghiệm kép
        x = -b / (2*a)
        print(f"Phương trình có một nghiệm kép: x = {x}")
    else:
        # Không có nghiệm
        print("Phương trình không có nghiệm")

# Chạy chương trình
giai_phuong_trinh_bac_2()


Lưu ý: Chương trình này sẽ hỏi người dùng nhập giá trị của a, b, c và sau đó sẽ giải phương trình bậc 2 dựa trên các giá trị này.