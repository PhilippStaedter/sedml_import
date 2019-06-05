# script to compute a linear regression given the data points (x_i,y_i)

import numpy as np

def linearRegression(tsv_file, x_catagory, y_catagory):

    if len(tsv_file[x_catagory]) != len(tsv_file[y_catagory]):
        print('Error: Length of catagories does not match!')

    # take those num_x and num_p where 'error_message' == nan
    x_data_point = []
    y_data_point = []
    for iCount in range(0, len(tsv_file[x_catagory])):
        if type(tsv_file['error_message'][iCount]) != type(x_catagory):
            x_data_point.append(tsv_file[x_catagory][iCount])
            y_data_point.append(tsv_file[y_catagory][iCount])

    Num_data_points = len(x_data_point)
    x_data_point = np.asarray(x_data_point)
    y_data_point = np.asarray(y_data_point)

    # solve linear system of equations Ax = b
    A = np.asarray([[Num_data_points, sum(x_data_point)], [sum(x_data_point), sum(x_data_point*x_data_point)]])
    c = np.asarray([[sum(y_data_point)],[sum(x_data_point*y_data_point)]])
    A_inv = np.linalg.inv(A)

    numerical_solution = A_inv.dot(c)
    a = numerical_solution[0]
    b = numerical_solution[1]

    return a,b