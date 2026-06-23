#!/bin/bash
#SBATCH -c 1                              # Request one core
#SBATCH -N 1                               # Request one node (if you request more than one core with -c, also using
                                           # -N 1 means all cores will be on the same node)
#SBATCH -t 0-02:00                         # Runtime in D-HH:MM format
#SBATCH -p short                        # Partition to run in
#SBATCH --mem=10G                        # Memory total in MB (for all cores)
#SBATCH -o slurm/gemme_%j.out                            # File to which STDOUT will be written, including job ID
#SBATCH -e slurm/gemme_%j.err                   # File to which STDERR will be written, including job ID
#SBATCH --job-name="GEMME-score"

source /n/groups/marks/users/sam/SpecificityStudio/zero_shot_config_SS.sh

export GEMME_LOCATION="path to GEMME installation"
export JET2_LOCATION="path to JET2 installation"
export TEMP_FOLDER="./gemme_tmp/"
export DMS_output_score_folder="${DMS_output_score_folder_subs}/GEMME/"

python ../ProteinGym/proteingym/baselines/gemme/compute_fitness.py --DMS_index=$DMS_index --DMS_reference_file_path=$DMS_reference_file_path_subs \
--DMS_data_folder=$DMS_data_folder_subs --MSA_folder=$DMS_MSA_data_folder --output_scores_folder=$DMS_output_score_folder \
--GEMME_path=$GEMME_LOCATION --JET_path=$JET2_LOCATION --temp_folder=$TEMP_FOLDER