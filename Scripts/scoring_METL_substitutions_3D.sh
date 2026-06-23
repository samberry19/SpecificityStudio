source /n/groups/marks/users/sam/SpecificityStudio/zero_shot_config_SS.sh

module load gcc/14.2.0 cuda/12.8

export dms_output_folder="${DMS_output_score_folder_subs}/METL_3D/"

python compute_fitness_metl.py \
  --model-uuid YoQkzoLD \
  --dms-input ${DMS_data_folder_subs} \
  --dms-output ${dms_output_folder} \
  --dms-mapping ${DMS_reference_file_path_subs} \
  --structure-folder ${DMS_structure_folder} \
  --dms-index $1