# simplex-solver

Simplex Solver written in Python using the Dual Simplex Method

# Installation

Download the binary for your operating system (currently available: Windows and Mac OS)
Extract the zip folder and either double click the .EXE file on Windows or run the `./simplex` file from the Terminal

You could also download the src folder and run python main.py (only working on Python >= 3.10 since I have to rename the parser module). <br>
Ideally you want to install the src to a virtual environment. I recommend virtualenv.

## Installing Virtualenv (ONLY REQUIRED IF BINARY IS NOT WORKING)

1. `pip install virtualenv` <br>
2. If there is no venv folder create one: `mkdir venv` <br>
3. run: `virtualenv venv`

## Activating Virtualenv

### On Windows

run: `.\venv\Scripts\activate`

### On MacOS/Linux

run: `source ./venv/bin/activate`

## Installing Numpy (ONLY REQUIRED WHEN USING A FRESH VIRTUALENV)

run `pip install numpy` in your virtualenv terminal if you installed a fresh virtualenv. Again, this is only necessary if the binaries are not working.

# Usage

Please read the shell instructions carefully. You will be prompted to give user input, please only use "y" or "n" as answers (without quotation marks). <br>
First it will recognize that there is no benchmark folder, which it needs to operate. It will automatically create one and it will ask you to drop your benchmarks/tasks in there. The application will terminate for now. <br>
Please only drop benchmarks which are solveable by the [lp_solve](http://web.mit.edu/lpsolve/doc/) application. If you do not have any benchmarks you can use, there are seven inside the benchmark folder inside this repository. [benchmarks](https://github.com/fjure/simplex-solver/tree/main/benchmarks) <br>
After you dropped your benchmarks into the folder, rerun the application. It will try to parse your files and will ask you, if you want to save the solutions to seperate files or if it should print out the solutions. Please again answer with "y" or "n". <br>
If you decide to save the solutions in files, it will generate a solutions folder in the same project folder with the solution files in it.

# TODO

- Maximization problems <br>
  Right now the application only supports minimization problems, since those were the only given benchmarks. <br>
- Adding more flags to the user shell <br>
  The user shell has to be more interactive. Right now it only offers the possibility to save the solutions. Flags like "interval", "create-demo-benchmarks" or "debug" will be added soon.
