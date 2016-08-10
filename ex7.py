from SolveLinear3 import solve_linear_3


def is_point_inside_triangle(point, v1, v2, v3):
    '''
    this func checks if the point given is inside the triangle.
    v1,v2,v3 are the coardinates of each corner in the triangle, we call the 
    func solve_linear_3 to check if the point is inside the 3 corners(those
    create a triangle). if it is we return true, if not false.
    '''
    POINT_X = 0
    POINT_Y = 1
    DEFAULT = 1
    ZERO = 0
    coefficients_list = []
    lst_x = [v1[POINT_X],v2[POINT_X],v3[POINT_X]]# we want all the x axis
    lst_y = [v1[POINT_Y],v2[POINT_Y],v3[POINT_Y]]# here all the y axis
    lst_1 = [DEFAULT,DEFAULT,DEFAULT]
    coefficients_list.append(lst_x)
    coefficients_list.append(lst_y)
    coefficients_list.append(lst_1)     
    right_hand_list = [point[POINT_X],point[POINT_Y],DEFAULT] 
    a,b,c = solve_linear_3(coefficients_list,right_hand_list)
    if a < ZERO or b < ZERO or c < ZERO:
        return False ,(a,b,c)
    else:
        return True ,(a,b,c)


def create_triangles(list_of_points):
    '''
    this func first makes triangle from the corners of the img. next it makes
    triangles for the next points in the list. 
    '''
    FIRST_4_POINTS = 4
    AFTER_4_POINTS = 4
    INITIALIZED = 0
    UPDATE_COUNTER = 1

    first_points = list_of_points[:FIRST_4_POINTS] 
    triangle_lst = []
    #get the points from the list, make from them 2 triangles
    v1,v3,v4 = [first_points[0],first_points[2],first_points[3]]
    v1,v2,v3 = [first_points[0],first_points[1],first_points[2]]
    triangle_lst.append((v1,v3,v4))
    triangle_lst.append((v1,v2,v3)) # make from all triangles one list

    #go through the list after we went through the 4 first points.
    for i in list_of_points[AFTER_4_POINTS:]:
        index = INITIALIZED
        #length of the list we've made of the first points
        while index < len(triangle_lst):
            #check for point(in or not the triangle) with vertexes 1, 2 and 3.
            in_or_out = is_point_inside_triangle(i,triangle_lst[index][0], \
                                                    triangle_lst[index][1],\
                                                    triangle_lst[index][2])[0]
            if in_or_out == True:
                # we pop the triangle we found the point in, and insert
                #instead of him the 3 new triangles(each of them push the 
                #other one to the next place). 
                remove_triangle = triangle_lst.pop(index)
                #we have 3 new triangles
                triangle_lst.insert(index,(i,remove_triangle[0], \
                                            remove_triangle[1]))
                triangle_lst.insert(index,(i,remove_triangle[0], \
                                            remove_triangle[2]))
                triangle_lst.insert(index,(i,remove_triangle[1], \
                                            remove_triangle[2])) 
                break
            else:
                index += UPDATE_COUNTER

    return triangle_lst

def do_triangle_lists_match(list_of_points1, list_of_points2):
    '''
    in this func we check if the index of the point we chose in the first 
    image has the same index of the point we chose in the second image, 
    and if its in the same triangles. if it is we return true, if not false. 
    '''
    FIRST_PLACE = 0
    triangle_list1 = create_triangles(list_of_points1)
    triangle_list2 = create_triangles(list_of_points2)

    for i in range(len(list_of_points1)) :
        point_i_1 = list_of_points1[i] 
        point_i_2 = list_of_points2[i]
        for j in range(len(triangle_list1)):
            v1,v2,v3 = triangle_list1[j] #we want each vertex from the triangle
            v4,v5,v6 = triangle_list2[j]
            in_out1 = is_point_inside_triangle(point_i_1,v1,v2,v3)[FIRST_PLACE]
            in_out2 = is_point_inside_triangle(point_i_2,v4,v5,v6)[FIRST_PLACE]
            if in_out1 != in_out2:
                return False
    return True

def get_point_in_segment(p1, p2, alpha):
    '''
    this func calculates the coardinates of a point that is between the 
    distance of p1 and p2, depends on the given alpha.
    '''
    DEFAULT = 1
    p1x,p1y = p1 #get the x's and y's
    p2x, p2y = p2
    #calculates value for the chosen point on the distance between p1 and p2
    vx = (DEFAULT-alpha) * p1x + alpha * p2x  
    vy = (DEFAULT-alpha) * p1y + alpha * p2y
    relevent_point = (vx,vy)
    return relevent_point



def get_intermediate_triangles(source_triangles_list,target_triangles_list,
                                alpha):
    '''
    in this func we want to create new triangle that is between the two other
    triangles (matched couples between im1 and im2). when in the end it returns 
    a list of all the new triangles. 
    '''
    UPDATE_COUNTER = 1
    middle_triangle_lst = []
    for i in range(len(source_triangles_list)):
        source_i = source_triangles_list[i]
        target_i = target_triangles_list[i]
        j = 0
        lst_points = []
        while j < len(source_i):
            source_j = source_i[j]
            target_j = target_i[j]
            #we calculate the point
            point = get_point_in_segment(source_j,target_j,alpha)
            lst_points.append(point) #add new points to the list
            j += UPDATE_COUNTER
        middle_triangle_lst.append(tuple(lst_points))
    return middle_triangle_lst

