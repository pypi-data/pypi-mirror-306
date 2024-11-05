import numpy as np
from numpy.typing import NDArray
from enum import Enum
import awkward as ak

class FastaMapping:
    """
    Holds character level mappings from FASTA characters to integer values.
    Passed to parsing methods for FASTAs.
    """
    def __init__(self, mapping: dict[str, int], default_value: int): ...
    def __str__(self) -> str: ...
    def __repr__(self) -> str: ...

class HeaderType(Enum):
    Skip = ...
    TaxonId = ...
    SubCluster = ...

def parse_fasta(
    path: str, header_type: HeaderType, mapping: FastaMapping | None
) -> tuple[NDArray[np.uint8], NDArray[np.int64], tuple[NDArray, ...]]:
    """
    Parses input fasta file, specified with **path** according to the **mapping**. Function executes on parallel threads.
    Header type to be parsed is specified with the **header_type** argument.

    Function returns a tuple of data, sequence descriptors and any header information.
    """
    ...

def concatenate_numpy(
    arrays: list[NDArray],
) -> tuple[NDArray[np.uint8], NDArray[np.int64]]:
    """
    Concatenates a given list of numpy arrays into a data and sequence descriptor arrays. Function executes on parallel threads.
    """
    ...

def concatenate_awkward(
    awkwards: list[tuple[NDArray, NDArray[np.int64]]],
) -> tuple[NDArray[np.uint8], NDArray[np.int64]]:
    """
    Concatenates a given list of awkward arrays into a single awkward array. Function executes on parallel threads.
    """
    ...

def awkward_from_list_of_numpy(
    arrays: list[NDArray],
) -> tuple[NDArray[np.uint8], NDArray[np.int64]]:
    """
    Constructs awkward arrays form a list of numpy arrays. Function executes on parallel threads.
    """
    ...

def find_boundaries_u32(arr: NDArray[np.uint32]) -> NDArray[np.int64]:
    """
    Looks for boundaries in the given array and returns them in a numpy array.
    """
    ...

def find_chunk_boundaries(
    sequence_lengths: NDArray[np.int64], chunk_tokens: int
) -> NDArray[np.int64]:
    """
    Looks for boundaries in the given array that are shorter than **chunk_tokens** and returns them in a numpy array.
    """
    ...

def permute_awkward(arr: ak.Array, permutation: np.ndarray) -> ak.Array:
    """
    Index the array with the indices given by `permutation`, and pack the resulting Awkward array into contiguous buffers.
    """
    ...

def permute_sequences(
    content: NDArray[np.uint8], cu_seqlens: NDArray[np.int64], permutation: np.ndarray
) -> tuple[NDArray[np.uint8], NDArray[np.int64]]:
    """
    Looks for boundaries in the given array that are shorter than **chunk_tokens** and returns them in a numpy array.
    """
    ...
