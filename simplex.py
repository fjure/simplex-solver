import numpy as np
import time
import sys

from parser import *

# DER FOLGENDE ALGORITHMUS BASIERT KOMPLETT AUF DEN REGELN DIE AUF www.atozmath.com VERWENDET WERDEN. DIESER NUTZT DEN DUALEN SIMPLEX UND DIE MINIMUM RATIO METHODE UM DAS PIVOT ELEMENT ZU BESTIMMEN
# DER ALGORITHMUS WIRD MIT DER START FUNKTION AUS DEM MAIN.PY PROGRAMM AUFGERUFEN

np.set_printoptions(edgeitems=30, linewidth=100000, suppress=True)

# Transforms matrix in case it is a minimization problem by mulitplying it by (-1). 
def init(initial, mode):
    if mode == "min":
        return np.multiply(initial, -1)
    else:
        # TODO: NOT IMPLEMENTED YET
        return

# Adds number of slack variables to the matrix and fills them with diagonal 1 shape (Dreiecksform)
def add_slack_variables(matrix):
    # Calculate how many extra variables we need
    global num_rows, num_cols
    num_rows, num_cols = matrix.shape
    needed_variables = num_rows - 1
    new_column_size = num_cols + needed_variables
    new_row_size = num_rows

    new_matrix = np.zeros((new_row_size, new_column_size))

    np.fill_diagonal(new_matrix[: ,num_cols-1:], 1)
    # Copy transposed matrix into new big matrix
    new_matrix[:, 0:num_cols - 1] = matrix[:, 0:num_cols - 1]
    # Access last column of new matrix and paste last column from transposed matrix
    new_matrix[:, -1] = matrix[:, -1]

    return new_matrix

# Finds pivot position in a given matrix and returns its position.
def find_pivot_position(matrix):
    # Look for the most negative value last column
    x_b = matrix[:, -1]
    most_negative_number_index = np.argmin(x_b)
    # Store pivot row for future calculations
    pivot_row = matrix[most_negative_number_index, :]

    # Access objective function (last row)
    c_row = matrix[-1, :]
    # Subtract Z row by objective function to prepare minimum ratio method
    z_minus_c = np.subtract(z_row, c_row)
    
    # Apply minimum ratio method rules. --> -1000000 will be inserted in case that a division is invalid but has to return a valid number.
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
        
    # Transform ratio list to a numpy array
    np.asarray(ratio)

    # Based on the given division rules we will only have numbers <= 0 in our ratio array. Now we want to find the maximum and note its index 
    max_negative_number_index = np.argmax(ratio)

    # Debug statement in case we want to check if our pivot element is correct
    pivot_element = matrix[most_negative_number_index, max_negative_number_index]

    return most_negative_number_index, max_negative_number_index

# Manipulate matrix based on linear transformation methods same as the Gaussian algorithm
def manipulate_matrix(matrix, pivot_position):
    # Calculate new pivot row
    pivot_row = matrix[pivot_position[0], :]
    pivot_row = np.true_divide(pivot_row, matrix[pivot_position], dtype=np.longdouble)
    matrix[pivot_position[0], :] = pivot_row
    # Update other rows except pivot row based on new pivot row
    for i in range(0, num_rows):
        if(i != pivot_position[0]):
            new_row = matrix[i, :]
            coefficient = np.multiply(new_row[pivot_position[1]], -1)
            new_row = np.add(new_row, np.multiply(pivot_row, coefficient))
            matrix[i, :] = new_row
    
    return matrix
    
# Check if all elements in last column are greater or equal to 0. In this case the optimal solution is given
def check_for_finish(matrix):
    return True if np.all(matrix[:, -1] >= 0) else False

# Print solutions for a given matrix
def print_solution(matrix):
    solutions = []
    # Used to read variable solutions
    matrix_without_slack_variables = matrix[:, 0:num_cols-1]
    last_column = matrix[:, -1]
    # Check which columns contain only zeros and ones. In this columns we have valid solutions for the given variable displayed in the last column.
    for i in range(0, matrix_without_slack_variables.shape[1]):
        current_column = matrix_without_slack_variables[:, i]
        if np.max(current_column) > 1 or np.min(current_column) < 0:
            continue
        elif 1 in current_column:
            index = np.argwhere(current_column == 1).item()
            solutions.append(f'x{i}: {last_column[index]}')
    # Return solutions to be printed by the main.py
    return matrix, iterations, matrix[-1, -1], solutions

# Start method to start the simplex algorithm
def start(parsed, mode):
    # Perform manipulation in case its a minimization problem
    init_matrix = init(np.asarray(parsed), mode)
    # Fill Matrix with slack variables
    new_matrix = add_slack_variables(init_matrix)
    # Initialize "z row" with zeros with the size of the matrix row size
    global z_row
    z_row = np.zeros(new_matrix.shape[1])
    global iterations
    iterations = 0
    finished = False
    while finished is False:
        pivot_position = find_pivot_position(new_matrix)
        new_matrix = manipulate_matrix(new_matrix, pivot_position)
        iterations += 1
        finished = check_for_finish(new_matrix)
    if finished:
        return print_solution(new_matrix)

