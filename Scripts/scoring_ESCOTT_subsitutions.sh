#!/bin/bash
#SBATCH -c 1
#SBATCH -N 1
#SBATCH -t 0-04:00
#SBATCH -p short
#SBATCH --mem=20G
#SBATCH -o slurm/escott_%j.out
#SBATCH -e slurm/escott_%j.err
#SBATCH --job-name="escott-score"

set -euo pipefail

CONTAINER="/n/app/containers/shared/marks/prescott-docker_latest.sif"
BIND_SRC="/n/groups/marks/users/sam/SpecificityStudio"
BIND_DEST="/sstudio"

apptainer exec \
  --bind "${BIND_SRC}:${BIND_DEST}" \
  --pwd "${BIND_DEST}/scripts" \
  "${CONTAINER}" \
  bash "${BIND_DEST}/scripts/run_ESCOTT.sh" --row-index "$1"