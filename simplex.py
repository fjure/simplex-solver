import numpy as np
import time
import sys

from parser import *

# DER FOLGENDE ALGORITHMUS BASIERT KOMPLETT AUF DEN REGELN DIE AUF www.atozmath.com VERWENDET WERDEN. DIESER NUTZT DEN DUALEN SIMPLEX UND DIE MINIMUM RATIO METHODE UM DAS PIVOT ELEMENT ZU BESTIMMEN

np.set_printoptions(edgeitems=30, linewidth=100000, suppress=True)

def init(initial, mode):
    if mode == "min":
        return np.multiply(initial, -1)
    else:
        # TODO: NOT IMPLEMENTED YET
        return


def add_slack_variables(matrix):
    # calculate how many extra variables we need
    global num_rows, num_cols
    
    num_rows, num_cols = matrix.shape
    needed_variables = num_rows - 1
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
    most_negative_number_index = np.argmin(x_b)
    most_negative_number = x_b[most_negative_number_index]

    c_row = matrix[-1, :]
    z_minus_c = np.subtract(z_row, c_row)

    pivot_row = matrix[most_negative_number_index, :]

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

    max_negative_number_index = np.argmax(ratio)
    max_negative_number = ratio[max_negative_number_index]

    pivot_element = matrix[most_negative_number_index, max_negative_number_index]

    return most_negative_number_index, max_negative_number_index

def manipulate_matrix(matrix, pivot_position):
    pivot_row = matrix[pivot_position[0], :]
    pivot_row = np.true_divide(pivot_row, matrix[pivot_position], dtype=np.longdouble)
    matrix[pivot_position[0], :] = pivot_row
    for i in range(0, num_rows):
        if(i != pivot_position[0]):
            new_row = matrix[i, :]
            coefficient = np.multiply(new_row[pivot_position[1]], -1)
            new_row = np.add(new_row, np.multiply(pivot_row, coefficient))
            matrix[i, :] = new_row
    
    return matrix
    

def check_for_finish(matrix):
    return True if np.all(matrix[:, -1] >= 0) else False

def print_solution(matrix):
    solutions = []
    matrix_without_slack_variables = matrix[:, 0:num_cols-1]
    last_column = matrix[:, -1]
    for i in range(0, matrix_without_slack_variables.shape[1]):
        current_column = matrix_without_slack_variables[:, i]
        if np.max(current_column) > 1 or np.min(current_column) < 0:
            continue
        elif 1 in current_column:
            index = np.argwhere(current_column == 1).item()
            solutions.append(f'x{i}: {last_column[index]}')
    return matrix, iterations, matrix[-1, -1], solutions


def start(parsed, mode):
    init_matrix = init(np.asarray(parsed), mode)
    new_matrix = add_slack_variables(init_matrix)
    global z_row
    z_row = np.zeros(new_matrix.shape[1])
    global iterations
    iterations = 0
    finished = False
    global variables_solutions
    while finished is False:
        pivot_position = find_pivot_position(new_matrix)
        new_matrix = manipulate_matrix(new_matrix, pivot_position)
        iterations += 1
        finished = check_for_finish(new_matrix)
    if finished:
        return print_solution(new_matrix)

