#!/bin/bash 
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:1
#SBATCH -p gpu_quad
#SBATCH -t 0:05:00
#SBATCH --mem=40G
#SBATCH --output=./slurm/esm1v_train-%j.out
#SBATCH --error=./slurm/esm1v_train-%j.err
#SBATCH --job-name="esm1v_score"

source /n/groups/marks/users/sam/SpecificityStudio/zero_shot_config_SS.sh
#source activate /n/groups/marks/software/anaconda_o2/envs/proteingym_env

module load gcc/14.2.0 cuda/12.8

MODEL_DIR="/n/groups/marks/users/sam/SpecificityStudio/models/checkpoints"

# ESM-1v parameters 
# Five checkpoints for ESM-1v
export model_checkpoint1=${MODEL_DIR}/esm1v_t33_650M_UR90S_1.pt
export model_checkpoint2=${MODEL_DIR}/esm1v_t33_650M_UR90S_2.pt
export model_checkpoint3=${MODEL_DIR}/esm1v_t33_650M_UR90S_3.pt
export model_checkpoint4=${MODEL_DIR}/esm1v_t33_650M_UR90S_4.pt
export model_checkpoint5=${MODEL_DIR}/esm1v_t33_650M_UR90S_5.pt
# combine all five into one string 
export model_checkpoint="${model_checkpoint1} ${model_checkpoint2} ${model_checkpoint3} ${model_checkpoint4} ${model_checkpoint5}"

export dms_output_folder="${DMS_output_score_folder_subs}/ESM1v/"

export model_type="ESM1v"
export scoring_strategy="masked-marginals"  # MSATransformer only uses masked-marginals
export scoring_window="optimal"
export DMS_index=$1

python /n/groups/marks/users/sam/SpecificityStudio/ProteinGym/proteingym/baselines/esm/compute_fitness.py \
    --model-location ${model_checkpoint} \
    --model_type ${model_type} \
    --dms_index ${DMS_index} \
    --dms_mapping ${DMS_reference_file_path_subs} \
    --dms-input ${DMS_data_folder_subs} \
    --dms-output ${dms_output_folder} \
    --scoring-strategy ${scoring_strategy} \
    --scoring-window ${scoring_window}
