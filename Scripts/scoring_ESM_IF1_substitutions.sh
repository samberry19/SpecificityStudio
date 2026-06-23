#!/bin/bash 
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:1
#SBATCH -p gpu_quad
#SBATCH -t 5:00:00
#SBATCH --mem=40G
#SBATCH --output=./slurm/esmif1_train-%j.out
#SBATCH --error=./slurm/esmif1_train-%j.err
#SBATCH --job-name="esmif1_score"

source /n/groups/marks/users/sam/SpecificityStudio/zero_shot_config_SS.sh
#module load conda/miniforge3/24.11.3-0
#conda activate /n/groups/marks/users/sam/SpecificityStudio/pg2/model_envs/esm-if1

## Regression weights are at: https://dl.fbaipublicfiles.com/fair-esm/regression/esm2_t33_650M_UR50S-contact-regression.pt
#https://dl.fbaipublicfiles.com/fair-esm/regression/esm2_t33_650M_UR50S-contact-regression.pt

MODEL_DIR="/n/groups/marks/users/sam/SpecificityStudio/models/checkpoints"
export model_checkpoint="${MODEL_DIR}/esm_if1_gvp4_t16_142M_UR50.pt"
export DMS_output_score_folder="${DMS_output_score_folder_subs}ESM-IF1/"
export DMS_index=$1

echo ${DMS_output_score_folder}

python ../ProteinGym/proteingym/baselines/esm/compute_fitness_esm_if1.py \
    --model_location ${model_checkpoint} \
    --structure_folder ${DMS_structure_folder} \
    --DMS_index $DMS_index \
    --DMS_reference_file_path ${DMS_reference_file_path_subs} \
    --DMS_data_folder ${DMS_data_folder_subs} \
    --output_scores_folder ${DMS_output_score_folder} 