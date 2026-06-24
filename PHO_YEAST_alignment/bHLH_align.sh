#!/bin/bash 
#SBATCH --cpus-per-task=4
#SBATCH -p priority
#SBATCH -t 3:00:00
#SBATCH --mem=50G
#SBATCH --output=./slurm/hmmbuild_bhlh-%j.out
#SBATCH --error=./slurm/hmmbuild_bhlh-%j.err
#SBATCH --job-name="bhlh_hmmbuild"

/n/groups/marks/software/jackhmmer/hmmer-3.3.1/bin/hmmalign -o bHLH2.aligned bHLH.hmm all_bHLH_sequences.fasta
