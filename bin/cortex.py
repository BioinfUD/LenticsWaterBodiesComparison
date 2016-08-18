import math
import numpy as np
import matplotlib.pyplot as plt

def main():
	a=int(input("ingresa coeficiente cuadratico\n"))
	b=int(input("ingresa coeficiente lineal\n"))
	c=int(input("ingresa constante\n"))
	disc=b*b-4*a*c
	if(a!=0):
		if(disc<0):
			print("tiene raices imaginarias")
		else:
			x1=(-b+(math.sqrt(disc)))/(2*a)
			x2=(-b-(math.sqrt(disc)))/(2*a)
			print("X1 = "+str(x1)+" X2 = "+str(x2))
			#plot()
	else:
		print("coefiente cuadratico debe ser diferente de cero")


def f(x):
    return x*x+x+0

def plot():
	t1 = np.arange(0.0, 5.0, 0.1)
	t2 = np.arange(0.0, 5.0, 0.02)

	fig1 = plt.figure(1)
	plt.subplot(211)
	#fig1.savefig('test.jpg')
	plt.plot(t1, f(t1), 'bo', t2, f(t2), 'k')
	plt.show()

main()