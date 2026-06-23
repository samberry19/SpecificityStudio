#!/bin/bash 
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:1
#SBATCH -p gpu_quad
#SBATCH -t 4:00:00
#SBATCH --mem=30G
#SBATCH --output=./slurm/tranception_score-%j.out
#SBATCH --error=./slurm/tranception_score-%j.err
#SBATCH --job-name="tranception_score"

source /n/groups/marks/users/sam/SpecificityStudio/zero_shot_config_SS.sh

export checkpoint=/home/sb611/lab/SpecificityStudio/models/checkpoints/Tranception_Large
export output_scores_folder=${DMS_output_score_folder_subs}/Tranception_no_retrieval

export DMS_index=$1

python ../ProteinGym/proteingym/baselines/tranception/score_tranception_proteingym.py \
                --checkpoint ${checkpoint} \
                --DMS_reference_file_path ${DMS_reference_file_path_subs} \
                --DMS_data_folder ${DMS_data_folder_subs} \
                --DMS_index ${DMS_index} \
                --output_scores_folder ${output_scores_folder} 