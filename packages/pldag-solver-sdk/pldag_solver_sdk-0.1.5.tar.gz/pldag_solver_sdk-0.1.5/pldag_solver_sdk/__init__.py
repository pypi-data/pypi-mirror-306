import requests
import numpy as np

from dataclasses import dataclass
from pldag import PLDAG
from typing import Dict, List, Optional
from enum import Enum
from hashlib import md5
from pickle import dumps, loads

class ConnectionError(Exception):
    pass

class SolverType(str, Enum):
    DEFAULT = "default"

@dataclass
class SolutionResponse:

    solution:   Optional[Dict[str, int]]    = None
    error:      Optional[str]               = None

@dataclass
class ICache:

    def set(self, key: str, value: bytes):
        pass

    def get(self, key: str):
        pass

@dataclass
class Solver:
    
    url: str

    # Optional cache
    cache_builder:  Optional[ICache] = None
    cache_server:   Optional[ICache] = None

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
        
    def prepare_model(self, model: PLDAG, assume: dict) -> tuple:
        """Prepare the model to be sent to the server"""

        def model_polyhedron(model: PLDAG, assume: dict) -> tuple:
            A, b = model.to_polyhedron(**assume)
            A_rows, A_cols, A_vals = self._sparse_polyhedron(A)
            return (A, b, A_rows, A_cols, A_vals)

        if self.cache_builder is not None:
            key = md5(dumps((model.sha1(), assume))).hexdigest()
            cached = self.cache_builder.get(key)
            if cached is not None:
                return loads(cached)
            
            data = model_polyhedron(model, assume)
            self.cache_builder.set(key, dumps(data))
            return data
        
        else:
            return model_polyhedron(model, assume)

    def solve(
        self, 
        model: PLDAG, 
        objectives: List[Dict[str, int]], 
        assume: Dict[str, complex] = {}, 
        solver: SolverType = SolverType.DEFAULT,
        maximize: bool = True,
    ) -> List[SolutionResponse]:
        
        if self.cache_server is not None:
            key = md5(dumps((model.sha1(), objectives, assume, solver, maximize))).hexdigest()
            cached = self.cache_server.get(key)
            if cached is not None:
                return loads(cached)

        A_dense, b_dense, A_sparse_rows, A_sparse_cols, A_sparse_vals = self.prepare_model(model, assume)
        response = requests.post(
            f"{self.url}/model/solve-one/linear",
            json={
                "model": {
                    "polyhedron": {
                        "A": {
                            "rows": A_sparse_rows,
                            "cols": A_sparse_cols,
                            "vals": A_sparse_vals,
                            "shape": {"nrows": A_dense.shape[0], "ncols": A_dense.shape[1]}
                        },
                        "b": b_dense.tolist()
                    },
                    "columns": model.columns.tolist(),
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
        
        result = list(
            map(
                lambda x: SolutionResponse(**x),
                response.json().get("solutions", [])
            )
        )

        if self.cache_server is not None:
            self.cache_server.set(key, dumps(result))

        return result
