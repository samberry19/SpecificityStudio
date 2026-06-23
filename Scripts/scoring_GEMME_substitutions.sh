#!/bin/bash
#SBATCH -c 1
#SBATCH -N 1
#SBATCH -t 0-04:00
#SBATCH -p short
#SBATCH --mem=20G
#SBATCH -o slurm/gemme_%j.out
#SBATCH -e slurm/gemme_%j.err
#SBATCH --job-name="gemme-score"

set -euo pipefail

CONTAINER="/n/app/containers/shared/marks/gemme_gemme.sif"
BIND_SRC="/n/groups/marks/users/sam/SpecificityStudio"
BIND_DEST="/sstudio"

eval "$(python export_from_csv.py ../SpecificityStudio_reference_sheet.csv --row-index "$1")"

apptainer exec \
  --bind "${BIND_SRC}:${BIND_DEST}" \
  --pwd "${BIND_DEST}/scripts" \
  "${CONTAINER}" \
  bash "${BIND_DEST}/scripts/run_gemme.sh" --row-index "$1"