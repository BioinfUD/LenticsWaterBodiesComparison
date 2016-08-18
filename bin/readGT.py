import sys, getopt
from osgeo import gdal,osr
gdal.UseExceptions()

def main():
	ds=gdal.Open(sys.argv[1])
	print 'MetaData'
	print ds.GetMetadata()
	print 'RasterBand'
	print ds.GetRasterBand(1)
	print 'GeoTransform'
	print ds.GetGeoTransform();

	prj=ds.GetProjection()
	print prj

	srs=osr.SpatialReference(wkt=prj)
	if srs.IsProjected:
	    print srs.GetAttrValue('projcs')
	print srs.GetAttrValue('geogcs')
'''	
from osgeo import gdal
from osgeo import osr
import sys, getopt
def main():
	ds = gdal.Open(sys.argv[1])
	width = ds.RasterXSize
	height = ds.RasterYSize
	gt = ds. GetGeoTransform()

	minx = gt[0]
	miny = gt[3] 
	maxy = gt[3] + width*gt[4] + height*gt[5] 
	maxx = gt[0] + width*gt[1] + height*gt[2]
	print  'x1:%s\ny1:%s\nx2:%s\ny2:%s'%(minx,miny,maxx,maxy)
	pixelPairs = [[0,0],[2048,2048]]
	print pixelPairs
	print pixelToLatLon(sys.argv[1],pixelPairs)

'''
# The following method translates given latitude/longitude pairs into pixel locations on a given GEOTIF
# INPUTS: geotifAddr - The file location of the GEOTIF
#      latLonPairs - The decimal lat/lon pairings to be translated in the form [[lat1,lon1],[lat2,lon2]]
# OUTPUT: The pixel translation of the lat/lon pairings in the form [[x1,y1],[x2,y2]]
# NOTE:   This method does not take into account pixel size and assumes a high enough 
#	  image resolution for pixel size to be insignificant
def latLonToPixel(geotifAddr, latLonPairs):
	# Load the image dataset
	ds = gdal.Open(geotifAddr)
	# Get a geo-transform of the dataset
	gt = ds.GetGeoTransform()
	# Create a spatial reference object for the dataset
	srs = osr.SpatialReference()
	srs.ImportFromWkt(ds.GetProjection())
	# Set up the coordinate transformation object
	srsLatLong = srs.CloneGeogCS()
	ct = osr.CoordinateTransformation(srsLatLong,srs)
	# Go through all the point pairs and translate them to latitude/longitude pairings
	pixelPairs = []
	for point in latLonPairs:
		# Change the point locations into the GeoTransform space
		(point[1],point[0],holder) = ct.TransformPoint(point[1],point[0])
		# Translate the x and y coordinates into pixel values
		x = (point[1]-gt[0])/gt[1]
		y = (point[0]-gt[3])/gt[5]
		# Add the point to our return array
		pixelPairs.append([int(x),int(y)])
	return pixelPairs
# The following method translates given pixel locations into latitude/longitude locations on a given GEOTIF
# INPUTS: geotifAddr - The file location of the GEOTIF
#      pixelPairs - The pixel pairings to be translated in the form [[x1,y1],[x2,y2]]
# OUTPUT: The lat/lon translation of the pixel pairings in the form [[lat1,lon1],[lat2,lon2]]
# NOTE:   This method does not take into account pixel size and assumes a high enough 
#	  image resolution for pixel size to be insignificant
def pixelToLatLon(geotifAddr,pixelPairs):
	# Load the image dataset
	ds = gdal.Open(geotifAddr)
	# Get a geo-transform of the dataset
	gt = ds.GetGeoTransform()
	# Create a spatial reference object for the dataset
	srs = osr.SpatialReference()
	srs.ImportFromWkt(ds.GetProjection())
	# Set up the coordinate transformation object
	srsLatLong = srs.CloneGeogCS()
	ct = osr.CoordinateTransformation(srs,srsLatLong)
	# Go through all the point pairs and translate them to pixel pairings
	latLonPairs = []
	for point in pixelPairs:
		# Translate the pixel pairs into untranslated points
		print 'ulon: %s*%s*%s'%(point[0],gt[1],gt[0])
		ulon = point[0]*gt[1]+gt[0]
		print ulon
		ulat = point[1]*gt[5]+gt[3]
		print ulat
		# Transform the points to the space
		(lon,lat,holder) = ct.TransformPoint(float(ulon),float(ulat))
		# Add the point to our return array
		latLonPairs.append([lat,lon])

	return latLonPairs

main()