# until here should be submitted by next week - 18.12.2014


def get_array_of_matching_points(size,triangles_list ,
                                 intermediate_triangles_list):
    '''
    in this func we want to make a new list of lists with new values of x,y   
    that matches between the intermediate triangles and the source or target 
    ones(doesnt matter which one). 
    for that we take a point from the size argument, which holds inside values 
    for x and y. then, we check if the point is inside the intermediate 
    triangle, if it is we want to make a new x,y according to the given 
    formula. we go through all the x,y in the size, until we get all of them, 
    we get a new list of lists, with new x,y.  
    '''
    x_y_tag_lst = []
    POINT_X = 0
    POINT_Y = 1
    TRUE_FALSE = 0
    VALUE_A_B_C = 1
    for j in range(size[POINT_X]): # i run through all the x                
        x_y_tag_lst.append([]) #make an inside list 
        for index in range(size[POINT_Y]): #i run through all the y        
            point = (j,index)
            counter = 0
            #to go through all the triangles in the intermediate
            while counter < len(intermediate_triangles_list):  
                Vertex1,Vertex2,Vertex3 = intermediate_triangles_list[counter]
                #check if the point is in the triangle or not
                in_out = is_point_inside_triangle(point,Vertex1,Vertex2,\
                                                    Vertex3)[TRUE_FALSE]
                #take the same triangle from the regular one (source or target) 
                v1,v2,v3 = triangles_list[counter] 
                v1x,v1y = v1
                v2x,v2y = v2
                v3x,v3y = v3
                if in_out == True:
                    a,b,c = is_point_inside_triangle(point,Vertex1,Vertex2,\
                                                        Vertex3)[VALUE_A_B_C]
                    #make the x and y tags
                    x_tag = a * v1x + b * v2x + c*v3x 
                    y_tag = a * v1y + b * v2y + c*v3y
                    # i have a new point of tags
                    x_y_tag = (x_tag,y_tag) 
                    x_y_tag_lst[j].append(x_y_tag) #put it into the index
                    break
                else:
                    counter += 1

    return x_y_tag_lst
                        

def create_intermediate_image(alpha, size, source_image, target_image,
                              source_triangles_list, target_triangles_list):
    '''
    this func takes the matching points between the source and the intermediate
    triangles (source arry) and the same with the target and the intermediate 
    triangles (target arry). with the source arry points the func gets the RGB 
    from the source image and it does the same with the target.
    then, with that, the whole RGB the func gets from all the points, it makes 
    a list of lists which holds inside all the new RGB. 
    this is the intermadiate image. 
    '''
    #list of intermediate triangles
    intermediate_triangles_list = get_intermediate_triangles \
                                    (source_triangles_list, \
                                    target_triangles_list,alpha)
    #list of matching points between source and median (list of lists)
    arry_source= get_array_of_matching_points(size,source_triangles_list, \
                                                intermediate_triangles_list)  
    #list of matching points between target and median (list of lists)
    arry_target= get_array_of_matching_points(size,target_triangles_list, \
                                                intermediate_triangles_list)
    image = [] # create a new list
    INNER_LIST = 0
    POINT_X = 0
    POINT_Y = 1
    RED = 0
    GREEN = 1
    BLUE = 2
    DEFAULT = 1

    for j in range(len(arry_source)): # i want to run through the len 500 
        #after it finishes the loop, it adds one more list with the size 
        #of 350
        image.append([])
        #run through the len of 350, the inner list 
        for i in range(len(arry_source[INNER_LIST])):
            # i want the x,y of the source and target
            source_match_point = arry_source[j][i] 
            target_match_point = arry_target[j][i]
            #this is the RGB for x,y of the source and target
            source_RGB = source_image[source_match_point[POINT_X], \
                                        source_match_point[POINT_Y]] 
            target_RGB = target_image[target_match_point[POINT_X], \
                                        target_match_point[POINT_Y]] 
            RGB_red = (DEFAULT - alpha) * source_RGB[RED] + alpha * \
                                                        target_RGB[RED]
            RGB_green = (DEFAULT - alpha) * source_RGB[GREEN] + alpha * \
                                                        target_RGB[GREEN]
            RGB_blue = (DEFAULT - alpha) * source_RGB[BLUE] + alpha * \
                                                        target_RGB[BLUE]
            #now i have a matching RGB
            matching_RGB = (int(RGB_red),int(RGB_green),int(RGB_blue)) 
            # i add in the same place the matching x,y were.
            image[j].append(matching_RGB) 
    return image
            
           



def create_sequence_of_images(size, source_image, target_image, 
                source_triangles_list, target_triangles_list, num_frames): 
    '''
    this func creates new images consider the num of frames it gets.
    it calculates the alpha with the formula,then create the intermediate image
    using the create_intermediate_image func. it makes images like that as 
    the num frames it gets.  
    '''
    LAST_NUM_FRAME = 1      
    lst_of_frames = []    
    for i in range(num_frames):
        alpha = i / (num_frames - LAST_NUM_FRAME)
        # getting a list of the pixels in the median image (list of lists)
        image = create_intermediate_image(alpha, size, source_image, \
                                            target_image, \
                                            source_triangles_list, \
                                            target_triangles_list)        
        lst_of_frames.insert(i,image)
    return lst_of_frames


    





