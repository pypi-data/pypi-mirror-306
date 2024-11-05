from .utils import AA_VOCAB
from dogma_data import (
    parse_fasta,
    FastaMapping,
    HeaderType,
    export_hdf5,
    Splitter,
    find_boundaries_i64,
    permute_sequences,
)
import argparse
import numpy as np
import pandas as pd


def cli():
    parser = argparse.ArgumentParser(description="Dogma-data preprocessing script")

    parser.add_argument("input_filename")
    parser.add_argument("output_filename")
    parser.add_argument(
        "--header",
        type=str,
        default="Skip",
        help="Header parser type",
        dest="header",
        choices=["skip", "taxon", "subcluster"],
    )
    parser.add_argument(
        "--csv-file",
        type=str,
        default="",
        help="CSV file used for evoprompting",
        dest="csv_file",
    )
    parser.add_argument(
        "--train", type=float, default=0.975, help="Training set split", dest="train"
    )
    parser.add_argument(
        "--eval", type=float, default=0.025, help="Evaluation set split", dest="eval"
    )
    parser.add_argument(
        "--test", type=float, default=0.0, help="Testing set split", dest="test"
    )
    parser.add_argument(
        "--vocab",
        type=str,
        default="aa",
        help="Vocabulary for token parsing",
        dest="vocab",
        choices=["skip", "aa"],
    )

    args = parser.parse_args()

    header_type = HeaderType.Skip
    if args.header == "taxon":
        header_type = HeaderType.TaxonId
    elif args.header == "subcluster":
        header_type = HeaderType.SubCluster

    fm = None
    if args.vocab == "aa":
        fm = FastaMapping(AA_VOCAB.stoi, default_value=AA_VOCAB["<aaunk>"])

    tokens, tokens_cu_seqlens, header_arrays = parse_fasta(
        args.input_filename, header_type, fm
    )

    splitter_len = len(tokens_cu_seqlens) - 1
    header_info = dict()
    if args.header == "taxon":
        header_info["taxon_ids"] = header_arrays[0]
    elif args.header == "subcluster":
        supercluster_ids = header_arrays[1]
        by_supercluster_ids = np.argsort(supercluster_ids)
        idx_for_supercluster_id = np.stack(
            (supercluster_ids, np.arange(len(supercluster_ids), dtype=np.int64)),
            axis=0,
        )[:, by_supercluster_ids]

        supercluster_boundaries = find_boundaries_i64(
            np.ascontiguousarray(idx_for_supercluster_id[0])
        ).astype(np.uint64)
        supercluster_ids_unique = idx_for_supercluster_id[0][
            supercluster_boundaries[:-1]
        ]

        new_tokens, new_tokens_cu_seqlens = permute_sequences(
            tokens, tokens_cu_seqlens, by_supercluster_ids
        )

        old_seqlens = tokens_cu_seqlens[1:] - tokens_cu_seqlens[:-1]
        new_seqlens = new_tokens_cu_seqlens[1:] - new_tokens_cu_seqlens[:-1]

        assert (
            tokens_cu_seqlens[-1] == new_tokens_cu_seqlens[-1]
        ), f"Permuted seqlens must match! {tokens_cu_seqlens[-1]} != {new_tokens_cu_seqlens[-1]}"

        assert np.all(
            new_seqlens >= 0
        ), "Token cummulative sequence lengths must be monotonically increasing!"

        assert (
            len(supercluster_ids_unique) == len(supercluster_boundaries) - 1
        ), "Number of clusters and cluster boundaries must match!"

        test_len = min(1000, len(supercluster_ids))
        for i in range(test_len):
            old_range = (
                tokens_cu_seqlens[by_supercluster_ids[i]],
                tokens_cu_seqlens[by_supercluster_ids[i] + 1],
            )
            new_range = (new_tokens_cu_seqlens[i], new_tokens_cu_seqlens[i + 1])
            assert (new_range[1] - new_range[0]) == (
                old_range[1] - old_range[0]
            ), "Ranges must match!"
            assert np.array_equal(
                tokens[old_range[0] : old_range[1]],
                new_tokens[new_range[0] : new_range[1]],
            ), "Token permutation does not match!"

        tokens = new_tokens
        tokens_cu_seqlens = new_tokens_cu_seqlens

        if args.csv_file != "":
            pair_csv = pd.read_csv(args.csv_file, header=None)
            pair_array = (
                pair_csv.to_numpy().flatten()
            )  # [set1_idx1, set1_idx2, set2_idx1, set2_idx2, ...]
            seq_set_boundaries = np.arange(0, len(pair_array) + 1, 2)

            inverse_seq_id_mapping = np.full(
                pair_array.max() + 1, fill_value=-1, dtype=np.int64
            )
            inverse_seq_id_mapping[header_arrays[0]] = np.arange(len(header_arrays[0]))
            pair_array = inverse_seq_id_mapping[pair_array]

            # Compute the total lengths of the sequences in each set
            print(f"{pair_array=}, {seq_set_boundaries=}, {len(tokens_cu_seqlens)=}")
            seq_set_lengths = (
                tokens_cu_seqlens[pair_array[0::2] + 1]
                - tokens_cu_seqlens[
                    pair_array[0::2]
                ]  # Length of first sequence of the set
                + tokens_cu_seqlens[pair_array[1::2] + 1]
                - tokens_cu_seqlens[
                    pair_array[1::2]
                ]  # Length of the second sequence of the set
            )

            assert len(seq_set_lengths) == len(seq_set_boundaries) - 1

            splitter_len = len(seq_set_lengths)
            header_info["seq_set_idcs"] = pair_array
            header_info["seq_set_boundaries"] = seq_set_boundaries
            header_info["seq_set_lengths"] = seq_set_lengths
        else:
            splitter_len = len(supercluster_ids_unique)

        header_info["taxon_ids"] = header_arrays[0]
        header_info["supercluster_ids_unique"] = supercluster_ids_unique
        header_info["supercluster_boundaries"] = supercluster_boundaries

        assert len(header_info["supercluster_ids_unique"]) == len(
            set(header_info["supercluster_ids_unique"])
        ), "Cluster ids array must contain unique ids!"

    train_val = args.train
    eval_val = args.eval
    test_val = args.test

    norm_fac = train_val + eval_val + test_val

    train_val /= norm_fac
    eval_val /= norm_fac
    test_val /= norm_fac

    export_hdf5(
        args.output_filename,
        Splitter(
            train_prop=train_val,
            val_prop=eval_val,
            test_prop=test_val,
            length=splitter_len,
        ),
        tokens,
        tokens_cu_seqlens,
        header_info,
        fm,
    )


if __name__ == "__main__":
    cli()
