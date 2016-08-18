import numpy as np

def divide_componentes():
	transformada = np.matrix([	[165, 151, 130, 0 ],
						[156, 156, 156, 156],
						[160, 169, 160, 147],
						[151, 156, 156, 156]])

	mitad = transformada.shape[0]/2
	ca = transformada[0:mitad,0:mitad].copy()
	ch = transformada[0:mitad,mitad:].copy()
	cv = transformada[mitad:,0:mitad].copy()
	cd = transformada[mitad:,mitad:].copy()
	print ca
	print ch
	print cv
	print cd
	new_V_mul_components = np.concatenate((np.concatenate((ca, ch), axis=1), np.concatenate((cv, cd), axis=1)), axis=0)
	print new_V_mul_components

divide_componentes()