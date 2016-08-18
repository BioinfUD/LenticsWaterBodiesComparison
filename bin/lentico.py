import matplotlib.pyplot as plt
import PythonMagick
from osgeo import gdal, ogr
from PIL import Image
import sys, getopt
import numpy
import os
import glob






def get_loticsRaster(im, out):
	print im.size
	print im.mode
	im.mode = 'I'
	table=[ i/256 for i in range(65536) ]
	im2 = im.point(table,'L')
	im = im2
	print "mode 2: "+im2.mode
	pix = im.load()
	width, height = im.size
	for x in range(0,width):
		for y in range(0,height):
			pixel = pix[x,y]
			#print pixel
			if pixel > 0:
				pix[x,y] = 255
	#im.thumbnail(im.size)
	im.save(out)
	#plt.imsave('results/out_plt.tif',im, cmap=plt.cm.gray)
	im.close()

def poligonizar(lotics):
	src_ds = gdal.Open(lotics)
	srcband = src_ds.GetRasterBand(1)
	drv = ogr.GetDriverByName("ESRI Shapefile")
	dst_ds = drv.CreateDataSource( lotics+".shp" )
	dst_layer = dst_ds.CreateLayer(lotics, srs = None )
	gdal.Polygonize( srcband, None, dst_layer, -1, [], callback=None )
	#return Image.fromarray(data)

def get_areas(shp):
	driver = ogr.GetDriverByName("ESRI Shapefile")
	dataSource = driver.Open(shp, 1)
	layer = dataSource.GetLayer()
	new_field = ogr.FieldDefn("Area", ogr.OFTInteger)
	layer.CreateField(new_field)
	area_total = 0
	for feature in layer:
	    geom = feature.GetGeometryRef()
	    area = geom.GetArea()
	    if area < 200:
			#print area
			feature.SetField("Area", area)
			layer.SetFeature(feature)
			area_total = area_total+area 
	print 'Area total:'
	print area_total
	dataSource = None

def main():

	print 'Leyengo imagen...'
	im = Image.open(sys.argv[1])
	out = sys.argv[2]
	files = glob.glob('results/*')
	for f in files:
	    os.remove(f)

	print 'Extrayendo loticos...'
	get_loticsRaster(im, out)

	print 'Poligonzando imagen...'
	poligonizar(out)

	print 'Calculando area de los poligonos...'
	get_areas(out+".shp")

main()

'''print 'Leyendo la imagen...'
tmp_img = PythonMagick.Image(input_img)
print 'conviertiendo imagen...'
tmp_img.write('file_out.tif')
print 'Leyendo nueva imagen...'
im = Image.open('file_out.tif')
print 'Filtrando los cuerpos lenticos...'
)
imin.mode = "I"
imout = Image.new("I", imin.size)
imin.point(lambda i: 255 if i>20 else i)
#imin.putdata(lambda pixel: 255 if pixel >= 100 else pixel) 
#plt.imsave('results/out_plt.tif',imout, cmap=plt.cm.gray)
imin.save(sys.argv[2])'''
'''
# Process every pixel
for x in range(0,width):
	for y in range(0,height):
		pixel = im.getpixel( (x,y) )
		if pixel > 20:
			im.putpixel( (x,y), 255)
'''
#im.save("foo_new.tiff")
        #if im.getpixel((i,j)) > 20:
        #	print im.getpixel((i,j))
        	
#
#plt.imsave('results/1.tif',out, cmap=plt.cm.gray)

