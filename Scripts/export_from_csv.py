#!/usr/bin/env python3

import argparse
import pandas as pd
import shlex


def main():
    parser = argparse.ArgumentParser(
        description="Extract a row from a CSV and output bash export statements"
    )
    parser.add_argument("csv_file", help="Path to CSV file")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--row-index", type=int, help="Row index (0-based)")
    group.add_argument("--filter", nargs=2, metavar=("COLUMN", "VALUE"),
                       help="Filter row by COLUMN == VALUE")

    parser.add_argument("--prefix", default="", help="Prefix for variable names")

    args = parser.parse_args()

    df = pd.read_csv(args.csv_file)

    # --- Select row ---
    if args.row_index is not None:
        row = df.iloc[args.row_index]

    else:
        col, val = args.filter

        # Important: CSV values are often strings unless parsed otherwise
        matches = df[df[col].astype(str) == val]

        if len(matches) == 0:
            raise ValueError(f"No rows found where {col} == {val}")
        if len(matches) > 1:
            raise ValueError(f"Multiple rows found where {col} == {val}")

        row = matches.iloc[0]

    # --- Output bash exports ---
    for col, val in row.items():
        env_name = f"{args.prefix}{col}".upper()

        # Safely quote values for bash
        safe_val = shlex.quote(str(val))

        print(f"export {env_name}={safe_val}")


if __name__ == "__main__":
    main()