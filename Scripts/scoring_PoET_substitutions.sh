#!/bin/bash 
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:a100:1
#SBATCH -p gpu_quad
#SBATCH -t 2-00:00
#SBATCH --mem=10G
#SBATCH --output=./slurm/poet_score-%j.out
#SBATCH --error=./slurm/poet_score-%j.err
#SBATCH --job-name="poet_score"

source /n/groups/marks/users/sam/SpecificityStudio/zero_shot_config_SS.sh
#source activate /n/groups/marks/software/anaconda_o2/envs/proteingym_env

module load gcc/14.2.0 cuda/12.8

MODEL_DIR="/n/groups/marks/users/sam/SpecificityStudio/models/"

export checkpoint=${MODEL_DIR}/PoET/data/poet.ckpt
export output_scores_folder=${DMS_output_score_folder_subs}/PoET

export DMS_index=$1

echo ${DMS_reference_file_path_subs}

python ../ProteinGym/proteingym/baselines/PoET/scripts/score.py \
    --checkpoint ${checkpoint} \
    --DMS_reference_file_path ${DMS_reference_file_path_subs} \
    --DMS_data_folder ${DMS_data_folder_subs} \
    --DMS_index ${DMS_index} \
    --output_scores_folder ${output_scores_folder} \
    --MSA_folder ${DMS_MSA_data_folder} \
    --context_lengths 6144 12288 24576 \
    --batch_size 8
