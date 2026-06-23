#!/bin/bash
#SBATCH -c 1                              # Request one core
#SBATCH -N 1                               # Request one node (if you request more than one core with -c, also using
                                           # -N 1 means all cores will be on the same node)
#SBATCH -t 0-08:00                         # Runtime in D-HH:MM format
#SBATCH -p short                        # Partition to run in
#SBATCH --mem=20G                        # Memory total in MB (for all cores)
#SBATCH -o slurm/evm_%j.out                            # File to which STDOUT will be written, including job ID
#SBATCH -e slurm/evm_%j.err                   # File to which STDERR will be written, including job ID
#SBATCH --job-name="evmutation-score"

source /n/groups/marks/users/sam/SpecificityStudio/zero_shot_config_SS.sh

export output_score_folder=${DMS_output_score_folder_subs}/EVmutation/
export model_folder="../EVcouplings/models/"
export DMS_index=$1
python ../ProteinGym/proteingym/baselines/EVmutation/score_mutants.py \
    --DMS_index $DMS_index \
    --DMS_data_folder $DMS_data_folder_subs \
    --model_folder $model_folder \
    --output_scores_folder $output_score_folder \
    --DMS_reference_file_path ${DMS_reference_file_path_subs}