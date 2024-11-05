from typing import TypeVar
import numpy as np
from dataclasses import dataclass
import awkward as ak
from .dogma_rust import permute_awkward

# Either numpy array or awkward array
_T = TypeVar("_T", np.ndarray, ak.Array)


@dataclass
class Split:
    train: _T
    val: _T
    test: _T

    def __iter__(self):
        return iter([self.train, self.val, self.test])


class Splitter:
    def __init__(
        self,
        *,
        train_prop: float,
        val_prop: float,
        test_prop: float | None = None,
        length: int,
    ):
        self.permutation = np.random.permutation(length)
        train_n_elements = int(train_prop * length)
        val_n_elements = int(val_prop * length)
        if test_prop is not None:
            assert test_prop + train_prop + val_prop == 1
        self.train_permutation = self.permutation[:train_n_elements]
        self.val_permutation = self.permutation[
            train_n_elements : train_n_elements + val_n_elements
        ]
        self.test_permutation = self.permutation[train_n_elements + val_n_elements :]

    def split_array(self, array: np.ndarray):
        return Split(
            array[self.train_permutation],
            array[self.val_permutation],
            array[self.test_permutation],
        )

    def split_awkward(self, array: ak.Array):
        return Split(
            permute_awkward(array, self.train_permutation),
            permute_awkward(array, self.val_permutation),
            permute_awkward(array, self.test_permutation),
        )

    def get_permutations(self):
        return Split(
            self.train_permutation, self.val_permutation, self.test_permutation
        )
