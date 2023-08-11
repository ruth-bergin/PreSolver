# SAT Pre-Solver - Warm Initialisation for SLS Solvers

## Usage
To generate predictions for an instance set, run `PreSolver/src/generate_predictions.py`.
| Argument                     | Flag     | Currently accepted values                               |
|------------------------------|----------|---------------------------------------------------------|
| dataset                      | -d       | basename of any folder with CNFs in PreSolver/instances |
| classifier                   | -c       | RfcBase \| RfcDpll                                      |
| variable selection heuristic | -v       | dlis \| relative_appearances \| weighted_purity         |

Output can be found in the folder `PreSolver/instances/{dataset}/{classifier}_predictions/`

## Evaluation
To execute a solver on an instance set:  
`execute_solver_on_instance_set.sh <dataset_name> [initialisation] [randomisationProb]`.
| Argument                     | Default  | Currently accepted values                               |
|------------------------------|----------|---------------------------------------------------------|
| dataset                      | N/A      | basename of any folder with CNFs in PreSolver/instances |
| initialisation               | control  | control \| any accepted classifier                      |
| variable selection heuristic | 25       | 0 - 100                                                 |

* Predictions must be generated before this script can be executed - takes input from the above output.  
* Currently only probSAT is configured for evaluation.  
* Ensure every solver is compiled before execution.

Output can be found in `results/{dataset}_{classifier}_{randomisationProb}.txt`
