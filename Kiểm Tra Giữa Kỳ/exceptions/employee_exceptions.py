class EmployeeException(Exception):
    pass


class InvalidAgeError(EmployeeException):
    def __init__(self):
        super().__init__("Tuổi phải từ 18 đến 65")


class InvalidSalaryError(EmployeeException):
    def __init__(self):
        super().__init__("Lương phải > 0")


class EmployeeNotFoundError(EmployeeException):
    def __init__(self, emp_id):
        super().__init__(f"Không tìm thấy nhân viên ID: {emp_id}")


class ProjectAllocationError(EmployeeException):
    def __init__(self):
        super().__init__("Tối đa 5 project")


class DuplicateEmployeeError(EmployeeException):
    def __init__(self):
        super().__init__("ID đã tồn tại")