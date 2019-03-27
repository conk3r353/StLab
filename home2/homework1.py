class Department:
    def __init__(self, name, employees, budget):
        self.name = name
        self.employees = employees
        self.budget = int(budget)

    def __add__(self, other):
        return Department.merge_departments(self, other)

    def __or__(self, other):
        x = self.get_budget_plan()
        y = other.get_budget_plan()
        if x < y:
            return other
        return self

    def __str__(self):
        return f'{self.name} ({len(self.employees)} - {self.average_salary}, {self.budget})'

    class BudgetError(ValueError):
        def __init__(self):
            super().__init__()

    def get_budget_plan(self):
        total_budget = self.budget - sum(self.employees.values())
        if total_budget < 0:
            raise Department.BudgetError()
        return total_budget

    @property
    def average_salary(self):
        return round(sum(self.employees.values()) / float(len(self.employees.values())), 2)

    @classmethod
    def merge_departments(cls, *args):
        cls.sum_name = []
        cls.sum_employees = dict()
        cls.sum_budget = 0

        for obj in sorted(args, key=lambda x: (-x.average_salary, x.name)):
            cls.sum_name.append(obj.name)
            cls.sum_employees.update(obj.employees)
            cls.sum_budget += obj.budget
        if cls.sum_budget - sum(cls.sum_employees.values()) < 0:
            raise Department.BudgetError()
        return Department(' - '.join(cls.sum_name), cls.sum_employees, cls.sum_budget)
