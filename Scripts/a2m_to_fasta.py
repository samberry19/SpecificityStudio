#!/usr/bin/env python3

import sys

def a2m_to_fasta(infile, outfile):
    with open(infile) as f, open(outfile, "w") as out:
        seq = ""
        header = None

        for line in f:
            line = line.strip()
            if not line:
                continue

            if line.startswith(">"):
                if header is not None:
                    out.write(seq.upper() + "\n")
                header = line
                out.write(header + "\n")
                seq = ""
            else:
                seq += line

        # write last sequence
        if header is not None:
            out.write(seq.upper() + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python a2m_to_fasta.py input.a2m output.fasta")
        sys.exit(1)

    a2m_to_fasta(sys.argv[1], sys.argv[2])
