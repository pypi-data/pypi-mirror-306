import numpy as np
from osgeo import gdal,osr
from osgeo import gdalnumeric
from osgeo.gdalconst import *
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import cv2

# This function will convert the rasterized clipper shapefile
# to a mask for use within GDAL.

def imageToArray(i):
    """
    Converts a Python Imaging Library array to a
    gdalnumeric image.
    """
    a = gdalnumeric.fromstring(i.tobytes(), 'b')
    a.shape = i.im.size[1], i.im.size[0]
    return a

def arrayToImage(a):
    """
    Converts a gdalnumeric array to a
    Python Imaging Library Image.
    """
    i = Image.fromstring('L', (a.shape[1], a.shape[0]),
                         (a.astype('b')).tobytes())
    return i

def pixel2world(geoMatrix, row, col):
    ulX = geoMatrix[0]
    ulY = geoMatrix[3]
    xDist = geoMatrix[1]
    yDist = geoMatrix[5]
    rtnX = geoMatrix[2]
    rtnY = geoMatrix[4]
    
    x = ulX + col * xDist
    y = ulY + row * yDist
    
    return x,y

def world2Pixel(geoMatrix, x, y):
    """
    Uses a gdal geomatrix (gdal.GetGeoTransform()) to calculate
    the pixel location of a geospatial coordinate
    """
    ulX = geoMatrix[0]
    ulY = geoMatrix[3]
    xDist = geoMatrix[1]
    yDist = geoMatrix[5]
    rtnX = geoMatrix[2]
    rtnY = geoMatrix[4]
    pixel = int(round(((x - ulX) / xDist),0))
    line = int(round(((ulY - y) / xDist),0))
    return (pixel, line)

