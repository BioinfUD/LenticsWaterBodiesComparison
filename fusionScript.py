#!/usr/bin/python
import cv2
import numpy as np
from PIL import Image
import sys, getopt
import exifread
from scipy import misc

def getH(r, g, b, I):
    Min = r
    flag = 'r'
    if g < Min:
        Min = g
        flag = 'g'    
    if b < Min:
        Min = b
        flag = 'b'
        if g < b:
            Min = g
            flag = 'g'
    if flag == 'r':
        h = (b-r)/(I-765*r) + 255
    elif flag == 'g':
		h = (r - g) / (I - 765*g) + 510
    elif flag == 'b':
    	h = (g - b) / (I - 765*b)
    return h


def getS(r, g, b, I, H):
	if 0<=H<=255:
		s = (I - 765*b) /I
	elif 255<H<=510:
		s = (I - 765*r) /I
	elif 510<H<=765:
		s = (I - 765*g) /I
	else:
		pass


def RGB2IHS(r,g,b):
	# segun la toria de http://ij.ms3d.de/pdf/ihs_transforms.pdf
	# los valores de RGB deben estar entre 0 y 1
	r = [x + 1 for x in r]
	g = [x + 1 for x in g]
	b = [x + 1 for x in b]
	I = [x + y + z for x, y, z in zip(r, g, b)]
	H = [getH(x, y, z, a) for x, y, z, a in zip(r, g, b, I)]
	S = [getS(x, y, z, a, b) for x, y, z, a, b in zip(r, g, b, I, H)]
	return I, H, S


input_mul = sys.argv[1]
input_pan = sys.argv[2]
output_fus = sys.argv[3]

img = Image.open(input_mul)
print 'la imagen tiene '+str(len(img.getbands()))+' banda(s): '+str(img.getbands())
if len(img.getbands()) == 4:
	r, g, b, a = img.split()
else:
	r, g, b = img.split()
#print str(r)
r_list = list(r.getdata())
g_list = list(g.getdata())
b_list = list(b.getdata())

I, H, S = RGB2IHS(r_list,g_list,b_list)
