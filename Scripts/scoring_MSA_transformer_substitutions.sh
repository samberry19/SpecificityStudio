#!/bin/bash 
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:1
#SBATCH -p gpu_quad
#SBATCH -t 1-00:00
#SBATCH --mem=80G
#SBATCH --output=./slurm/msa_transformer_train-%j.out
#SBATCH --error=./slurm/msa_transformer_train-%j.err
#SBATCH --job-name="msa_transformer_train"

source /n/groups/marks/users/sam/SpecificityStudio/zero_shot_config_SS.sh
export DMS_index=$1
export seed=77

# MSA transformer checkpoint 
export model_checkpoint="/n/groups/marks/users/sam/SpecificityStudio/models/checkpoints/esm_msa1b_t12_100M_UR50S.pt"
export DMS_index=$1
export dms_output_folder="${DMS_output_score_folder_subs}/MSA_Transformer/"
export scoring_strategy=masked-marginals # MSA transformer only supports "masked-marginals"
export model_type=MSA_transformer
export scoring_window="optimal"
export random_seeds="1 2 3 4 5"
export DMS_MSA_weights_for_MSA_Transformer_folder="${DMS_MSA_weights_folder}" # Use weights recomputed post MSA filtering used in MSA Transformer

python ../ProteinGym/proteingym/baselines/esm/compute_fitness.py \
    --model-location ${model_checkpoint} \
    --model_type ${model_type} \
    --dms_index ${DMS_index} \
    --dms_mapping ${DMS_reference_file_path_subs} \
    --dms-input ${DMS_data_folder_subs} \
    --dms-output ${dms_output_folder} \
    --scoring-strategy ${scoring_strategy} \
    --scoring-window ${scoring_window} \
    --msa-path ${DMS_MSA_data_folder} \
    --msa-weights-folder ${DMS_MSA_weights_for_MSA_Transformer_folder} \
    --seeds ${random_seeds}
