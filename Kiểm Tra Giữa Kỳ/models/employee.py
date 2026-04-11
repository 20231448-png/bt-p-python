class Employee:
    def __init__(self, id, name, age, email):
        self.id = id
        self.name = name
        self.age = age
        self.email = email
        self.projects = []
        self.score = 0

    def calculate_salary(self):
        return 0

    def add_project(self, project):
        from exceptions.employee_exceptions import ProjectAllocationError

        if len(self.projects) >= 5:
            raise ProjectAllocationError()

        self.projects.append(project)

    def __str__(self):
        return f"{self.id} - {self.name} - {self.age} - {self.email}"