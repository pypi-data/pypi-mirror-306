import warnings
from pathlib import Path
from typing import Iterable, List, Optional, Tuple, Union

import joblib
import numpy as np
import pynndescent
import scipy.sparse as spr


class Index:
    def __init__(
        self,
        options: np.ndarray,
        vectors: Union[np.ndarray, spr.sparray, spr.spmatrix],
        nearest_neighbours_kwargs: dict,
    ):
        self.options = options
        self.vectors = vectors
        self.nearest_neighbours_kwargs = nearest_neighbours_kwargs
        self.nearest_neighbours = pynndescent.NNDescent(
            vectors, **self.nearest_neighbours_kwargs
        )
        self.nearest_neighbours.prepare()

    def query(
        self,
        vectors: np.ndarray,
        limit: int = 10,
    ) -> Tuple[np.ndarray, np.ndarray]:
        indices, distances = self.nearest_neighbours.query(vectors, k=limit)
        return indices, distances


class IndexArray:
    def __init__(self, nearest_neighbours_kwargs: dict):
        self.nearest_neighbours_kwargs = nearest_neighbours_kwargs
        self.children = []
        self.options = np.array([])
        self.vectors = np.array([])
        self.option_offsets = []

    def add_index(self, options: np.ndarray, vectors: np.ndarray):
        self.children.append(
            Index(options, vectors, self.nearest_neighbours_kwargs)
        )
        option_set = set(self.options)
        is_in_options = [option in option_set for option in options]
        options = options[~is_in_options]
        vectors = vectors[~is_in_options]
        self.options = np.concatenate([self.options, options])
        self.vectors = np.concatenate([self.vectors, options])
        self.options_offsets.append(len(options))
        return self

    def query(
        self,
        vectors: Union[np.ndarray, spr.sparray, spr.spmatrix],
        limit: int = 10,
    ) -> Tuple[np.ndarray, np.ndarray]:
        indices = []
        distances = []
        for i_index, index in enumerate(self.children):
            offset = 0 if i_index == 0 else self.option_offsets[i_index - 1]
            sub_indices, sub_distances = index.query(vectors, limit)
            indices.append(sub_indices + offset)
            distances.append(sub_distances)
        indices = np.concatenate(indices, axis=-1)
        distances = np.concatenate(distances, axis=-1)
        sorting = np.argsort(distances, axis=-1)
        return indices[:, sorting], distances[:, sorting]
