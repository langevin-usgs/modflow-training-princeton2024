import flopy
import numpy as np

# Functions for generating disv model grid and identifying which zone the cells fall into
def split_list(a_list):
    half = len(a_list)//2
    return a_list[:half], a_list[half:]


def read_dims(flname):
    with open(flname, "r") as f:
        for line in f:
            if "DIMENS" in line:
                line = next(f)
                m_arr = line.strip().split()
                nnode = int(m_arr[0])
                nelement = int(m_arr[1])
                break
    
    return nnode, nelement


def read_nodes(flname, nelement):
    iverts = []
    with open(flname, "r") as f:
        for line in f:
            if "NODE" in line:
                for i in np.arange(nelement):
                    line = next(f)
                    m_arr = line.strip().split()
                    iverts.append([i] + [int(itm) - 1 for itm in m_arr])
                
                break
    
    return iverts


def read_coords(flname):
    all_vals = []
    with open(flname, "r") as f:
        for line in f:
            if "COOR" in line:
                line = next(f)
                while "GK_COOR" not in line:
                    m_arr = line.strip().split(',')
                    for val in m_arr:
                        if not val == '':
                            all_vals.append(float(val))
                    
                    line = next(f)
                
                break
    
    return all_vals


def process_verts(iverts, verts):
    xc, yc = [], []
    xyverts = []
    for iv in iverts:
        xv, yv = [], []
        for v in iv[1:]:
            tiv, txv, tyv = verts[v]
            xv.append(txv)
            yv.append(tyv)
        
        xc.append(np.mean(xv))
        yc.append(np.mean(yv))
        xyverts.append(list(zip(xv, yv)))
    
    return xc, yc, xyverts


def get_bnd_inflow_locs(verts):
    left_bnd_verts = []
    
    for itm in verts:
        xcoord = itm[1]
        ycoord = itm[2]
        
        if ycoord >= 15 and ycoord <= 35:
            if xcoord < 0.5:
                left_bnd_verts.append(itm)
    
    return left_bnd_verts


def generate_bnd_features(verts, iverts, left_bnd_verts):
    # Store the ids of the new features
    inQ_feat = []
    
    for i in np.arange(len(left_bnd_verts) - 1):
        pt1 = left_bnd_verts[i]
        pt1_id = pt1[0]
        pt1_y = pt1[2]
        pt2 = left_bnd_verts[i+1]
        pt2_id = pt2[0]
        pt2_y = pt2[2]
        if i == 0:
            newpt3 = [len(verts), 0.0, pt2_y]
            newpt4 = [len(verts) + 1, 0.0, pt1_y]
            # Store the vertices 
            verts.append(newpt3) 
            verts.append(newpt4) 
        else:
            newpt3 = [len(verts), 0.0, pt2_y]
            # Store the vertex
            verts.append(newpt3)
        
        # add the new ivert to list iverts
        if i == 0:
            new_ivert = [len(iverts), pt1_id, pt2_id, newpt3[0], newpt4[0]]
        else:
            new_ivert = [len(iverts), pt1_id, pt2_id, newpt3[0], prev_pt3[0]]
        
        iverts.append(new_ivert)
        inQ_feat.append(new_ivert)
        
        # pt 3 will become pt4 in the next feature
        prev_pt3 = newpt3
        
    # Return
    return verts, iverts, inQ_feat


def create_cell2d(iverts, xyverts, xc, yc):
    cell2d = []
    for ix, iv in enumerate(iverts):
        xv, yv = np.array(xyverts[ix]).T
        if flopy.utils.geometry.is_clockwise(xv, yv):
            rec = [iv[0], xc[ix], yc[ix], len(iv[1:])] + iv[1:]
        else:
            iiv = iv[1:][::-1]
            rec = [iv[0], xc[ix], yc[ix], len(iiv)] + iiv
        
        cell2d.append(rec)
    
    return cell2d


def read_finite_element_mesh(flname):
    # Read dimensions
    nnode, nelement = read_dims(flname)
    
    # Read in vertices
    iverts = read_nodes(flname, nelement)
    
    # Read in continuous list of FEFLOW node coordinates
    # (assumes all x come first, then all y)
    all_vals = read_coords(flname)
    
    # Stitch coord locations together
    all_x, all_y = split_list(all_vals)
    verts = []
    for i, (x, y) in enumerate(zip(all_x, all_y)):
        verts.append([int(i), float(x), float(y)])
    
    # Create rectangular this boundary cells where specified inflows will enter
    left_bnd_verts = get_bnd_inflow_locs(verts)
    # sort, upper to lower
    left_bnd_verts.sort(key=lambda x: x[2], reverse=True)          
    # generate new 2d DISV objects for inflow
    verts, iverts, inQ_iverts = generate_bnd_features(verts, iverts, left_bnd_verts)
    
    # Calculate cell center locations for each element
    # and store xyverts for later use.
    xc, yc, xyverts = process_verts(iverts, verts)
    
    # Finally create a cell2d record                           
    cell2d = create_cell2d(iverts, xyverts, xc, yc)
    
    # Return disv objects
    return verts, cell2d, inQ_iverts


def determine_zone(cell2d):
    low_k_id = []  
    high_k_id = [] 
    for itm in cell2d:
        id = itm[0]
        y_coord = itm[2]
        if y_coord >= 35.0 or y_coord <= 15.00:
            low_k_id.append(id)
        else:
            high_k_id.append(id)

    low_k_id.sort()
    high_k_id.sort()
    return low_k_id, high_k_id


def determine_bnd(cell2d, verts):
    left_bnd = []
    right_bnd = []
    for itm in cell2d:
        id = itm[0]
        incld_verts = itm[-3:]
        
        xlct = 0
        xrct = 0
        for vert in incld_verts:
            x = verts[vert][1]
            y = verts[vert][2]
            if y >= 15 and y <= 35:
                if x < 0.25:
                    xlct += 1
                    if xlct == 2:
                        left_bnd.append(id)
                
                elif x > 135.0 - 0.01:
                    xrct += 1
                    if xrct == 2:
                        right_bnd.append(id)
    
    return left_bnd, right_bnd


def determine_param(low_k_id, high_k_id, val_zn1, val_zn2, mode):
    msg0 = 'Missing an index'
    msg1 = 'Missing ID is: '
    p_arr = []

    id_max = np.max([np.max(low_k_id), np.max(high_k_id)])
    assert len(low_k_id + high_k_id) == id_max + 1, msg0
    for idx in np.arange(id_max + 1):
        if idx in low_k_id:
            p_arr.append(val_zn2)
        elif idx in high_k_id:
            p_arr.append(val_zn1)
        else:
            assert False, msg1 + str(idx) + " (0-based)"

    return p_arr
