def rotate_points_90_clock_wise(my_points,img):
    assert type(my_points) == list
    assert len(my_points) > 0
    original_img_shape = img.shape
    rotated_img_shape = (original_img_shape[1],original_img_shape[0],original_img_shape[2])
    HEIGHT = rotated_img_shape[0]
    WIDTH =  rotated_img_shape[1]
    rotated_points = []
    for my_point in my_points:
        assert type(my_point) == tuple
        X_Temp = my_point[0]
        X = WIDTH - my_point[1]
        Y = X_Temp
        rotated_point = (X,Y)
        rotated_points.append(rotated_point)
    return rotated_points

def rotate_points_90_counter_clock_wise(my_points,img):
    assert type(my_points) == list
    assert len(my_points) > 0
    original_img_shape = img.shape
    rotated_img_shape = (original_img_shape[1],original_img_shape[0],original_img_shape[2])
    HEIGHT = rotated_img_shape[0]
    WIDTH =  rotated_img_shape[1]
    rotated_points = []
    for my_point in my_points:
        assert type(my_point) == tuple
        Y_Temp = my_point[1]
        Y = HEIGHT - my_point[0]
        X = Y_Temp
        rotated_point = (X,Y)
        rotated_points.append(rotated_point)
    return rotated_points

def rotate_points_180(my_points,img):
    assert type(my_points) == list
    assert len(my_points) > 0
    rotated_points = []
    for my_point in my_points:
        assert type(my_point) == tuple
        X = img.shape[1] - my_point[0]
        Y = img.shape[0] - my_point[1]
        rotated_point = (X,Y)
        rotated_points.append(rotated_point)
    return rotated_points


def draw_polygon(my_points, img):
    my_points_arr = np.array(my_points,np.int32)
    my_points_arr = my_points_arr.reshape(-1,1,2)
    img = cv.polylines(img,[my_points_arr],True,(255,0,0))
    return img
