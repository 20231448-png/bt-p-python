from models.employee import Employee

class Intern(Employee):
    def __init__(self, id, name, age, email, stipend):
        super().__init__(id, name, age, email)
        self.stipend = stipend

    def calculate_salary(self):
        return self.stipend