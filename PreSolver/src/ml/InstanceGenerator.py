from cnfgen import RandomKCNF, PigeonholePrinciple, CountingPrinciple, CliqueColoring
from pysat import solvers
from src.SATInstance.CNF import CNF

def generateInstances(max_variables, max_clauses, max_k, model_count):
    F = CliqueColoring(8,14,12)
    print(F.to_dimacs())
    print(CNF(F.to_dimacs()).solve())

generateInstances(2,3,4,5)