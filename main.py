import os
import sys
import shutil
import time

from parser import try_to_parse
from simplex import start

def main():
    print("This is a program to solve linear optimization problems using the simplex algorithm.")
    print("Currently it only supports minimization problems.")
    print("This shell will help you using the application.")
    print("Please only answer with y or n as user input.")
    print("Lets start with test cases.")

    folder_exist = os.path.isdir("./benchmarks")
    if folder_exist is False:
        print("I detected that you do not have a folder with cases in it. ")
        user_input = input("Do you want me to create a folder?")
        if user_input == "y":
            os.mkdir("./benchmarks")
            print("The application will close now. Please insert cases that fulfill the lp_solve syntax.")
            sys.exit()
        if user_input == "n":
            print("Please create a folder called benchmarks and fill it with cases that fulfill the lp_solve syntax.")
            sys.exit()
        
    print("I detected a folder called benchmarks in this directory.")
    print("I will try to parse those files and use them to parse the contents...")
    save_user_input = input("Do you want to save the solutions to a according text file?")
    save_mode = False
    if save_user_input == "y":
        save_mode = True
        print("Check the benchmarks folder after the application is done.")

    original_stdout = sys.stdout

    if(save_mode):
        if os.path.isdir("./solutions"):
            shutil.rmtree("./solutions")
            print("Cleaning the solutions folder..")
            os.mkdir("./solutions")
        else:
            os.mkdir("./solutions")
        
    
    files = os.listdir("./benchmarks")
    if(".DS_Store" in files):
        files.remove(".DS_Store")
    print(files)
    for file in files:
        parsed_benchmark = try_to_parse(file)
        case = parsed_benchmark[0]
        mode = parsed_benchmark[1]
        solutions = start(case, mode)

        solution_file = open(f'./solutions/solution_{file}', "w")
        sys.stdout = solution_file

        print(f'{solutions[0]}')
        print(f'Iterationen benötigt: {solutions[1]}')
        print(f'Zielfunktionswert: {solutions[2]}')
        print(f'Variablen:')
        for variable in solutions[3]:
            print(variable)

        time.sleep(0.5)

        sys.stdout = original_stdout    


main()