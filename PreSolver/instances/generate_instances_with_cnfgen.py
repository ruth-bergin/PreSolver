import cnfgen
import networkx
import os
import numpy as np

for filename in os.listdir("cnfgen"):
    if os.path.isfile(f"cnfgen/{filename}"):
        os.remove(f"cnfgen/{filename}")
for i in range(250,500,10):
    for k in range(3,10):
        j = 0
        fails = 0
        while j < 5 and not (fails==100 and j<1):
            g = networkx.gnm_random_graph(i, i*(k**2))
            while max([d for n,d in g.degree()])>k and fails<100:
                print("Guaranteed unsat")
                g = networkx.gnm_random_graph(i, np.sqrt(i)*k)
                fails += 1
            if max([d for n,d in g.degree()])>k:
                continue
            cnf = cnfgen.GraphColoringFormula(g, k)
            if cnf.is_satisfiable():
                j += 1
                file = open(f"cnfgen/kcoloring_{i*k}_{k}_{j}.cnf", "w")
                file.write(cnf.to_dimacs())
                file.close()
            else:
                fails += 1
        print(f"n:\t{i*5}\nk:\t{k}")
        print(f"j:\t{j}\nfails:\t{fails}")
