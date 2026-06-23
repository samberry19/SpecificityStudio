#!/bin/bash 
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:1
#SBATCH -p gpu_quad
#SBATCH -t 1-00:00
#SBATCH --mem=40G
#SBATCH --output=./slurm/eve_train-%j.out
#SBATCH --error=./slurm/eve_train-%j.err
#SBATCH --job-name="eve_train"

export DMS_index=$1
export seed=77

source /n/groups/marks/users/sam/SpecificityStudio/zero_shot_config_SS.sh

export model_parameters_location='../ProteinGym/proteingym/baselines/EVE/EVE/default_model_params.json'
export training_logs_location='../ProteinGym/proteingym/baselines/EVE/logs/'
export DMS_reference_file_path=$DMS_reference_file_path_subs
# export DMS_reference_file_path=$DMS_reference_file_path_indels

echo ${DMS_MSA_data_folder}

python ../ProteinGym/proteingym/baselines/EVE/train_VAE.py \
    --MSA_data_folder ${DMS_MSA_data_folder} \
    --DMS_reference_file_path ${DMS_reference_file_path} \
    --protein_index "${DMS_index}" \
    --MSA_weights_location ${DMS_MSA_weights_folder} \
    --VAE_checkpoint_location ${DMS_EVE_model_folder} \
    --model_parameters_location ${model_parameters_location} \
    --training_logs_location ${training_logs_location} \
    --threshold_focus_cols_frac_gaps 1 \
    --seed ${seed} \
    --skip_existing \
    --experimental_stream_data
