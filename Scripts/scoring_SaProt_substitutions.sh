#!/bin/bash 
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:1
#SBATCH -p gpu_quad
#SBATCH -t 8:00:00
#SBATCH --mem=40G
#SBATCH --output=./slurm/saprot_train-%j.out
#SBATCH --error=./slurm/saprot_train-%j.err
#SBATCH --job-name="saprot_score"

source /n/groups/marks/users/sam/SpecificityStudio/zero_shot_config_SS.sh

export SaProt_model_path="/home/sb611/lab/SpecificityStudio/models/SaProt_650M_AF2/d9b9ad00ef61c0990e611b2b43f2231c7de24b38" #Path where you have downloaded all SaProt model/tokenizer files from the HF hub (https://huggingface.co/westlake-repl/SaProt_650M_AF2)
export output_scores_folder="${DMS_output_score_folder_subs}/SaProt_650M_AF2"
export foldseek_bin="/home/sb611/lab/SpecificityStudio/models/foldseek/bin/foldseek" #(Download from here: https://github.com/steineggerlab/foldseek?tab=readme-ov-file)

#export DMS_index="Experiment index to run (e.g. 0,1,...216)"
export DMS_index=$1

python ../ProteinGym/proteingym/baselines/saprot/compute_fitness.py \
            --foldseek_bin ${foldseek_bin} \
            --SaProt_model_name_or_path ${SaProt_model_path} \
            --DMS_reference_file_path ${DMS_reference_file_path_subs} \
            --DMS_data_folder ${DMS_data_folder_subs} \
            --structure_data_folder ${DMS_structure_folder} \
            --DMS_index $DMS_index \
            --output_scores_folder ${output_scores_folder}
