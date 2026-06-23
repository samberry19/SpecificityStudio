#!/bin/bash 
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:1
#SBATCH -p gpu_quad
#SBATCH -t 1:00:00
#SBATCH --mem=80G
#SBATCH --output=./slurm/eve_score-%j.out
#SBATCH --error=./slurm/eve_score-%j.err
#SBATCH --job-name="eve_score"

source /n/groups/marks/users/sam/SpecificityStudio/zero_shot_config_SS.sh
#source activate /n/groups/marks/software/anaconda_o2/envs/proteingym_env

module load gcc/14.2.0 cuda/12.8

export DMS_index=$1
export model_parameters_location='../ProteinGym/proteingym/baselines/EVE/EVE/default_model_params.json'
export training_logs_location='../ProteinGym/proteingym/baselines/EVE/logs/'
export computation_mode='DMS'
export output_scores_folder="${DMS_output_score_folder_subs}EVE/"
export num_samples_compute_evol_indices=20000
export batch_size=1024  # Pushing batch size to limit of GPU memory
export random_seeds="77"

echo ${output_scores_folder}

python ../ProteinGym/proteingym/baselines/EVE/compute_evol_indices_DMS.py \
    --MSA_data_folder ${DMS_MSA_data_folder} \
    --DMS_reference_file_path ${DMS_reference_file_path_subs} \
    --protein_index ${DMS_index} \
    --VAE_checkpoint_location ${DMS_EVE_model_folder} \
    --model_parameters_location ${model_parameters_location} \
    --DMS_data_folder ${DMS_data_folder_subs} \
    --output_scores_folder ${output_scores_folder} \
    --num_samples_compute_evol_indices 20000 \
    --batch_size ${batch_size} \
    --aggregation_method "full" \
    --threshold_focus_cols_frac_gaps 1 \
    --skip_existing \
    --MSA_weights_location ${DMS_MSA_weights_folder} \
    --random_seeds ${random_seeds} 
