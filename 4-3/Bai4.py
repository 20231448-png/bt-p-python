name = input("Tên: ")
age = input("Tuổi: ")
email = input("Email: ")
skype = input("Skype: ")
address = input("Địa chỉ: ")
work = input("Nơi làm việc: ")

with open("setInfo.txt", "w", encoding="utf-8") as f:
    f.write(f"Tên: {name}\n")
    f.write(f"Tuổi: {age}\n")
    f.write(f"Email: {email}\n")
    f.write(f"Skype: {skype}\n")
    f.write(f"Địa chỉ: {address}\n")
    f.write(f"Nơi làm việc: {work}\n")
    
with open("setInfo.txt", "r", encoding="utf-8") as f:
    print("Thông tin đã lưu:")
    print(f.read())