import numpy as np
from numpy.typing import DTypeLike, NDArray
from .dogma_rust import concatenate_numpy as concatenate_arrays
from contextlib import contextmanager
from time import time
from collections import OrderedDict
from dataclasses import dataclass
from enum import IntEnum, auto
from typing import Dict, List, Optional, TypeVar


_T = TypeVar("_T", bound=np.generic, covariant=True)


def concatenate_numpy(
    arrays: list[NDArray[_T]],
) -> tuple[NDArray[_T], NDArray[np.int64]]:
    arr, cu = concatenate_arrays(arrays)
    dtype: DTypeLike = arrays[0].dtype
    arr = arr.view(dtype)
    cu //= dtype.itemsize
    return arr, cu


@contextmanager
def timer(name):
    print(f"{name}...")
    start = time()
    yield
    print(f"{name} took {time() - start} seconds")


class TokenType(IntEnum):
    AMINO_ACID = auto()
    NUCLEOTIDE = auto()
    SPECIAL = auto()
    MASKING = auto()
    OTHER = auto()


@dataclass(frozen=True)
class Token:
    value: str
    token_type: TokenType


class Vocabulary:
    """Class to manage a vocabulary, mapping tokens to indices and vice versa."""

    def __init__(
        self, tokens: List[Token], specials: Optional[List[Token]] = None
    ) -> None:
        self.stoi: Dict[str, int] = OrderedDict()
        self.itos: List[str] = []
        self.default_index: Optional[int] = None

        for token in (specials or []) + tokens:
            self.add_token(token)

    def add_token(self, token: Token) -> None:
        if token.value not in self.stoi:
            self.stoi[token.value] = len(self.itos)
            self.itos.append(token.value)

    def __getitem__(self, token_value: str) -> int:
        return self.stoi.get(token_value, self.default_index)

    def get_itos(self) -> List[str]:
        return self.itos

    def set_default_index(self, index: int) -> None:
        self.default_index = index


# Define tokens
tokens = [
    Token("a", TokenType.NUCLEOTIDE),
    Token("g", TokenType.NUCLEOTIDE),
    Token("c", TokenType.NUCLEOTIDE),
    Token("t", TokenType.NUCLEOTIDE),
    # Amino acids
    Token("A", TokenType.AMINO_ACID),
    Token("C", TokenType.AMINO_ACID),
    Token("D", TokenType.AMINO_ACID),
    Token("E", TokenType.AMINO_ACID),
    Token("F", TokenType.AMINO_ACID),
    Token("G", TokenType.AMINO_ACID),
    Token("H", TokenType.AMINO_ACID),
    Token("I", TokenType.AMINO_ACID),
    Token("K", TokenType.AMINO_ACID),
    Token("L", TokenType.AMINO_ACID),
    Token("M", TokenType.AMINO_ACID),
    Token("N", TokenType.AMINO_ACID),
    Token("P", TokenType.AMINO_ACID),
    Token("Q", TokenType.AMINO_ACID),
    Token("R", TokenType.AMINO_ACID),
    Token("S", TokenType.AMINO_ACID),
    Token("T", TokenType.AMINO_ACID),
    Token("V", TokenType.AMINO_ACID),
    Token("W", TokenType.AMINO_ACID),
    Token("Y", TokenType.AMINO_ACID),
    Token("<stop>", TokenType.AMINO_ACID),  # Both selenocysteine and pyrrolysine
    Token("<aaunk>", TokenType.AMINO_ACID),
    Token("<rna_mask>", TokenType.MASKING),
    Token("<aa_mask>", TokenType.MASKING),
    # Indicators of the type of masking used in the sequence
    Token("<seq_triple_masked>", TokenType.MASKING),
    Token("<seq_third_masked>", TokenType.MASKING),
    Token("<seq_rna_masked>", TokenType.MASKING),
    Token("<seq_protein_masked>", TokenType.MASKING),
    Token("O", TokenType.AMINO_ACID),
    Token("Z", TokenType.AMINO_ACID),
    Token("B", TokenType.AMINO_ACID),
    Token("U", TokenType.AMINO_ACID),
    Token("X", TokenType.AMINO_ACID),
    Token(".", TokenType.OTHER),
    Token("-", TokenType.OTHER),
]

specials = [
    Token("<pad>", TokenType.SPECIAL),
    Token("<sos>", TokenType.SPECIAL),
    Token("<eos>", TokenType.SPECIAL),
    Token("<unk>", TokenType.SPECIAL),
]

AA_VOCAB = Vocabulary(tokens, specials)

PAD_TOK = AA_VOCAB["<pad>"]
SOS_TOK = AA_VOCAB["<sos>"]
EOS_TOK = AA_VOCAB["<eos>"]
UNK_TOK = AA_VOCAB["<unk>"]
DOT_TOK = AA_VOCAB["."]
HYPHEN_TOK = AA_VOCAB["-"]
AA_MASK_TOK = AA_VOCAB["<aa_mask>"]
RNA_MASK_TOK = AA_VOCAB["<rna_mask>"]
AAUNK_TOK = AA_VOCAB["<aaunk>"]
AASTOP_TOK = AA_VOCAB["<stop>"]

AMINO_ACID_TOK_SET = np.array(
    [AA_VOCAB[t.value] for t in tokens if t.token_type == TokenType.AMINO_ACID]
)
NUCELOTIDE_TOK_SET = np.array(
    [AA_VOCAB[t.value] for t in tokens if t.token_type == TokenType.NUCLEOTIDE]
)

AA_VOCAB.set_default_index(AA_VOCAB["<aaunk>"])
