from py4design import py3dmodel
import time
import numpy as np
import json
import sys
import matplotlib
from matplotlib import cm

#color range and lower value
low = 15
rg = 15

#Flip Melexis coordinates?
flip = False

data_path = sys.argv[1]
res_path = sys.argv[2]
#========================================================================================================
#FUNCTIONS
#========================================================================================================
def merge_lidar_temp(data, temp_dlist, bbox_list, res_path, temps, origin = (0,0,0),
                     x_axis = (1,0,0), y_axis = (0,1,0), z_axis = (0,0,1),):
    
    nml_edges = []
    nml_pts = []
    dists = []
    print(len(data["LIDAR"]["Data"]))
    for line_ls in data["LIDAR"]["Data"]:  
        r = line_ls[2]
        if r != 0:
            dists.append(r)
            theta = line_ls[1]
            phi = line_ls[0]
            if theta <= 90:
                theta2 = 90-theta
            else:
                theta2 = theta-90
                theta2 = theta2*-1
    
            mv_pt = py3dmodel.modify.move_pt(origin, x_axis, 1)
            edge1 = py3dmodel.construct.make_edge(origin, mv_pt)
            edge2 = py3dmodel.modify.rotate(edge1, origin, y_axis, theta2)
            edge3 = py3dmodel.modify.rotate(edge2, origin, z_axis, phi)
            nml_pt= py3dmodel.fetch.points_frm_edge(edge3)[1]
            nml_pts.append(nml_pt)
            nml_edges.append(edge3)
    
    # vs = py3dmodel.construct.make_occvertex_list(nml_pts)
    # print(len(vs))
    # py3dmodel.utility.visualise([vs], ['BLUE'])

    #TODO FIGURE OUT THE BEST ARRAY SIZE FOR PROCESSING
    ninterv = 18
    npts = len(nml_pts)
    interv = int(npts/ninterv)
    xyz_str = ''

    #color scheme based on stddev or min/max
    maxval = max(temps)
    minval = min(temps)
    std = np.std(temps)
    mean = np.mean(temps)
    #comment accordingly if you want to use straight min/max or stddev
    #norm = matplotlib.colors.Normalize(vmin = minval, vmax = maxval)
    norm = matplotlib.colors.Normalize(vmin = mean-std, vmax = mean+std)
    colors = cm.ScalarMappable(norm = norm, cmap = 'inferno')
    
    #the number of points is too many to process it all at one go
    for i in range(ninterv):
        start = i*interv
        if i != ninterv-1:
            end = (i+1) * interv    
            #print(i, start, end)
            nml_pts2 = nml_pts[start:end]
            dists2 = dists[start:end]
        else:
            #print(start)
            nml_pts2 = nml_pts[start:]
            dists2 = dists[start:]
            
        indices = py3dmodel.calculate.pts_in_bboxes(nml_pts2, bbox_list, 
                                                    zdim = True)
        pt_indices = indices[0]
        box_indices = indices[1]
        
        uniq, uniq_inds, repeat_inds, rpt_cnt = np.unique(pt_indices, return_index=True, return_inverse=True, 
                                                          return_counts=True, axis=0)
        #print(len(uniq))
        for cnt, pt_ind in enumerate(uniq):
            #print(pt_ind)
            #first get the point
            nml_pt2 = nml_pts2[pt_ind]
            dist = dists2[pt_ind]
            #move the pt to the right xyz
            nml_pt3 = py3dmodel.modify.move_pt(origin, nml_pt2, dist)
            
            #find the corresponding bbox
            nrpt = rpt_cnt[cnt]
            uniq_ind = uniq_inds[cnt]
            start_bbox = uniq_ind
            end_bbox = uniq_ind+nrpt
            temp_indices = box_indices[start_bbox:end_bbox]
            chosen_temp_d = np.take(temp_dlist, temp_indices, axis = 0)

            #of the tmep points find the closest one
            mn_index = find_pts_closest(nml_pt2, chosen_temp_d)
            #then choose the temp and inherit it to the lidar point
            temp = chosen_temp_d[mn_index]['temp']
##            fc = chosen_temp_d[mn_index]['falsecolour']
            # #write to pts file format
            x = nml_pt3[0]
            y = nml_pt3[1]
            z = nml_pt3[2]
##            r = int(fc[0]*255)
##            g = int(fc[1]*255)
##            b = int(fc[2]*255)

            #Choose the color of the point
            rgbs = colors.to_rgba(temp)
            r = int(rgbs[0]*256)
            g = int(rgbs[1]*256)
            b = int(rgbs[2]*256)

##            d = np.sqrt(x**2+y**2+z**2)
##            th = np.arctan2(y,x)
##            if th<0: th = th+2*np.pi
##            ph = np.arccos(z/d)
            
            xyz_str = xyz_str + str(x) + ',' + str(y) + ',' + str(z) + ',' + str(temp) + ',' + str(r) + ',' + str(g) + ',' + str(b) + '\n'
            #xyz_str = xyz_str + str(th) + ',' + str(ph) + ',' + str(d) + ',' + str(temp) + '\n'
        
        res_file = open(res_path, 'w')
        res_file.write(xyz_str)
        res_file.close()

def find_pts_closest(pt, temp_d2check):
    dist_list = []
    for ptd in temp_d2check:
        pt2 = ptd['pt']
        dist = py3dmodel.calculate.distance_between_2_pts(pt, pt2)
        dist_list.append(dist)
        
    mn = min(dist_list)
    mn_index = dist_list.index(mn)
    return mn_index

