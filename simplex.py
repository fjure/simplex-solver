import numpy as np
import time

from parser import *

# DER FOLGENDE ALGORITHMUS BASIERT KOMPLETT AUF DEN REGELN DIE AUF www.atozmath.com VERWENDET WERDEN. DIESER NUTZT DEN DUALEN SIMPLEX UND DIE MINIMUM RATIO METHODE UM DAS PIVOT ELEMENT ZU BESTIMMEN

np.set_printoptions(edgeitems=30, linewidth=100000, suppress=True)

def init(initial, mode):
    if mode == "min":
        return np.multiply(initial, -1)
    else:
        return


def add_slack_variables(matrix):
    # calculate how many extra variables we need
    global num_rows, num_cols
    
    num_rows, num_cols = matrix.shape
    needed_variables = num_rows - 1
    print(f'{needed_variables}')
    new_column_size = num_cols + needed_variables
    new_row_size = num_rows

    new_matrix = np.zeros((new_row_size, new_column_size))

    # Fülle mit Schlupfvariablen
    np.fill_diagonal(new_matrix[: ,num_cols-1:], 1)
    # copy transposed matrix into new big matrix
    new_matrix[:, 0:num_cols - 1] = matrix[:, 0:num_cols - 1]
    # access last column of new matrix and paste last column from transposed matrix
    new_matrix[:, -1] = matrix[:, -1]

    return new_matrix


def find_pivot_position(matrix):
    # look for the most negative value (kleinste zahl) in rhs (letzte spalte)
    x_b = matrix[:, -1]
    print(x_b)
    most_negative_number_index = np.argmin(x_b)
    most_negative_number = x_b[most_negative_number_index]
    print(f'index: {most_negative_number_index} number: {most_negative_number}')

    c_row = matrix[-1, :]
    print(f'c_row: {c_row}')

    print(f'z_row: {z_row}')

    z_minus_c = np.subtract(z_row, c_row)
    print(f'z_minus_c: {z_minus_c}')

    pivot_row = matrix[most_negative_number_index, :]
    print(f'pivot_row: {pivot_row}')

    ratio = []
    for i in range(0, z_minus_c.size - 1):
        if(z_minus_c[i] == 0 and pivot_row[i] < 0):
            ratio.append(0)
        elif(z_minus_c[i] == 0 and pivot_row[i] > 0):
            ratio.append(-1000000)
        elif(z_minus_c[i] == 0 and pivot_row[i] == 0):
            ratio.append(-1000000)
        elif(z_minus_c[i] > 0 and pivot_row[i] == 0):
            ratio.append(-1000000)
        elif(z_minus_c[i] > 0 and pivot_row[i] > 0):
            ratio.append(-1000000)
        else:
            ratio.append(np.true_divide(z_minus_c[i], pivot_row[i], dtype=np.longdouble))
        
    np.asarray(ratio)
    print(f'ratio: {ratio}')

    max_negative_number_index = np.argmax(ratio)
    max_negative_number = ratio[max_negative_number_index]
    print(f'index: {max_negative_number_index} number: {max_negative_number}')

    pivot_element = matrix[most_negative_number_index, max_negative_number_index]
    print(f'pivot element: {pivot_element}')

    return most_negative_number_index, max_negative_number_index

def manipulate_matrix(matrix, pivot_position):
    pivot_row = matrix[pivot_position[0], :]
    print(f'pivot_row: {pivot_row}')
    pivot_row = np.true_divide(pivot_row, matrix[pivot_position], dtype=np.longdouble)
    matrix[pivot_position[0], :] = pivot_row
    # TODO:, KOEFFIZIENT IST GLUABE FALSCH
    for i in range(0, num_rows):
        if(i != pivot_position[0]):
            new_row = matrix[i, :]
            #print(f'extracted row {new_row}')
            coefficient = np.multiply(new_row[pivot_position[1]], -1)
            #print(f'{coefficient}')
            new_row = np.add(new_row, np.multiply(pivot_row, coefficient))
            #print(f'calculated {new_row}') 
            matrix[i, :] = new_row
    #print(f'new pivot_col: {pivot_column}')
    

    print(f'new matrix: \n {matrix}')

    return matrix
    

def check_for_finish(matrix):
    return True if np.all(matrix[:, -1] >= 0) else False

def start(parsed):
    init_matrix = init(parsed, "min")
    new_matrix = add_slack_variables(init_matrix)
    global z_row
    z_row = np.zeros(new_matrix.shape[1])
    iterations = 1
    finished = False
    while finished is False:
        pivot_position = find_pivot_position(new_matrix)
        new_matrix = manipulate_matrix(new_matrix, pivot_position)
        iterations += 1
        finished = check_for_finish(new_matrix)
        time.sleep(2)


ki_5 = np.array([[1,1,1,4,5,5], [4,1,4,3,3,9], [5,1,1,4,4,15], [1,3,3,5,2,0]]).astype(np.longdouble)
ki_8 = np.array([[2,2,2,5,7,8,2,5,51], [4,4,3,1,2,7,5,1,1], [8,5,3,6,6,2,2,6,26], [7,8,5,7,8,1,4,7,38], [1,6,6,6,2,6,8,7,0]]).astype(np.longdouble)
ki_9 = np.array([[4,5,4,1,5,2,7,2,9,22], [9,3,8,5,4,1,8,2,2,55], [4,8,1,7,8,6,6,3,9,24], [8,8,6,6,4,4,9,2,5,46], [4,2,3,1,5,9,6,4,4,6], [9,3,2,8,1,3,7,7,5,11], [7,8,3,5,3,1,3,6,8,59], [9,4,6,4,1,3,3,8,7,17], [9,5,3,8,6,8,5,3,1, 0]]).astype(np.longdouble)
ki_15 = np.array([[11,1,11,12,11,9,1,2,3,13,6,12,10,7,6,78], [1,8,1,3,15,9,5,3,7,9,1,8,11,6,15,144], [7,7,7,15,3,8,8,12,9,11,6,5,14,4,5,79], [11,9,2,8,6,7,2,12,10,15,1,11,2,15,12,25], [14,9,7,14,2,5,3,4,1,5,6,9,1,2,4,71], [9,6,1,6,2,11,7,13,8,9,7,14,8,10,9,27], [3,7,8,7,2,15,3,8,15,7,9,4,14,3,10,179], [12,3,6,11,4,10,1,13,1,12,7,9,9,9,4,97], [8,9,3,8,14,14,13,1,7,7,13,13,3,5,2,138], [1,6,1,13,14,8,15,1,8,14,6,7,2,7,4,0]]).astype(np.longdouble)

def solve_all():
  parsedBenchmarks = getParsedBenchmarks()
  solutions = []
  for i, parsed in enumerate(parsedBenchmarks):
    print(parsed)
    start(np.asarray(parsed[0]))

solve_all()

#start(ki_15)
