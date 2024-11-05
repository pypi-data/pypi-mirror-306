import numpy as np
import hdf5plugin
from h5py import File as H5File
from .utils import timer
from ._split import Splitter
from numpy.typing import NDArray
from dogma_data import FastaMapping


def export_hdf5(
    output_path: str,
    train_splitter: Splitter,
    tokens: NDArray[np.uint8],
    tokens_cu_seqlens: NDArray[np.int64],
    header_info: dict[str, NDArray],
    mapping: FastaMapping | None,
) -> None:
    train, val, test = train_splitter.get_permutations()

    with H5File(output_path, "w") as f:
        compressor = hdf5plugin.Blosc2(cname="zstd", clevel=3)

        assert (
            len(tokens) == 0 or tokens.max() <= np.iinfo(np.uint8).max
        ), "Data overflow in tokens"
        assert (
            len(tokens_cu_seqlens) == 0
            or tokens_cu_seqlens.max() <= np.iinfo(np.uint64).max
        ), "Data overflow in tokens_cu_seqlens"

        with timer("Writing tokens..."):
            f.create_dataset("tokens", data=tokens, dtype=np.uint8, **compressor)

        with timer("Writing seqlens..."):
            f.create_dataset(
                "tokens_cu_seqlens",
                data=tokens_cu_seqlens,
                dtype=np.int64,
                **compressor,
            )

        with timer("Writing header data..."):
            for header_name, header_values in header_info.items():
                f.create_dataset(
                    header_name,
                    data=header_values,
                    dtype=header_values.dtype,
                    **compressor,
                )

        with timer("Writing training splits..."):
            f.create_dataset("train_split", data=train, dtype=np.int64, **compressor)
            f.create_dataset("val_split", data=val, dtype=np.int64, **compressor)
            f.create_dataset("test_split", data=test, dtype=np.int64, **compressor)

        if mapping is not None:
            f.attrs["mapping"] = str(mapping)
