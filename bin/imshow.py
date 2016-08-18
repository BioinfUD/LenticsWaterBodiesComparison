
# coding=utf-8
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from PIL import Image

image_pan = plt.imread('/home/nazkter/Sofware_Develop/fusion_multipan/files/new_cellcrop_panp.tif')
image_mul = plt.imread('/home/nazkter/Sofware_Develop/fusion_multipan/files/new_cellcrop_rgb1p.tif')
pan_shape = image_pan.shape
mul_shape = image_mul.shape
print  'shape mul: %s' % (mul_shape,)
print  'shape pan: %s' % (pan_shape,)

'''image_pan = plt.imread('/home/nazkter/Sofware_Develop/fusion_multipan/fusionMultiPan/upload/panp.tif')
image_mul = plt.imread('/home/nazkter/Sofware_Develop/fusion_multipan/fusionMultiPan/upload/rgb1p.tif')
pan_shape = image_pan.shape
mul_shape = image_mul.shape
print  'shape mul: %s' % (mul_shape,)
print  'shape pan: %s' % (pan_shape,)
print image_mul[0][0]
print image_pan[0][0]

image_pan = image_pan[0:4,0:4].copy()
print image_pan
expand = 3 # cantidad de celdas nuevas por cada actual
img_size = 4 # tamaño de un lado de la imagen
new_image = np.zeros((img_size*expand,img_size*expand)) # creo una imagen del tamaño de la imagen final
shape = image_pan.shape
print 'Shape:\n%s'%(shape,)
x = 0
y = 0
while y < shape[1]:
    while x < shape[0]:
    	# tomo cada pixel y lo replico "expand" veces
    	pixel = image_pan[x][y]
    	print 'Pixel[%s][%s]:%s'%(x,y,pixel)
    	a=0
    	b=0
    	while a < expand:
    		while b < expand:
    			new_image[x*expand+b][y*expand+a] = pixel
    			b=b+1
    		a=a+1
    		b=0
    	print 'New image:\n%s'%(new_image,)
        x=x+1
    y=y+1
    x=0
'''
#plt.imshow(image_mul)
#plt.show()