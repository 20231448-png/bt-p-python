from models.employee import Employee

class Manager(Employee):
    def __init__(self, id, name, age, email, salary):
        super().__init__(id, name, age, email)
        self.salary = salary

    def calculate_salary(self):
        return self.salary