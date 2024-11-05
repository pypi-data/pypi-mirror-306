import numpy as np
from PIL import Image
from geopandas import gpd
from rs3 import LightImage, pixel2world
from polygonize import polygonize
import torch
import cv2
from segment_anything import sam_model_registry, SamAutomaticMaskGenerator, SamPredictor
from skimage.transform import probabilistic_hough_line
import math
from shapely.geometry import Polygon as sPolygon
from shapely.affinity import rotate
from skimage.measure import label
import itertools
import rasterio
from sklearn.neighbors import KDTree
from sklearn.cluster import DBSCAN

class PlotExtraction(LightImage):
    
    def __init__(self, data_product):
        
        self.data_product = data_product
        
    def load_image(self, filename):
        
        super().__init__(filename)
        self.img_array = self.get_img_array()[:,:,:3]
        self.img_width = self.img_array.shape[1]
        self.img_height = self.img_array.shape[0]
        self.cc_map = self.canopeo(self.img_array)    
  
        
    def clip(self, geometry, filename):
        
        self.data_product.clip(geojson_feature=geometry, out_raster=filename)
        super().__init__(filename)
        self.img_array = self.get_img_array()[:,:,:3]
        self.img_width = self.img_array.shape[1]
        self.img_height = self.img_array.shape[0]
        self.cc_map = self.canopeo(self.img_array)    
        
        
    def canopeo(self, arr, th1=0.95, th2=0.95, th3=20):
        
        # Read bands
        red = arr[:,:,0].astype(np.float32)
        green = arr[:,:,1].astype(np.float32)
        blue = arr[:,:,2].astype(np.float32)

        # Find canopy cover
        i1 = red / green
        i2 = blue / green
        i3 = (2*green - blue - red)
        # i4 = (red + green + blue)
        # i5 = (green - blue)
        cond1 = i1 < th1
        cond2 = i2 < th2
        cond3 = i3 > th3
        # cond4 = i4 < th4
        # cond5 = i5 > th5
        cond = (cond1 * cond2 * cond3) * 255
        
        return cond
    
    def load_sam(self, sam_checkpoint, model_type='vit_h', points_per_side=100):
    
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
        sam.to(device=device)
        
        self.mask_generator = SamAutomaticMaskGenerator(
            model=sam,
            # points_per_side=np.max([img_dict[img_suffix]['n_cols'],img_dict[img_suffix]['n_rows']]),
            points_per_side=points_per_side,
            pred_iou_thresh=0.86,
            stability_score_thresh=0.92,
            crop_n_layers=1,
            crop_n_points_downscale_factor=2,
            min_mask_region_area=100,  # Requires open-cv to run post-processing
        )
        
        self.predictor = SamPredictor(sam)
        
        print(f"Loaded device: {device}")
        
    def get_masks(self, resize=1024):
        
        self.resize=resize
        
        self.scale_col = self.img_width / resize
        self.scale_row =  self.img_height/ resize
        img_resize = cv2.resize(self.img_array,(resize,resize),interpolation=cv2.INTER_NEAREST)
        
        masks = self.mask_generator.generate(img_resize)
        
        mask_arr = np.zeros((img_resize.shape[:2]))
        for mask_ in masks:
            mask_arr += mask_['segmentation'] * np.random.randint(1,len(masks))
        self.mask_arr = cv2.resize(mask_arr, (self.img_width, self.img_height), interpolation=cv2.INTER_NEAREST)
        
        return self.mask_arr
    
    def rotate_plot(self, offset=180, line_length=100, line_gap=10):
                
        mask = np.array(self.mask_arr, dtype=np.uint8)*255
        edge = cv2.Canny(mask, 50, 150, apertureSize=3)
        
        edge_full = Image.fromarray(edge).resize((self.ncol, self.nrow))
        lines = probabilistic_hough_line(np.array(edge_full), threshold=10, line_length=line_length, line_gap=line_gap)
        
        slope = []
        for line in lines:
            p0, p1 = line
            eps = 1E-6
            slope.append(np.degrees(math.atan2((p0[1]-p1[1]+eps),(p1[0]-p0[0]+eps))))
            
        self.slope_deg = offset - np.median(slope)
        print(f"Estimated orientation angle: {self.slope_deg:.2f} degree")
        
        center_x = self.img_width/2
        center_y = self.img_height/2
        self.center_img = (center_x,center_y)
        
        center_x_geo, center_y_geo = pixel2world(self.geotransform, center_y, center_x)
        self.center_geo = (center_x_geo, center_y_geo)
        
        self.img_rotated = Image.fromarray(self.img_array).rotate(self.slope_deg, center=(center_x,center_y))
        
        return self.img_rotated
        
        
    def filter_plots(self, plot_width, plot_height, delta_area=1):
        
        self.plot_width = plot_width
        self.plot_height = plot_height
        
        img_rotated_resize = np.array(self.img_rotated.resize((self.resize,self.resize)))
        masks = self.mask_generator.generate(img_rotated_resize)
        
        polygons_loc={'id':[],'geometry':[]}
        polygons_mask=[]
        
        i=0
        for mask in masks:
            mask_, mask_num = label(mask['segmentation'], return_num=True)
            for j in range(mask_num):
                mask_tmp = (mask_==(j+1))
                polygon = polygonize(mask_tmp, convex=True, simplify_tolerance=1)[0]
                xy = np.array(polygon.exterior.xy).transpose() * np.array([self.scale_col, self.scale_row])
                x = xy[:,0]
                y = -xy[:,1]
                transformed_coords = (np.array([x,y])*self.x_spacing + np.array([[self.ext_left],[self.ext_up]])).transpose()
                polygon_loc = sPolygon(transformed_coords)
                
                if polygon_loc.area > (plot_width*plot_height)-delta_area and polygon_loc.area < (plot_width*plot_height)+delta_area:
                    polygons_loc['id']=i
                    polygons_loc['geometry'].append(polygon_loc)
                    polygons_mask.append(mask_tmp)
                    i+=1
        self.polygons_local = polygons_loc
        
        x_loc,y_loc,cent_loc = [],[],[]
        for polygon_loc in polygons_loc['geometry']:
            # x,y, and centroid in geo-coordinate
            x_loc.append(np.array(polygon_loc.exterior.xy[0]))
            y_loc.append(np.array(polygon_loc.exterior.xy[1]))
            cent_loc.append([polygon_loc.centroid.x, polygon_loc.centroid.y])
        self.cent_local = cent_loc
            
        polygons_arr = np.zeros((self.resize,self.resize))
        for i,mask in enumerate(polygons_mask):
            polygons_arr += mask * (i+1)
        filtered_mask = cv2.resize(np.array(polygons_arr, dtype=np.uint8), 
                                   (self.img_width,self.img_height), interpolation=cv2.INTER_NEAREST)
        
        self.mask = polygons_mask
        
        return filtered_mask
        
    def get_polygons(self):
        
        polygon_initial_loc = {'id':[],'geometry':[]}

        for i,(x_loc,y_loc) in enumerate(self.cent_local):
                
            ul = [x_loc - self.plot_width/2, y_loc + self.plot_height/2]
            ur = [x_loc + self.plot_width/2, y_loc + self.plot_height/2]
            br = [x_loc + self.plot_width/2, y_loc - self.plot_height/2]
            bl = [x_loc - self.plot_width/2, y_loc - self.plot_height/2]
            
            bbox = np.array([ul,ur,br,bl,ul])
            
            polygon_initial_loc['id'].append(i)
            polygon_initial_loc['geometry'].append(sPolygon(bbox))
            
        gdf_local = gpd.GeoDataFrame(polygon_initial_loc, geometry='geometry')
        
        return gdf_local
        
            
    def to_geojson(self, gdf, rotation=False):
        
        if rotation:
            gdf['geometry'] = gdf['geometry'].apply(lambda geom: rotate(geom, -self.slope_deg, origin=self.center_geo, use_radians=False))
        
        gdf.set_crs('EPSG:32618', inplace=True)
        gdf.to_crs('EPSG:4326', inplace=True)
        gdf_geojson = gdf.__geo_interface__
        
        return gdf_geojson
    
    
    def grid_filling(self, n_rows, n_cols):
        
        self.n_rows = n_rows
        self.n_cols = n_cols
        
        x_l,y_l = np.array(self.cent_local)[:,0],np.array(self.cent_local)[:,1]

        # Combine the x and y coordinates into a single array
        points = np.column_stack((x_l, y_l))

        # Step 1: Use DBSCAN to detect outliers
        # eps: maximum distance between points to be considered in the same neighborhood
        # min_samples: minimum number of points to form a cluster
        db = DBSCAN(eps=self.plot_width, min_samples=3).fit(points)

        # Step 2: Identify the core points (clusters) and noise points (outliers)
        labels = db.labels_

        # Points labeled as -1 are outliers
        core_points = points[labels != -1]
        x_l = core_points[:,0]
        y_l = core_points[:,1]

        # get del height
        ind = np.lexsort((-y_l.round(1),x_l.round(1)))
        x_ord,y_ord = x_l[ind],y_l[ind]
        dist_list=[]
        for i in range(len(x_ord)-1):
            dist = np.linalg.norm([x_ord[i+1]-x_ord[i], y_ord[i+1]-y_ord[i]])
            dist_list.append(dist)

        hist, edges = np.histogram(dist_list, np.arange(0,int(np.ceil(np.max(dist_list)))))
        dist_arr = np.array(dist_list)
        most_freq_edge = edges[np.argmax(hist)]
        ind_ = np.where((most_freq_edge<=dist_arr) & (dist_arr<(most_freq_edge+1)))
        del_height = np.mean(dist_arr[ind_]) - self.plot_height
        self.del_height = del_height
        
        # get del width
        ind = np.lexsort((x_l.round(1), y_l.round(1)))
        x_ord,y_ord = x_l[ind],y_l[ind]
        dist_list=[]
        for i in range(len(x_ord)-1):
            dist = np.linalg.norm([x_ord[i+1]-x_ord[i], y_ord[i+1]-y_ord[i]])
            dist_list.append(dist)

        hist, edges = np.histogram(dist_list, np.arange(0,int(np.ceil(np.max(dist_list)))))
        dist_arr = np.array(dist_list)
        most_freq_edge = edges[np.argmax(hist)]
        ind_ = np.where((most_freq_edge<=dist_arr) & (dist_arr<(most_freq_edge+1)))
        del_width = np.mean(dist_arr[ind_]) - self.plot_width
        self.del_width = del_width
        
        # grid fill
        xv, yv = np.meshgrid(np.linspace(x_l.min(),x_l.max(),self.n_cols), np.linspace(y_l.min(),y_l.max(),self.n_rows))
        self.grid_coords = np.array([xv.flatten(),yv.flatten()])
        
        rc=[]
        for r,c in itertools.product(range(n_rows),range(n_cols)):
            x,y = xv[r,c],yv[r,c]
            missing_ind = np.where(np.sqrt((x_ord-x)**2 + (y_ord-y)**2) < min(self.plot_width, self.plot_height) - max(del_width, del_height))[0]
            if len(missing_ind)>0:
                pass
            else:
                # print(r,c,ind)
                rc.append([r,c])
                
                        
        img_rotated_resize = np.array(self.img_rotated.resize((self.resize,self.resize)))
        self.predictor.set_image(np.array(img_rotated_resize))

        for r,c in rc:
            x,y = [xv[r,c],yv[r,c]]
            x_img, y_img = (np.array([x,y]) - np.array([self.ext_left,self.ext_down])) / self.x_spacing
            
            mask, _, _ = self.predictor.predict(
                point_coords = np.array([[x_img/self.scale_col, y_img/self.scale_row]]),
                point_labels = np.array([1]),
                multimask_output=False,
            )    
            self.mask.append(mask[0,:,:])
                
        i=1
        polygons_loc={'id':[],'geometry':[]}
        for mask in self.mask:
            mask_, mask_num = label(mask, return_num=True)
            for j in range(mask_num):
                mask_tmp = (mask_==(j+1))
                polygon = polygonize(mask_tmp, convex=True, simplify_tolerance=1)[0]
                xy = np.array(polygon.exterior.xy).transpose() * np.array([self.scale_col, self.scale_row])
                x = xy[:,0]
                y = -xy[:,1]
                transformed_coords = (np.array([x,y])*self.x_spacing + np.array([[self.ext_left],[self.ext_up]])).transpose()
                polygon_loc = sPolygon(transformed_coords)
                
                if polygon_loc.area > (self.plot_width*self.plot_height)-1 and polygon_loc.area < (self.plot_width*self.plot_height)+1:
                    polygons_loc['id']=i
                    polygons_loc['geometry'].append(polygon_loc)
                    i+=1           
                    
        cent_loc = []
        for polygon_loc in polygons_loc['geometry']:
            # x,y, and centroid in geo-coordinate
            cent_loc.append([polygon_loc.centroid.x, polygon_loc.centroid.y])
        self.cent_local = cent_loc

        polygon_filled_loc = {'geometry':[]}
        for x_loc,y_loc in self.cent_local:
            
            ul = [x_loc - self.plot_width/2, y_loc + self.plot_height/2] 
            ur = [x_loc + self.plot_width/2, y_loc + self.plot_height/2]
            br = [x_loc + self.plot_width/2, y_loc - self.plot_height/2]
            bl = [x_loc - self.plot_width/2, y_loc - self.plot_height/2]
            
            bbox_loc = np.array([ul,ur,br,bl,ul])
            
            polygon_filled_loc['geometry'].append(sPolygon(bbox_loc))
            
        gdf_filled = gpd.GeoDataFrame(polygon_filled_loc, geometry='geometry')            
                    
        return gdf_filled

    
    
    def grid_remove(self, gdf, dist_thr=1, dist_thr2=1, cc_coverage_thr=0.5):
        
        cc_coverage=[]
        with rasterio.open(self.data_product.url) as src:
            for geom in gdf.geometry:
                clip, _ = rasterio.mask.mask(src, [geom], crop=True)
                arr = clip.transpose([1,2,0])
                canopeo = self.canopeo(arr)
                cc_coverage.append(np.sum(canopeo) / canopeo.size)

        kdtree = KDTree(np.array(self.cent_local))
        dist, ind = kdtree.query(np.array(self.cent_local), k=3)
        drop_ind=[]
        for i in range(len(self.cent_local)):
            if i not in drop_ind:
                if (dist[i,1:]<dist_thr).any():
                    redundant_ind = ind[i,:][np.where(dist[i,:]<dist_thr)]
                    # print(redundant_ind)
                    best_cc_ind = np.argmax([cc_coverage[i] for i in redundant_ind])
                    # print(best_cc_ind)
                    drop_ind += [val for i,val in enumerate(redundant_ind) if i!=best_cc_ind]
                    
        kdtree2 = KDTree(self.grid_coords.T)
        for i,(x_loc,y_loc) in enumerate(self.cent_local):
            dist2, ind2 = kdtree2.query(np.array([x_loc,y_loc]).reshape(1,-1), k=1)
            if dist2>dist_thr2:
                drop_ind.append(i)
                
        cc_cov_cut_arr = np.where(np.array(cc_coverage)<cc_coverage_thr)[0]
        drop_ind = np.unique(list(drop_ind) + list(cc_cov_cut_arr))

        gdf.drop(drop_ind, inplace=True)
        
        return gdf
    
    
    def assign_row_col(self, gdf, dist_thr=0.5):
        
        gdf['geometry'] = gdf['geometry'].apply(lambda geom: rotate(geom, self.slope_deg, origin=self.center_geo, use_radians=False))
        
        polygon_row_col = {'id':[],
                           'geometry':[], 
                           'row':[], 
                           'col':[]}
        
        kdtree = KDTree(self.grid_coords.T)
        for i,geom in enumerate(gdf.geometry):
            x = geom.centroid.x
            y = geom.centroid.y
            dist, ind = kdtree.query(np.array([x,y]).reshape(1,-1), k=1)
            if dist < dist_thr:
                index = ind[0][0] + 1
                polygon_row_col['id'].append(i)
                polygon_row_col['geometry'].append(geom)
                polygon_row_col['row'].append(self.n_rows - (index // self.n_cols))
                polygon_row_col['col'].append(index % self.n_cols)
        
        gdf_row_col = gpd.GeoDataFrame(polygon_row_col, geometry='geometry')    
        
        return gdf_row_col
        