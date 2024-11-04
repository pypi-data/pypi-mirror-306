import requests
import numpy as np

from dataclasses import dataclass
from pldag import PLDAG
from typing import Dict, List, Optional
from enum import Enum

class ConnectionError(Exception):
    pass

class SolverType(str, Enum):
    DEFAULT = "default"

@dataclass
class SolutionResponse:

    solution:   Optional[Dict[str, int]]    = None
    error:      Optional[str]               = None

@dataclass
class Solver:
    
    url: str

    def __post_init__(self):
        # Test by sending a health get request to the server
        if not self.health():
            raise ConnectionError(f"Healthcheck to {self.url} failed")

    def _sparse_polyhedron(self, matrix: np.ndarray) -> tuple:
        rows, cols = np.nonzero(matrix)
        vals = matrix[rows, cols]
        return rows.tolist(), cols.tolist(), vals.tolist()
    
    def health(self) -> bool:
        try:
            response = requests.get(f"{self.url}/health")
            return response.status_code == 200
        except:
            return False

    def solve(
        self, 
        model: PLDAG, 
        objectives: List[Dict[str, int]], 
        assume: Dict[str, complex] = {}, 
        solver: SolverType = SolverType.DEFAULT,
        maximize: bool = True,
    ) -> List[SolutionResponse]:
        A, b = model.to_polyhedron(**assume)
        A_rows, A_cols, A_vals = self._sparse_polyhedron(A)
        response = requests.post(
            f"{self.url}/model/solve-one/linear",
            json={
                "model": {
                    "polyhedron": {
                        "A": {
                            "rows": A_rows,
                            "cols": A_cols,
                            "vals": A_vals,
                            "shape": {"nrows": A.shape[0], "ncols": A.shape[1]}
                        },
                        "b": b.tolist()
                    },
                    "columns": model.columns.tolist(),
                    "rows": [],
                    "intvars": model.integer_primitives.tolist()
                },
                "direction": "maximize" if maximize else "minimize",
                "objectives": objectives,
                "solver": solver.value
            }
        )
        if response.status_code != 200:
            data = response.json().get('error', {})
            if data.get('code') == 400:
                raise ValueError(data.get('message', 'Unknown input error'))
            else:
                raise Exception(data.get('message', 'Unknown error'))
        
        return list(
            map(
                lambda x: SolutionResponse(**x),
                response.json().get("solutions", [])
            )
        )
    
    def solve_polyhedron(
        self, 
        A: np.ndarray, 
        b: np.ndarray, 
        objectives: List[Dict[str, int]], 
        solver: SolverType = SolverType.DEFAULT, 
        maximize: bool = True,
    ) -> List[SolutionResponse]:
        A_rows, A_cols, A_vals = self._sparse_polyhedron(A)
        response = requests.post(
            f"{self.url}/model/solve-one/linear",
            json={
                "model": {
                    "polyhedron": {
                        "A": {
                            "rows": A_rows,
                            "cols": A_cols,
                            "vals": A_vals,
                            "shape": {"nrows": A.shape[0], "ncols": A.shape[1]}
                        },
                        "b": b.tolist()
                    },
                    "columns": [],
                    "rows": [],
                    "intvars": []
                },
                "direction": "maximize" if maximize else "minimize",
                "objectives": objectives,
                "solver": solver.value
            }
        )
        if response.status_code != 200:
            data = response.json().get('error', {})
            if data.get('code') == 400:
                raise ValueError(data.get('message', 'Unknown input error'))
            else:
                raise Exception(data.get('message', 'Unknown error'))
        
        return list(
            map(
                lambda x: SolutionResponse(**x),
                response.json().get("solutions", [])
            )
        )