def temp_sphere2pts(temp_path, origin = (0,0,0), x_axis = (1,0,0), 
                    y_axis = (0,1,0), z_axis = (0,0,1), bbox_xdim = 0.05, 
                    bbox_ydim = 0.05, bbox_zdim = 0.05):
    #reading from csv file
##    temp_file = open(temp_path, 'r')
##    lines = temp_file.readlines()
##    new_temps = []
##    for line in lines:
##        line = line.replace('\n', '')
##        line_ls = line.split(',')
##        line_ls = list(map(float, line_ls))
##        new_temps.append(line_ls)
##    new_temps_zip = list(zip(*new_temps))

    #reading and processing raw json data
    new_temps_zip = read_temps(temp_path)
    
    pts = []
    edges = []
    temps = []
    bbox_list = []
    dlist = []
    boxes = []
    box= py3dmodel.construct.make_box(0.05, 0.05, 0.05)
    
    for new_temp in new_temps_zip:
        d= {}
        phi = new_temp[0]
        theta = new_temp[1]
        temp = new_temp[2]
        mv_pt = py3dmodel.modify.move_pt(origin, x_axis, 1)
        edge1 = py3dmodel.construct.make_edge(origin, mv_pt)
        
        if theta <= 90:
            theta2 = 90-theta
            theta2 = theta2*-1
        else:
            theta2 = theta-90
            theta2 = theta2
        edge2 = py3dmodel.modify.rotate(edge1, origin, y_axis, theta2)
        edge3 = py3dmodel.modify.rotate(edge2, origin, z_axis, phi)
        pt = py3dmodel.fetch.points_frm_edge(edge3)[1]
        bbox = make_bbox_frm_pt(pt, bbox_xdim, bbox_ydim,bbox_zdim)
        mv_box = py3dmodel.modify.move((0,0,0), pt, box)
        boxes.append(mv_box)
        d['pt'] = pt
        d['temp'] = temp
        dlist.append(d)
        pts.append(pt)
        edges.append(edge3)
        temps.append(temp)
        bbox_list.append(bbox)
        
##    temp_file.close()
    
    mx_temp = max(temps)
    mn_temp = min(temps)

    falsecolours = py3dmodel.utility.falsecolour(temps, mn_temp, mx_temp, inverse = False)
    for cnt,d in enumerate(dlist):
        d['falsecolour'] = falsecolours[cnt]
        
    
    return pts, dlist, edges, bbox_list, temps, boxes

def read_temps(data):

    arr = np.zeros((24,32,3,1))
    copy = np.zeros((24,32,3,1))

    final=[]

    #generate the original array coordinates for sensor centered at (0,0)
    for i in range(24):
        for j in range(32):
            #coordinates in spherical
            th = np.radians(-27.5+55/31*(j))
            ph = np.radians(72.5+35/23*(i))
            #coordinates in cartesian
            x = np.cos(th)*np.sin(ph);
            y = np.sin(th)*np.sin(ph);
            z = np.cos(ph);
            arr[i][j]=np.array([[x],[y],[z]])
            copy[i][j]=np.array([[x],[y],[z]])

    for trial in data['Melexis']:
        if flip:
            trial[1][0] = (trial[1][0]+180)%(360)
            trial[1][1] = 180-trial[1][1]
            
        theta = np.radians(trial[1][0])
        phi = np.radians(-(trial[1][1]-90))
        
        #generate rotational matrix
        R = np.array([[np.cos(theta)*np.cos(phi),-1*np.sin(theta),np.cos(theta)*np.sin(phi)],
                      [np.sin(theta)*np.cos(phi),np.cos(theta),np.sin(theta)*np.sin(phi)],
                      [-1*np.sin(phi),0,np.cos(phi)]])
        
        for i in range(24):
            for j in range(32):
                arr[i][j]=copy[i][j].copy()
        for i in range(24):
            for j in range(32):
                rot = R@arr[i][j]
                th = np.degrees(np.arctan2(rot[1],rot[0]))[0]
                if th < 0:
                    th = 360+th
                ph = np.degrees(np.arccos(rot[2]))[0]
                point = (th,ph,trial[0][32*i+j])
                final.append(point)
    return final

def make_bbox_frm_pt(pt, xdim, ydim, zdim):
    x_half = xdim/2
    y_half = ydim/2
    z_half = zdim/2
    xmin = pt[0] - x_half
    xmax = pt[0] + x_half
    ymin = pt[1] - y_half
    ymax = pt[1] + y_half
    zmin = pt[2] - z_half
    zmax = pt[2] + z_half
    return (xmin,ymin,zmin, xmax, ymax, zmax)

def secs2hrsmins_str(seconds):
    taken_mins = seconds/60
    taken_hrs_mins = divmod(taken_mins, 60)
    hr = str(int(taken_hrs_mins[0]))
    mins = str(int(taken_hrs_mins[1]))
    strx = 'Elapsed Time:'+hr+' hr ' + mins + ' mins'
    return strx

#========================================================================================================
#========================================================================================================
#first read the temp file   
with open(data_path) as file:
    data = json.load(file)
time1 = time.perf_counter()
temp_pts, dlist, temp_edges, bbox_list, temps, boxes = temp_sphere2pts(data)
tvs = py3dmodel.construct.make_occvertex_list(temp_pts)
# py3dmodel.utility.visualise([boxes], ['GREEN'])
# py3dmodel.utility.visualise_falsecolour_topo(tvs, temps)

#merge the two dataset, 
merge_lidar_temp(data, dlist, bbox_list, res_path, temps)
time2 = time.perf_counter()
time_taken = time2-time1
time_str = secs2hrsmins_str(time_taken)
print(time_str)
