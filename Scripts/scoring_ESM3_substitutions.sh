#!/bin/bash 
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:1
#SBATCH -p gpu_quad
#SBATCH -t 1:00:00
#SBATCH --mem=40G
#SBATCH --output=./slurm/esm3_score-%j.out
#SBATCH --error=./slurm/esm3_score-%j.err
#SBATCH --job-name="esm3_score"

source /n/groups/marks/users/sam/SpecificityStudio/zero_shot_config_SS.sh

MODEL_DIR="/n/groups/marks/users/sam/SpecificityStudio/models/checkpoints"
#export model_checkpoint="${MODEL_DIR}/esm_if1_gvp4_t16_142M_UR50.pt"
export DMS_index=$1

export dms_output_folder=${DMS_output_score_folder_subs}/ESM3/ 

echo ${DMS_data_folder_subs}

python ../ProteinGym/proteingym/baselines/evoscale/compute_fitness_elains_version.py \
    --model_type "esm3_open" \
    --reference_csv ${DMS_reference_file_path_subs} \
    --dms_dir ${DMS_data_folder_subs} \
    --DMS_index ${DMS_index} \
    --pdb_dir ${DMS_structure_folder} \
    --output_dir ${dms_output_folder} \
    --use_structure