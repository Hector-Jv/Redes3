from datetime import date
x = date(1997, 7, 13)
y = date(2023, 4, 3)
z = y - x
print(z.days)
print(z.days%3+1)