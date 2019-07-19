x = [['y']]
y = x
x[0] = 8
print(id(y), id(x))
