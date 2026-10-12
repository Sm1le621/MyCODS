from collections import deque

class Employee:
  def __init__(self, name):
    self.name = name
    self.subordinates = []

  def add_subordinates(self, employee):
    self.subordinates.append(employee)

class Company:
  def __init__(self, ceo):
    self.ceo = ceo

  def print_by_levels(self):
    queue = deque([self.ceo])
    while queue:
      current = queue.popleft()
      print(current.name)
      for i in current.subordinates:
        queue.append(i)

if __name__ == "__main__":
  alexey = Employee("Алексей CEO")
  mari = Employee("Мария CTO")
  ivan = Employee("Иван CFO")
  mari_dev1 = Employee("Анна DEV")
  mari_dev2 = Employee("Сергей DEV")
  ivan_dev1 = Employee("Георгий DEV")
  alexey.add_subordinates(mari)
  alexey.add_subordinates(ivan)
  mari.add_subordinates(mari_dev1)
  mari.add_subordinates(mari_dev2)
  ivan.add_subordinates(ivan_dev1)
  
  company = Company(alexey)
  company.print_by_levels()