class LightImage():
    """
    Image class with memory efficient implementation
    """

    def __init__(self, fn):
        self.fn = fn

        # Open hyperspectral data
        self.ds = gdal.Open(fn)
        self.ncol = self.ds.RasterXSize
        self.nrow = self.ds.RasterYSize
        self.nband = self.ds.RasterCount

        # Determine data type used
        self.band = self.ds.GetRasterBand(1)
        self.dtype = self.band.ReadAsArray(0, 0, 1, 1).dtype
        self.gdal_dtype = self.band.DataType

        # Compute extent of the image
        self.geotransform = self.ds.GetGeoTransform()
        self.ext_up = self.geotransform[3]
        self.ext_left = self.geotransform[0]
        # Cell size
        self.x_spacing = self.geotransform[1]
        self.y_spacing = self.geotransform[5]
        # Continue computing extent
        self.ext_down = self.ext_up + self.y_spacing * self.nrow
        self.ext_right = self.ext_left + self.x_spacing * self.ncol

        # Extract projection information
        self.projection = osr.SpatialReference()
        self.projection.ImportFromWkt(self.ds.GetProjectionRef())
        
    def show_image_rgb(self, bands=[0,1,2], axis='off'):
        """
        Display rgb image
        """

        # Initialize numpy array
        img = np.zeros((self.nrow, self.ncol, 3), dtype=self.dtype)

        # Read file onto memory
        for i in bands:
            band = self.ds.GetRasterBand(i+1)
            img[:, :, i] = np.array(band.ReadAsArray(0, 0, self.ncol, self.nrow), dtype=np.uint8)

        fig = plt.figure()
        ax = fig.add_subplot(111)
            
        ax.imshow(img)
        ax.axis(axis)

        plt.show()


    def get_img_array(self):
        
        arr = np.zeros((self.nrow, self.ncol, self.nband), dtype=self.dtype)

        for i in range(self.nband):
            band = self.ds.GetRasterBand(i + 1)
            arr[:,:,i] = band.ReadAsArray(0, 0, self.ncol, self.nrow)
        return arr


    def get_intersect_image(self, img):

        if self.ext_left < img.ext_left:
            col_in,_ = world2Pixel(self.geotransform, img.ext_left, img.ext_up)
        else:
            col_in = 0
        
        if self.ext_right < img.ext_right:
            col_out = None
        else:
            col_out, _ = world2Pixel(self.geotransform, img.ext_right, img.ext_down)
            
        if self.ext_up < img.ext_up:
           row_in = 0
        else:
             _, row_in = world2Pixel(self.geotransform, img.ext_left, img.ext_up)
            
        if self.ext_down < img.ext_down:
            _, row_out = world2Pixel(self.geotransform, img.ext_right, img.ext_down)
        else:
            row_out = None

        img_arr = np.empty((self.nrow, self.ncol), dtype=np.float32)

        # get reference image extent
        ext_left = [self.ext_left, img.ext_left]
        ext_right = [self.ext_right, img.ext_right]
        ext_up = [self.ext_up, img.ext_up]
        ext_down = [self.ext_down, img.ext_down]

        # set intersection boundary
        inter_left = max(ext_left)
        inter_right = min(ext_right)
        inter_up = min(ext_up)
        inter_down = max(ext_down)
        
        # clip data with reference image extent
        #get pixel boundary
        col_start, row_start = world2Pixel(img.geotransform, inter_left, inter_up)
        col_end, row_end = world2Pixel(img.geotransform, inter_right, inter_down)
        if (col_end-col_start)<=0 or (row_end-row_start)<=0:
            return None
        # image clipping
        img_clip = img.get_box(col_start,col_end-1,row_start,row_end-1)
        
        if img_arr[row_in:row_out,col_in:col_out].shape != img_clip.shape:
            
            img_clip_resize = cv2.resize(img_clip,(img_arr[row_in:row_out,col_in:col_out].shape[1],img_arr[row_in:row_out,col_in:col_out].shape[0]),
                                         interpolation=cv2.INTER_NEAREST)
            print('Image was resized to match the dimension: ',img_clip.shape,'->',img_clip_resize.shape)
        else:
            img_clip_resize = img_clip
        
        img_arr[row_in:row_out,col_in:col_out] = img_clip_resize

        return img_arr
            
            
            
            
    def get_pixel(self, x, y, band=0):
        """
        Return the value of pixel.

        Default is to return the pixel value of first band at (x,y)

        (x,y) is based on the image coordinate where upper left is the origin, and x increase to the right, and y increases downwards.
        This is equivalent to (col, row) pair
        """
        # Check if given (x,y) is inside the range of the image
        if x < 0 or x > self.ncol - 1:
            print("X coordinate is out of range")
            return None

        if y < 0 or y > self.nrow - 1:
            print("Y coordinate is out of range")
            return None

        band = self.ds.GetRasterBand(band + 1)

        return band.ReadAsArray(x, y, 1, 1)[0][0]

    def get_pixel_by_coordinate(self, x, y, band=0, debug_flag=False):
        """
        Extract pixel values based on the coordinate

        (x,y) is the coordinate pair in the coordinate system used for the image.
        """

        # Check if the coordinate given is inside the image
        if (x < self.ext_left) or (x > self.ext_right) or (y < self.ext_down) or (y > self.ext_up):
            print("The given point (%f, %f) is not inside the image." % (x, y))
            return None

        # Compute offset from the upper left corner.
        x_off = x - self.ext_left
        y_off = self.ext_up - y

        x_ind = int(x_off / abs(self.x_spacing))
        y_ind = int(y_off / abs(self.y_spacing))

        if debug_flag:
            print("(x_ind, y_ind) = (%d, %d)" % (x_ind, y_ind))

        return self.img[band, y_ind, x_ind]

    def get_box(self, minx, maxx, miny, maxy, band=0):
        """
        Return the value of box.

        Default is to return the pixel value of first band

        (x,y) is based on the image coordinate where upper left is the origin, and x increase to the right, and y increases downwards.
        This is equivalent to (col, row) pair

        Requires (minx, maxx, miny, maxy) input

        """
        # Check if given (x,y) is inside the range of the image
        if minx < 0 or maxx > self.ncol - 1:
            print("X coordinate is out of range")
            return None

        if miny < 0 or maxy > self.nrow - 1:
            print("Y coordinate is out of range")
            return None

        band = self.ds.GetRasterBand(band + 1)

        return band.ReadAsArray(minx, miny, maxx - minx + 1, maxy - miny + 1)


    def get_box_all(self, minx, maxx, miny, maxy):
        """
        Return the value of box.

        Default is to return the pixel value of first band

        (x,y) is based on the image coordinate where upper left is the origin, and x increase to the right, and y increases downwards.
        This is equivalent to (col, row) pair

        Requires (minx, maxx, miny, maxy) input

        """
        # Check if given (x,y) is inside the range of the image
        if minx < 0 or miny < 0:
            print("pixel coordinate is out of range")
            return None
        
        if maxx > self.ncol or maxx == -1:
            maxx = self.ncol
        
        if maxy > self.nrow or maxy == -1:
            maxy = self.nrow            
        
        num_x = int(maxx - minx)
        num_y = int(maxy - miny)


        box_img = np.zeros((self.nband, maxy-miny, maxx-minx),
                            dtype=self.dtype)

        for i in range(self.nband):
            band = self.ds.GetRasterBand(i + 1)
            box_img[i,:,:] = band.ReadAsArray(int(minx), int(miny), num_x, num_y)
            
        gt_out = [self.ext_left + minx * self.x_spacing, 
                  self.x_spacing, 
                  self.geotransform[2], 
                  self.ext_up + miny * self.y_spacing, 
                  self.geotransform[4], 
                  self.y_spacing]
        

        return box_img , gt_out

    def get_pixel_boundary(self, x, y):
        """
        Return the boundary of the specified pixel

        Will return (x_min, x_max, y_min, y_max) pair
        """
        return self.ext_left + self.x_spacing * x, self.ext_left + self.x_spacing * (x+1), \
            self.ext_up + self.y_spacing * y, self.ext_up + self.y_spacing * (y+1)

    def get_pixel_ul(self, x, y):
        return self.ext_left + self.x_spacing * x, self.ext_up + self.y_spacing * y

    def get_pixel_ll(self, x, y):
        return self.ext_left + self.x_spacing * x, self.ext_up + self.y_spacing * (y+1)

    def get_pixel_lr(self, x, y):
        return self.ext_left + self.x_spacing * (x+1), self.ext_up + self.y_spacing * (y+1)

    def get_pixel_ur(self, x, y):
        return self.ext_left + self.x_spacing * (x+1), self.ext_up + self.y_spacing * y

    def get_pixel_center(self, x, y):
        """
        Return center coordinates of the pixel

        Input: (x,y) is the image coordinate of the pixel
        """
        return self.ext_left + self.x_spacing * (x+0.5), self.ext_up + self.y_spacing * (y + 0.5)

    def get_pixel_coordinate(self, x, y):
        """
        Return pixel coordinate from the actual coordinates

        Input (x,y) is the actual coordinates, and return value will be pixel coordinates
        """
        x_off = x - self.ext_left
        y_off = y - self.ext_up

        return x_off / float(self.x_spacing), y_off / float(self.y_spacing)

    def clip_by_polygon(self, poly):
        """
        Clip image by polygon provided

        Input "poly" should be poly read by Fiona
        """
        geoTrans = self.ds.GetGeoTransform()
        points = []
        pixels = []
        pixels_clipped = []
        geom = poly.GetGeometryRef()
        pts = geom.GetGeometryRef(0)

        for p in range(pts.GetPointCount()):
            points.append((pts.GetX(p), pts.GetY(p)))

        # for p in poly['geometry']['coordinates'][0]:
        #     points.append(p)

        for p in points:
            pixels.append(world2Pixel(geoTrans, p[0], p[1]))

        pixels_np = np.array(pixels)
        minx = pixels_np[:, 0].min()
        maxx = pixels_np[:, 0].max()
        miny = pixels_np[:, 1].min()
        maxy = pixels_np[:, 1].max()

        # Now check if polygon is inside the image
        if (minx < 0) or (maxx > self.ncol - 1):
            print("Polygon is outside of image")
            return None

        if (miny < 0) or (maxy > self.nrow - 1):
            print("Polygon is outside of image")
            return None

        clipped_img = self.get_box_all(minx, maxx, miny, maxy)
        clipped_img_width = clipped_img.shape[2]
        clipped_img_height = clipped_img.shape[1]

        for p in pixels:
            pixels_clipped.append((p[0] - minx, p[1] - miny))

        rasterPoly = Image.new("L", (clipped_img_width, clipped_img_height), 1)
        rasterize = ImageDraw.Draw(rasterPoly)
        rasterize.polygon(pixels_clipped, 0)
        mask = imageToArray(rasterPoly)

        clipped_img_masked = gdalnumeric.choose(mask, (clipped_img, 0))

        return clipped_img_masked

    def clip_by_polygon_and_save(self, poly, out_fn):
        """
        Clip image by polygon provided

        Input "poly" should be poly read by Fiona
        """
        geoTrans = self.ds.GetGeoTransform()
        points = []
        pixels = []
        pixels_clipped = []
        geom = poly.GetGeometryRef()
        pts = geom.GetGeometryRef(0)

        for p in range(pts.GetPointCount()):
            points.append((pts.GetX(p), pts.GetY(p)))

        # for p in poly['geometry']['coordinates'][0]:
        #     points.append(p)

        for p in points:
            pixels.append(world2Pixel(geoTrans, p[0], p[1]))

        pixels_np = np.array(pixels)
        minx = pixels_np[:, 0].min()
        maxx = pixels_np[:, 0].max()
        miny = pixels_np[:, 1].min()
        maxy = pixels_np[:, 1].max()

        # Now check if polygon is inside the image
        if (minx < 0) or (maxx > self.ncol - 1):
            print("Polygon is outside of image")
            return None

        if (miny < 0) or (maxy > self.nrow - 1):
            print("Polygon is outside of image")
            return None

        clipped_img = self.get_box_all(minx, maxx, miny, maxy)
        clipped_img_width = clipped_img.shape[2]
        clipped_img_height = clipped_img.shape[1]

        for p in pixels:
            pixels_clipped.append((p[0] - minx, p[1] - miny))

        rasterPoly = Image.new("L", (clipped_img_width, clipped_img_height), 1)
        rasterize = ImageDraw.Draw(rasterPoly)
        rasterize.polygon(pixels_clipped, 0)
        mask = imageToArray(rasterPoly)

        clipped_img_masked = gdalnumeric.choose(mask, (clipped_img, 0))

        num_band = clipped_img_masked.shape[0]

        clipped_lc = self.ext_left + minx * self.x_spacing
        clipped_uc = self.ext_up   + miny * self.y_spacing

        driver = gdal.GetDriverByName('ENVI')
        outds = driver.Create(out_fn, clipped_img_width, clipped_img_height,
                            clipped_img_masked.shape[0], self.gdal_dtype)
        outds.SetGeoTransform([clipped_lc, self.x_spacing, self.geotransform[2],
                clipped_uc, self.geotransform[4], self.y_spacing])
        outds.SetProjection(self.ds.GetProjection())

        if num_band == 1:
            outds.GetRasterBand(1).WriteArray(clipped_img_masked[:,:])
        else:
            for i in range(num_band):
                outds.GetRasterBand(i+1).WriteArray(clipped_img_masked[i,:,:])

        outds = None
        
    def create_copy(self, out_fn, projection=None, gt=None):
        
        if projection is None:
            projection = self.projection
        if gt is None:
            gt = self.geotransform
            
        driver = gdal.GetDriverByName('GTiff')
        out_ds = driver.CreateCopy(out_fn, self.ds, 0)
        out_ds.SetProjection(projection)
        out_ds.SetGeoTransform(gt)
        out_ds = None
