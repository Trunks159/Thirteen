def f():
	return 5
	
def x(y = f()):
	return y
	
print(x())
