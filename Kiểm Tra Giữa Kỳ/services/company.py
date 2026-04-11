class Company:
    def __init__(self):
        self.employees = []

    def add_employee(self, emp):
        ids = [e.id for e in self.employees]

        if emp.id in ids:
            i = 1
            new_id = f"{emp.id}_{i}"
            while new_id in ids:
                i += 1
                new_id = f"{emp.id}_{i}"   # ✅ sửa ở đây

            emp.id = new_id

        self.employees.append(emp)

    def get_all(self):
        if not self.employees:
            raise IndexError("Chưa có dữ liệu")
        return self.employees

    def find_by_id(self, emp_id):
        for e in self.employees:
            if e.id == emp_id:
                return e
        raise Exception("Không tìm thấy nhân viên")

    def delete_employee(self, emp_id):
        emp = self.find_by_id(emp_id)
        self.employees.remove(emp)