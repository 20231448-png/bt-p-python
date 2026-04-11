from models.employee import Employee

class Developer(Employee):
    def __init__(self, id, name, age, email, salary, language):
        super().__init__(id, name, age, email)
        self.salary = salary
        self.language = language

    def calculate_salary(self):
        return self.salary