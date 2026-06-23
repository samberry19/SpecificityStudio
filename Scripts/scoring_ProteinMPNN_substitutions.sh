#!/bin/bash 
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:1
#SBATCH -p gpu_quad
#SBATCH -t 1:00:00
#SBATCH --mem=40G
#SBATCH --output=./slurm/proteinmpnn_score-%j.out
#SBATCH --error=./slurm/proteinmpnn_score-%j.err
#SBATCH --job-name="proteinmpnn_score"

source /n/groups/marks/users/sam/SpecificityStudio/zero_shot_config_SS.sh

export output_scores_folder=${DMS_output_score_folder_subs}/ProteinMPNN

export model_checkpoint=/n/groups/marks/users/sam/SpecificityStudio/models/checkpoints/v_48_020.pt
export DMS_index=$1

python ../ProteinGym/proteingym/baselines/protein_mpnn/compute_fitness.py \
    --checkpoint ${model_checkpoint} \
    --structure_folder ${DMS_structure_folder} \
    --DMS_index $DMS_index \
    --DMS_reference_file_path ${DMS_reference_file_path_subs} \
    --DMS_data_folder ${DMS_data_folder_subs} \
    --output_scores_folder ${output_scores_folder}