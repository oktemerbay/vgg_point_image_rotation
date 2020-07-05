import argparse
import point_rotation
import json
import sys
import cv2 as cv
import os
import numpy as np
import time

rotation_degree_dict = {'90_clock_wise':[cv.ROTATE_90_CLOCKWISE,point_rotation.rotate_points_90_clock_wise],
                   '90_counter_clock_wise':[cv.ROTATE_90_COUNTERCLOCKWISE,point_rotation.rotate_points_90_counter_clock_wise],
                   '180':[cv.ROTATE_180,point_rotation.rotate_points_180]}



def main():

    def get_rotation_degree(rotation_degree):
        assert rotation_degree != None and len(rotation_degree) > 0
        for key in rotation_degree_dict:
            if key == rotation_degree:
                return rotation_degree_dict[key]

        
    def get_rotation_degree_method(rotation_degree_arr):
        assert rotation_degree_arr != None and len(rotation_degree_arr) == 2
        return rotation_degree_arr[1]

    def get_rotation_degree_orientation(rotation_degree_arr):
        assert rotation_degree_arr != None and len(rotation_degree_arr) == 2
        return rotation_degree_arr[0]


    def get_rotated_image_key(image_key,rotation_degree):
        assert image_key != None and len(image_key) > 0
        return image_key + "_" +rotation_degree

    def get_rotated_img_by_img(img,rotation_degree):
        assert img is not None
        rotation_degree_arr = get_rotation_degree(rotation_degree)
        if rotation_degree_arr != None:
            rot_met = get_rotation_degree_orientation(rotation_degree_arr)
            img = cv.rotate(img,rot_met)
            return img


    def get_abs_filename(folderpath,filename):
        filename = os.path.join(folderpath,filename)
        return filename;

    def get_file_size(folderpath,filename):
        assert filename != None and len(filename) > 0
        filename = get_abs_filename(folderpath,filename)
        if os.path.exists(filename):
            return os.stat(filename).st_size

    def get_file_name_by_image_key(image_list,my_key):
        if my_key != None and len(my_key) > 0:
            for image_key in image_list:
                image_value = image_list[image_key]
                if my_key == image_key:
                    return image_value['filename']

    def save_img(folderpath ,filename,img):
        assert filename != None and len(filename) > 0 and img is not None
        filename = get_abs_filename(folderpath,filename)
        cv.imwrite(filename,img)


    def get_rotated_region_by_key(rotated_file_region_points,my_key):
        if my_key != None and len(my_key) > 0:
            region_value_arr = []
            for rotated_file_region_point in rotated_file_region_points:
                for image_key , region_value in rotated_file_region_point.items():
                    if my_key == image_key:
                        region_value_arr.append(region_value)
            return region_value_arr

    def convert_points_to_all_points_x_and_y(points):
        assert type(points) == list
        if points != None and len(points) > 0:
            all_points_x = []
            all_points_y = []
            for point in points:
                all_points_x.append(point[0])
                all_points_y.append(point[1])
            return all_points_x , all_points_y       

    def get_splitted_filename_prefix_suffix(filename):
        assert filename != None and len(filename) > 0
        prefix = filename[0:filename.rindex('.')]
        suffix = filename[filename.rindex('.') + 1:len(filename)]
        return prefix , suffix

    def get_rotated_filename(filename,rotation_degree):
        assert filename != None and len(filename) > 0
        prefix , suffix = get_splitted_filename_prefix_suffix(filename)
        rotated_filename = prefix + '_' + rotation_degree +'_degree_rotated.'+suffix
        return rotated_filename

    def get_region_attribute_by_image_key_and_index(image_list,image_key,index):
        assert image_list != None and image_key != None and len(image_key) > 0 and index != None
        if image_key in image_list and image_list[image_key] is not None:
            _m_json_data = image_list[image_key]
            if "regions" in _m_json_data:
                if "region_attributes" in _m_json_data["regions"][index]:
                    return  _m_json_data["regions"][index]["region_attributes"]

    def get_shape_attribute_by_image_key_and_index(image_list,image_key,index):
        assert image_list != None and image_key != None and len(image_key) > 0 and index != None
        if image_key in image_list and image_list[image_key] is not None:
            _m_json_data = image_list[image_key]
            if "regions" in _m_json_data:
                if "shape_attributes" in _m_json_data["regions"][index]:
                    return  _m_json_data["regions"][index]["shape_attributes"]

    def get_file_attributes_by_image_key(image_list,image_key):
        assert image_list != None and image_key != None and len(image_key) > 0
        if image_key in image_list and image_list[image_key] is not None:
            _m_json_data = image_list[image_key]
            if "file_attributes" in _m_json_data:
                return _m_json_data["file_attributes"]


    def get_rotation_degree_dict_keys():
        rotation_degree_key_set = []
        for key in rotation_degree_dict:
            rotation_degree_key_set.append(key)
        return rotation_degree_key_set


    def is_paths_valid(folderpath,model_file_name):
        assert folderpath != None and len(folderpath) > 0 and model_file_name != None and len(model_file_name) > 0
        joined_path = os.path.join(folderpath,model_file_name)
        is_joined_path_exist = os.path.exists(joined_path)
        if not is_joined_path_exist:
            print(joined_path ,' does not exist')
            return False
        return True

    def is_rotation_degree_valid(rotation_degree):
        assert rotation_degree != None and len(rotation_degree) > 0
        for key in rotation_degree_dict:
            if key == rotation_degree:
                return True
        if rotation_degree == 'all':
            return True
        print("rotation_degree is not valid , must be one of ; ",get_rotation_degree_dict_keys())
        return False

    def validate_params(folder_path,model_file_name,rotation_degree):
        val_res = is_paths_valid(folder_path,model_file_name)
        if val_res:
            val_res = is_rotation_degree_valid(rotation_degree)
            if not val_res:
                return False
        else:
            return False
        return True
    
    
    class Image_Json_Dom:
        def __init__(self):
            self.image_key = ''
            self.filename = ''
            self.size = None #int olacak
            self.regions = []
            self.file_attributes = {}

        def __str__(self):
            return 'image_key:'+self.image_key+'\n'+'filename:'+self.filename +'\n'+'size:'+str(self.size)+'\n'+'regions:'+str(self.regions)+ '\n'

        def _get_json_data(self):
            _json_data = {
                self.image_key:{
                    "filename":self.filename,
                    "size":self.size,
                    "regions":self.regions,
                    "file_attributes":self.file_attributes
                }
            }
            return _json_data


    def process_json(folderpath,rotation_degree,model_file_path):
        with open(model_file_path,'r') as model_file:
            data = json.load(model_file)
            image_list = data['_via_img_metadata']
            image_id_list = data['_via_image_id_list']

            counter = 0
            file_region_points = [];
            rotated_file_region_points = []
            for image_key in image_list:
                filename = image_list[image_key]['filename']
                regions = image_list[image_key]['regions']
                region_points = []
                for i in range(len(regions)):
                    region = regions[i]
                    points = []
                    shape_attributes = region['shape_attributes']
                    points_x = shape_attributes['all_points_x']
                    points_y = shape_attributes['all_points_y']
                    assert len(points_x) == len(points_y) and len(points_x) > 0
                    for i in range(len(points_x)):
                        point_x = points_x[i]
                        point_y = points_y[i]
                        points.append((point_x,point_y))
                    region_points.append(points)

                file_region_points.append({image_key:region_points})
                #counter += 1
                #if counter == 1:    
                #    break

            for i in range(len(file_region_points)):
                for image_key , file_regions in file_region_points[i].items():
                    filename = get_file_name_by_image_key(image_list,image_key)
                    img = cv.imread(get_abs_filename(folderpath,filename))
                    for file_region in file_regions:
                        rotation_degree_arr = get_rotation_degree(rotation_degree)
                        if img is not None:
                            rotated_region = rotation_degree_arr[1](file_region,img)
                            rotated_file_region_points.append({image_key:rotated_region})

            if rotated_file_region_points != None and len(rotated_file_region_points) > 0:
                image_list_to_add = {}
                for image_key in image_list:
                    rotated_region_value_arr = get_rotated_region_by_key(rotated_file_region_points,image_key)
                    if rotated_region_value_arr != None:
                        filename = get_file_name_by_image_key(image_list,image_key)
                        img = cv.imread(get_abs_filename(folderpath,filename))
                        if img is not None:
                            img_rotated = get_rotated_img_by_img(img,rotation_degree)
                            rotated_file_name = get_rotated_filename(filename,rotation_degree)
                            save_img(folderpath,rotated_file_name,img_rotated) ## img saved
                            rotated_file_size = get_file_size(folderpath,rotated_file_name)
                            rotated_image_key = get_rotated_image_key(image_key,rotation_degree)
                            image_json_dom = Image_Json_Dom()
                            image_json_dom.image_key = rotated_image_key
                            image_json_dom.filename = rotated_file_name
                            image_json_dom.size = rotated_file_size
                            image_json_dom.regions = []
                            for index in range(len(rotated_region_value_arr)):
                                rotated_region_value = rotated_region_value_arr[index]
                                if rotated_region_value != None:
                                    all_points_x , all_points_y = convert_points_to_all_points_x_and_y(rotated_region_value)
                                    _shape_attributes = get_shape_attribute_by_image_key_and_index(image_list,image_key,index)
                                    _shape_attributes_json = {
                                        "name":_shape_attributes.get("name"),
                                        "all_points_x": all_points_x,
                                        "all_points_y": all_points_y
                                    }
                                    _region_attributes = get_region_attribute_by_image_key_and_index(image_list,image_key,index)
                                    _region_attributes_json ={
                                        "region_attributes":_region_attributes
                                    }
                                    image_json_dom.regions.append({"shape_attributes":_shape_attributes_json})
                                    image_json_dom.regions.append({"region_attributes":_region_attributes_json})
                                    image_json_dom.file_attributes = get_file_attributes_by_image_key(image_list,image_key)
                                    image_list_to_add.update(image_json_dom._get_json_data())

                image_id_list_to_add = []
                for image_id_key in image_list_to_add:
                    image_id_list_to_add.append(image_id_key)
                return data,image_list_to_add,image_id_list_to_add
                

    parser = argparse.ArgumentParser(description='Enter fields.')
	
    parser.add_argument('--folder_path', metavar='--folder_path', type=str, required=True,
						help='Enter the folder path of your training set')
	
    parser.add_argument('--model_file_name', metavar='--model_file_name', type=str, required=True,
						help='Enter the model file name of your training set')
	
    parser.add_argument('--rotation_degree', metavar='--rotation_degree', type=str, required=True,
						help='Enter the rotation degree for your training set (90_clock_wise,90_counter_clock_wise or 180)')

	
    args = parser.parse_args()
    folderpath = args.folder_path
    model_file_name = args.model_file_name
    rotation_degree = args.rotation_degree
	
    val_res = validate_params(folderpath,model_file_name,rotation_degree)
    if not val_res:
      print("Params are not valid")
      return
	
    model_file_path = os.path.join(folderpath,model_file_name)

    _image_list_to_add = {}
    _image_id_list_to_add = []
    _data = None
    if rotation_degree == "all":
        for rot_degree in rotation_degree_dict:
            rotation_degree = rot_degree
            _data,__image_list_to_add , __image_id_list_to_add = process_json(folderpath,rotation_degree,model_file_path)
            #print(__image_list_to_add)
            _image_list_to_add.update(__image_list_to_add)
            _image_id_list_to_add.extend(__image_id_list_to_add)
    else:
        _data,__image_list_to_add ,__image_id_list_to_add = process_json(folderpath,rotation_degree,model_file_path)
        _image_list_to_add.extend(__image_list_to_add)
        _image_id_list_to_add.extend(__image_id_list_to_add)
    
    
    
    _image_list = _data['_via_img_metadata']
    _image_id_list = _data['_via_image_id_list']
    
    _image_list.update(_image_list_to_add)
    _image_id_list.extend(_image_id_list_to_add)
    
    out_put_file_name = str(int(time.time() * 1000))+'.json'
    out_put_file_name = os.path.join(folderpath,out_put_file_name)


    with open(out_put_file_name,'w') as model_file_to_write:
        json.dump(_data,model_file_to_write)
        print("Created model file is ",out_put_file_name)	



	

if __name__ == "__main__":
	main()
