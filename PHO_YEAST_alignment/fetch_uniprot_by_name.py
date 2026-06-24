#!/usr/bin/env python3
import sys
from textwrap import wrap

def iter_fasta(handle):
    """
    Simple FASTA parser: yields (header, sequence) pairs.
    header includes the leading '>'.
    """
    header = None
    seq_chunks = []
    for line in handle:
        line = line.rstrip("\n")
        if not line:
            continue
        if line.startswith(">"):
            if header is not None:
                yield header, "".join(seq_chunks)
            header = line
            seq_chunks = []
        else:
            seq_chunks.append(line.strip())
    if header is not None:
        yield header, "".join(seq_chunks)

def get_uniprot_entry_name(header):
    """
    Extracts the UniProt entry name from a header like:
    >sp|P07270|PHO4_YEAST Phosphate system positive...
    Returns: PHO4_YEAST
    """
    if header.startswith(">"):
        header = header[1:]
    first_token = header.split()[0]  # e.g. 'sp|P07270|PHO4_YEAST'
    parts = first_token.split("|")
    if len(parts) >= 3:
        return parts[2]  # PHO4_YEAST
    else:
        # Fallback: use the whole token if format is unexpected
        return first_token

def fetch_by_entry_names(uniprot_fasta, id_list_path, output_fasta):
    # Read desired IDs into a set
    with open(id_list_path) as f:
        wanted = {line.strip() for line in f if line.strip()}
    remaining = set(wanted)

    n_found = 0

    with open(uniprot_fasta) as db, open(output_fasta, "w") as out:
        for header, seq in iter_fasta(db):
            entry_name = get_uniprot_entry_name(header)
            if entry_name in remaining:
                # Write header unchanged, sequence wrapped at 60 chars
                out.write(header + "\n")
                for chunk in wrap(seq, 60):
                    out.write(chunk + "\n")
                n_found += 1
                remaining.remove(entry_name)
                if not remaining:
                    break  # found everything

    # Optional: report what happened
    sys.stderr.write(f"Requested IDs: {len(wanted)}\n")
    sys.stderr.write(f"Found sequences: {n_found}\n")
    if remaining:
        sys.stderr.write("Not found:\n")
        for r in sorted(remaining):
            sys.stderr.write(f"  {r}\n")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "Usage: python fetch_uniprot_by_name.py <uniprot.fasta> <ids.txt> <out.fasta>",
            file=sys.stderr,
        )
        sys.exit(1)

    uniprot_fasta = sys.argv[1]
    ids_file = sys.argv[2]
    out_fasta = sys.argv[3]

    fetch_by_entry_names(uniprot_fasta, ids_file, out_fasta)