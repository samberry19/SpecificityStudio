#!/bin/bash 
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:1
#SBATCH -p gpu_quad
#SBATCH -t 1:00:00
#SBATCH --mem=40G
#SBATCH --output=./slurm/esm2_score-%j.out
#SBATCH --error=./slurm/esm2_score-%j.err
#SBATCH --job-name="esm2_score"

source /n/groups/marks/users/sam/SpecificityStudio/zero_shot_config_SS.sh

export model_checkpoint="../models/checkpoints/esm2_t33_650M_UR50D.pt"
export dms_output_folder=${DMS_output_score_folder_subs}/ESM2

export model_type="ESM2"
export scoring_strategy="masked-marginals"
export DMS_index=$1

python ../ProteinGym/proteingym/baselines/esm/compute_fitness.py \
    --model-location ${model_checkpoint} \
    --dms_index $DMS_index \
    --dms_mapping ${DMS_reference_file_path_subs} \
    --dms-input ${DMS_data_folder_subs} \
    --dms-output ${dms_output_folder} \
    --scoring-strategy ${scoring_strategy} \
    --model_type ${model_type} 