from pysat.solvers import Solver
import math
import numpy

k=int(input("Enter Value of K "))

with open("test_case_5.txt") as fname:
    #replace 'sample_data/test_case.txt' with the location of the--
    #-- text file containing test_cases in your device/environment
    a = numpy.loadtxt(fname, dtype = 'float', delimiter=",")

#------------------------------------------------------------------------------#
# Taking input of sudoku cell values from the .txt file
n = k*k

sudoku_1=[]
for i in range(n):
    row = []
    for j in range(n):
        row.append(a[n*i + j])
    sudoku_1.append(row)

cells = n*n

sudoku_2=[]
for i in range(n):
    row = []
    for j in range(n):
        row.append(a[n*i + j + cells])
    sudoku_2.append(row)

sud_pair=[]
sud_pair.append(sudoku_1)
sud_pair.append(sudoku_2)
#------------------------------------------------------------------------------#

def print_solved_spair(sudoku_pair_solver, n, Initial_Clauses):
    solution_possible = False
    for p in sudoku_pair_solver.enum_models(assumptions = Initial_Clauses):
        solution_possible = True
        for s_no in range(2):
            print(f"Solved Sudoku No. {s_no + 1} :\n")
            for x in range(n):
                  row = []
                  for y in range(n):
                      for val in range(n):
                          cl_val=int(s_no*n*n*n + n*n*x + n*y + val)
                          if p[cl_val]>0:
                              print(val+1, end="    ")
                              row.append(val+1)
                  print("\n")
            print("__________________________________________\n")

    if not solution_possible:
        print("None")

# Below: 'x','y','z' refers to row, column, assigned number respectively.

# Storing Presumed clauses in one list
#------------------------------------------------------------------------------#
Initial_Clauses = []
for s_no in range(2):
    for x in range(n):
        for y in range(n):
            for z in range(n):
                if sud_pair[s_no][x][y]:
                    if(sud_pair[s_no][x][y] != z+1):
                        Initial_Clauses.append(int((-1)*(s_no*n*n*n + n*n*x + n*y + z+1)))
                    else:
                        Initial_Clauses.append(int(s_no*n*n*n + n*n*x + n*y + z+1))
#------------------------------------------------------------------------------#

# Initializing the SAT solver
sudoku_pair_solver = Solver()

# 1: Each cell should have atleast one number
#------------------------------------------------------------------------------#
#Sudoku 1
for x in range(n):
    for y in range(n):
        clause = []
        for z in range(n):
            clause.append(int(n*n*x + n*y + z+1))
        sudoku_pair_solver.add_clause(clause)

#Sudoku 2
for x in range(n):
    for y in range(n):
        clause = []
        for z in range(n):
            clause.append(int(n*n*n + n*n*x + n*y + z+1))
        sudoku_pair_solver.add_clause(clause)
#------------------------------------------------------------------------------#

# 2: Each number appears at most once in each kxk sub-grid:
#------------------------------------------------------------------------------#
for s_no in range(2):
    for x in range(k):
        for y in range(k):
            for z in range(n):
                clause = []
                # i, j are used to keep track of sub-grids
                for i in range(k*x, k*(x+1)):
                    for j in range(k*y, k*(y+1)):
                      clause.append(int(s_no*n*n*n + n*n*i + n*j + z+1))
                sudoku_pair_solver.add_clause(clause)
#------------------------------------------------------------------------------#

# 3: Each number appears at most once in each row
#------------------------------------------------------------------------------#
for s_no in range(2):
    for y in range(n):
        for z in range(n):
            for x1 in range(n):
                for x2 in range(x1 + 1, n):
                    clause = []
                    clause.append(int((-1)*(s_no*n*n*n + n*n*x1 + n*y + z+1)))
                    clause.append(int((-1)*(s_no*n*n*n + n*n*x2 + n*y + z+1)))
                    sudoku_pair_solver.add_clause(clause)
#------------------------------------------------------------------------------#

# 4: Each number appears at most once in each column
#------------------------------------------------------------------------------#
for s_no in range(2):
    for x in range(n):
        for z in range(n):
            for y1 in range(n):
                for y2 in range(y1 + 1, n):
                    clause = []
                    clause.append(int((-1)*(s_no*n*n*n + n*n*x + n*y1 + z+1)))
                    clause.append(int((-1)*(s_no*n*n*n + n*n*x + n*y2+ z+1)))
                    sudoku_pair_solver.add_clause(clause)
#------------------------------------------------------------------------------#

# 5: Corresponding cells in both sudokus have different numbers
#------------------------------------------------------------------------------#
for x in range(n):
    for y in range(n):
        for z in range(n):
            clause=[]
            clause.append(int((-1)*(n*n*x + n*y + z+1)))
            clause.append(int((-1)*(n*n*n + n*n*x + n*y + z+1)))
            sudoku_pair_solver.add_clause(clause)
#------------------------------------------------------------------------------#

print_solved_spair(sudoku_pair_solver, n, Initial_Clauses)
