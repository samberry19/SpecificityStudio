#!/bin/bash 
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:1
#SBATCH -p gpu_quad
#SBATCH -t 10:00:00
#SBATCH --mem=30G
#SBATCH --output=./slurm/progen_score-%j.out
#SBATCH --error=./slurm/progen_score-%j.err
#SBATCH --job-name="progen_score"

source /n/groups/marks/users/sam/SpecificityStudio/zero_shot_config_SS.sh
 
export Progen2_model_name_or_path=../models/checkpoints/
export output_scores_folder="${DMS_output_score_folder_subs}/Progen2"

export DMS_index=$1

python ../ProteinGym/proteingym/baselines/progen2/compute_fitness.py \
            --Progen2_model_name_or_path ${Progen2_model_name_or_path} \
            --DMS_reference_file_path ${DMS_reference_file_path_subs} \
            --DMS_data_folder ${DMS_data_folder_subs} \
            --DMS_index $DMS_index \
            --output_scores_folder ${output_scores_folder}
