#!/usr/bin/env bash
set -euxo pipefail

STRUCTURE_DIR="/sstudio/structures"
MSA_DIR="/sstudio/msas"
MUT_DIR="/sstudio/processed_data"

echo "$@"

python3 export_from_csv.py /sstudio/SpecificityStudio_reference_sheet.csv "$@"

eval "$(python3 export_from_csv.py /sstudio/SpecificityStudio_reference_sheet.csv "$@")"

echo ${PDB_FILE}

cd /sstudio/model_scores/ESCOTT

escott -p "${STRUCTURE_DIR}/${PDB_FILE}" -m "${MUT_DIR}/${ESCOTT_MUT_FILE}" "${MSA_DIR}/${MSA_FILENAME}"