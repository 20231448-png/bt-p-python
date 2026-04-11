from services.company import Company
from models.manager import Manager
from models.developer import Developer
from models.intern import Intern

from utils.validators import *
from exceptions.employee_exceptions import *

def menu():
    print("\n===== MENU =====")
    print("1. Thêm nhân viên")
    print("2. Hiển thị danh sách")
    print("3. Tìm theo ID")
    print("4. Thêm project")
    print("5. Xóa nhân viên")
    print("6. Thoát")

def main():
    company = Company()

    while True:
        try:
            menu()
            choice = int(input("Chọn: "))

            if choice == 1:
                id = input("ID: ")
                name = input("Tên: ")

                while True:
                    try:
                        age = int(input("Tuổi: "))
                        validate_age(age)
                        break
                    except Exception as e:
                        print("❌", e)

                while True:
                    try:
                        email = input("Email: ")
                        validate_email(email)
                        break
                    except Exception as e:
                        print("❌", e)

                print("a. Manager | b. Developer | c. Intern")
                t = input("Loại: ")

                while True:
                    try:
                        salary = float(input("Lương: "))
                        validate_salary(salary)
                        break
                    except Exception as e:
                        print("❌", e)

                if t == "a":
                    emp = Manager(id, name, age, email, salary)
                elif t == "b":
                    lang = input("Ngôn ngữ: ")
                    emp = Developer(id, name, age, email, salary, lang)
                else:
                    emp = Intern(id, name, age, email, salary)

                company.add_employee(emp)
                print("✔ Đã thêm!")

            elif choice == 2:
                try:
                    for e in company.get_all():
                        print(e)
                except Exception as e:
                    print("❌", e)

            elif choice == 3:
                try:
                    id = input("ID: ")
                    print(company.find_by_id(id))
                except Exception as e:
                    print("❌", e)

            elif choice == 4:
                try:
                    id = input("ID: ")
                    emp = company.find_by_id(id)

                    project = input("Project: ")
                    emp.add_project(project)

                    print("✔ OK")
                except Exception as e:
                    print("❌", e)

            elif choice == 5:
                try:
                    id = input("ID: ")
                    company.delete_employee(id)
                    print("✔ Đã xóa")
                except Exception as e:
                    print("❌", e)

            elif choice == 6:
                break

        except ValueError:
            print("❌ Nhập số!")

if __name__ == "__main__":
    main()