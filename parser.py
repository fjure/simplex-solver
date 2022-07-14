import sys

import numpy as np

benchmark_dir = "./benchmarks"

def try_to_parse(filename):
    
    print(f'Parser: Parsing {filename}')

    file = open(f'{benchmark_dir}/{filename}', "r")
    lines = file.readlines()

    objective_function = ""
    functions_string = []
    mode = "null"

    for line in lines:
        if line.startswith("//"):
            continue
        elif line.startswith(" +") or line.startswith(" -"):
            functions_string.append(line)
        elif line.startswith("min"):
            mode = "min"
            objective_function = line.strip("min")
        elif line.startswith("max"):
            mode = "max"
            objective_function = line.strip("max")

    functions_string.append(objective_function)

    if(mode == "null" or len(functions_string) == 0):
        print(f'Parser: Something went wrong with {filename}.. Check your files.')
        sys.exit()
    
    functions = []
    for function in functions_string:
        # remove leading whitespace
        function = function.strip()
        coefficients = []
        factors = function.split(" ")
        for i in range(len(factors)):
            if factors[i] == "+":
                coefficients.append(int(factors[i+1].split("*")[0]))
            elif factors[i] == "-":
                coefficients.append(-int(factors[i+1].split("*")[0]))
            elif factors[i] == ">=" or factors[i] == "<=":
                coefficients.append(int(factors[i+1].strip(";")))
        functions.append(coefficients)

    functions[-1].append(0)
    file.close()
    return np.array(functions), mode