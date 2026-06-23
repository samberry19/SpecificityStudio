# This file has all general filepaths and directories used in the scoring pipeline. The individual scripts may have 
# additional parameters specific to each method 

# DMS zero-shot parameters

# Folders containing the csvs with the variants for each DMS assay
# export DMS_data_folder_subs="Folder containing DMS substitution csvs"
export DMS_data_folder_subs="/n/groups/marks/users/sam/SpecificityStudio/processed_data"

# Folders containing multiple sequence alignments and MSA weights for all DMS assays
export DMS_MSA_data_folder="/n/groups/marks/users/sam/SpecificityStudio/msas"
export DMS_MSA_weights_folder="/n/groups/marks/users/sam/SpecificityStudio/weights"

# Reference files for substitution and indel assays
export DMS_reference_file_path_subs="/n/groups/marks/users/sam/SpecificityStudio/SpecificityStudio_reference_sheet.csv"

# Folders where fitness predictions for baseline models are saved 
# export DMS_output_score_folder_subs="folder for DMS substitution scores"
export DMS_output_score_folder_subs="/n/groups/marks/users/sam/SpecificityStudio/model_scores/"

# Folder containing EVE models for each DMS assay
export DMS_EVE_model_folder="/n/groups/marks/users/sam/SpecificityStudio/EVE_models"

# Folders containing predicted structures for the DMSs 
export DMS_structure_folder="/n/groups/marks/users/sam/SpecificityStudio/structures"