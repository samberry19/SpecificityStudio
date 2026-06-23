import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math

from scipy.stats import linregress
from copy import copy
from scipy.stats import sem

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42

def get_raw_sequence_from_df_ids(dms_df, mut_sep='/', L=None, first_index=1):
    
    if L is None:
        pos_list = [int(i[1:-1]) for i in dms_df.index if mut_sep not in i and i.lower()!='wt']
        L = np.max(pos_list)
        print(f"Identified maximum mutated position of {L}, using as sequence length")
        
    seq = ['_' for i in range(L)]

    for v in dms_df.index:
        muts = v.split(mut_sep)
        for mut in muts:
            if mut.lower()!='wt':
                try:
                    pos = int(mut[1:-1])-1
                except:
                    pos=None
                    print(f"Cannot obtain position information from mutation string {mut}")
    
                wt_aa = mut[0]
                if seq[pos]=='_':
                    seq[pos] = wt_aa
                elif seq[pos]==wt_aa:
                    pass
                else:
                    print(f"Inconsistency in mutation names found in mutation {mut}. Already assigned to {seq[pos]}")

    return ''.join(seq)

def assign_specificity_categories(df, inactive_function, specificity_altering_function, exclude=None):

    categories = []
    
    for var,row in df.iterrows():

        inactive = inactive_function(var,row)
        if inactive:
            categories.append('inactive')
        elif specificity_altering_function(var,row):
            categories.append("altered-specificity")
        elif exclude is not None:
            if exclude(var,row):
                categories.append('excluded')
            else:
                categories.append("native-specificity")
        else:
            categories.append("native-specificity")

    df2 = df.copy()
    df2.loc[:,'specificity_category'] = pd.Series(categories, index=df.index)

    return df2

def assign_mutant_column(df):

    mutants = []
    for var in df.index:
        v=str(copy(var))
        for sep_char in (',','_','+','/'):
            if sep_char in v:
                v = v.replace(sep_char,':')
        for m in v.split(':'):
            if m[0]==m[-1]:
                v = v.replace(f":{m}", '').replace(f"{m}:", '').replace(f"{m}",'')
        if v=='WT' or v=='':
            v='M1M'
        mutants.append(v)
    df['mutant'] = pd.Series(mutants, index=df.index)
    return df

# Reuse the mutation repair functions from earlier
def apply_mutations(reference_seq, mutation_str, first_index=1):

    if mutation_str.lower()=='wt':
        return reference_seq
    else: 
        seq = list(reference_seq)
        mutations = mutation_str.split(':')
        for mut in mutations:
            orig_aa = mut[0]
            mut_aa = mut[-1]
            pos_str = mut[1:-1]
            try:
                pos = int(pos_str) - first_index
            except:
                print(f"{mut[1:-1]} from mutation {mut} is not a valid position!")
            if pos > len(seq):
                print(f"Can't index position {pos} from sequence of length {len(seq)}")
            elif pos < 0:
                print(f"Can't index negative position {pos} - check your first_index!")
            if seq[pos] != orig_aa:
                raise ValueError(f"Reference mismatch at position {pos+1}: expected '{orig_aa}', found '{seq[pos]}'")
            seq[pos] = mut_aa
        return ''.join(seq)

def get_variant(reference, mutations, start_index=1):
    variant = reference.copy()
    for mut in mutations:
        pos = int(mut[1:-1])-start_index
        variant[pos] = mut[-1]
    return variant

def selector(df, dic):

    '''A little tool for selecting from pandas dataframes by passing a dictionary, e.g.
            selector(df, {"color":"red", "shape":["square", "circle"]})
       
        For advanced usage, you can pass a function and it will return where True, e.g.
            selector(df, ["name": lambda name: "Sam" in name])
           
        You can also use this to select things greater than or less than a value, e.g.
            selector(df, ["enrichment": lambda enr: enr > 1])'''
   
    X = df.copy()

    for key,val in dic.items():
       
        # If you pass a tuple, list or numpy array
        if isinstance(val, (tuple, list, np.ndarray)):
            where = np.any(np.array([X[key]==v for v in val]),axis=0)
            X = X.loc[where]
           
        # If you pass a function
        elif isinstance(val, type(lambda x: x+1)):
            X = X.loc[X[key].apply(val)]
            
        elif isinstance(val, str) and '>' in val:
            
            if val.count('>')==2:
                X = X.loc[(X[key]<float(val.split('>')[0])) & (X[key]>float(val.split('>')[2]))]
            else:
                X = X.loc[X[key]>float(val.split('>')[1])]
                      
        elif isinstance(val, str) and '<' in val:
            
            if val.count('<')==2:
                X = X.loc[(X[key]>float(val.split('<')[0])) & (X[key]<float(val.split('<')[2]))]
            else:
                X = X.loc[X[key]<float(val.split('<')[1])]
           
        # Otherwise we assume it's a single value
        else:
            X = X.loc[X[key]==val]

    return X

from matplotlib.colors import LogNorm

def hexbin_plot(data, x, y, ax=None, figsize=(5.5,5), cmap='cividis', log_hue=True, vmin=1, vmax=100, cbar_shrink=0.5, **kwargs):
    
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    
    if log_hue:
        kwargs['norm'] = LogNorm(vmin=vmin, vmax=vmax)
    
    hb = ax.hexbin(data[x], data[y], cmap=cmap, **kwargs)
    plt.colorbar(hb, shrink=cbar_shrink)
    
    return ax, hb

def perpendicular_line(m, b, x0):
    # Compute y0 on the original line
    y0 = m * x0 + b

    # Perpendicular slope
    if m == 0:
        # Original line is horizontal, perpendicular is vertical (undefined slope)
        return f"x = {x0}"
    elif m == float('inf') or m == -float('inf'):
        # Original line is vertical, perpendicular is horizontal
        return f"y = {y0}"
    else:
        m_perp = -1 / m
        # Now compute y-intercept of the perpendicular line using y = mx + b
        b_perp = y0 - m_perp * x0
        return m_perp, b_perp  # returns slope and intercept

import math

def perpendicular_intersection_and_distance(m, b, x1, y1):
    if m == 0:
        # Original line is horizontal: y = b
        x_intersect = x1
        y_intersect = b
    else:
        # Perpendicular slope
        m_perp = -1 / m
        # Intercept of the perpendicular line
        b_perp = y1 - m_perp * x1
        # Solve for intersection: mx + b = m_perp * x + b_perp
        x_intersect = (b_perp - b) / (m - m_perp)
        y_intersect = m * x_intersect + b

    # Euclidean distance
    dx = x1 - x_intersect
    dy = y1 - y_intersect
    
    distance = np.sqrt(dx**2 + dy**2)

    return (x_intersect, y_intersect), distance

def check_dataset(df, first_index=1):

    print("Checking dataset table:")
    passed = 0

    if 'DMS_score' in df:
        print(f"✅ DMS_score in table")
        passed+=1
    else:
        print("❌ Warning: no column 'DMS_score' present in table, some models require this column")

    if 'mutated_sequence' in df:
        print(f"✅ mutated_sequence in table")
        passed+=1
    else:
        print("❌ Warning: no column 'mutated_sequence' present in table, some models require this column")

    if 'mutant' in df:
        print(f"✅ mutant in table")
        passed+=1

        if 'M1M' in df.mutant.values:
            print(f"✅ Contains WT sequence (M1M)")
            passed+=1
        else:
            print("❌ Warning: no row 'M1M' present in table, WT sequence will not be scored")

        failed_mutants = []
        for n,mut in df.mutant.items():
            try:
                for m in mut.split(':'):
                    p = int(m[1:-1])
                    seq = df.loc[n].mutated_sequence
                    #assert m[0]==seq[p-first_index]
                    assert m[-1]==seq[p-first_index]
            except:
                failed_mutants.append(mut)
        if len(failed_mutants)==0:
            print(f"✅ all mutants pass checks and match sequence")
            passed+=1

        else:
            print(f"❌ Issues with the following variants: {', '.join(failed_mutants)}")
        
    else:
        print("❌ Warning: no column 'mutant' present in table, some models require this column")

    print('')
    if passed == 5:
        print("✅ All checks passed!")
    else:
        print("❌ Better check again...")

default_palette={"altered-specificity":"orangered", "native-specificity":"dodgerblue", "inactive":"lightgray", "other":"darkgray"}
gentle_palette={"altered-specificity":"xkcd:apricot", "native-specificity":"lightblue", "inactive":"lightgray", "other":"darkgray"}
default_hue_order = ["native-specificity", "altered-specificity", "inactive"]

import os
import pandas as pd

# Reuse the mutation repair functions from earlier
def apply_mutations(reference_seq, mutation_str):

    if mutation_str.lower()=='wt':
        return reference_seq
    else: 
        seq = list(reference_seq)
        mutations = mutation_str.split(':')
        for mut in mutations:
            orig_aa = mut[0]
            mut_aa = mut[-1]
            pos_str = mut[1:-1]
            pos = int(pos_str) - 1
            if seq[pos] != orig_aa:
                raise ValueError(f"Reference mismatch at position {pos+1}: expected '{orig_aa}', found '{seq[pos]}'")
            seq[pos] = mut_aa
        return ''.join(seq)

def infer_mutations(reference_seq, mutant_seq):
    if len(reference_seq) != len(mutant_seq):
        raise ValueError("Mutant sequence length does not match reference.")
    mut_str =  ":".join(
        f"{ref}{i+1}{mut}" for i, (ref, mut) in enumerate(zip(reference_seq, mutant_seq)) if ref != mut
    )

    if len(mut_str)>0:
        return mut_str
    else:
        return 'WT'

def repair_mutant_sequence_columns(df, reference_seq, mutant_col='mutant', seq_col='mutated_sequence', debug=False):
    df = df.copy()
    if mutant_col not in df.columns and seq_col not in df.columns:
        raise ValueError("DataFrame must have at least one of 'mutant' or 'mutated_sequence'")
    if mutant_col not in df.columns:
        if debug:
            print(f'{mutant_col} not in columns: attempting to repair...')
        df[mutant_col] = df[seq_col].apply(lambda s: infer_mutations(reference_seq, s))
    if seq_col not in df.columns:
        if debug:
            print(f'{seq_col} not in columns: attempting to repair...')
        df[seq_col] = df[mutant_col].apply(lambda m: apply_mutations(reference_seq, m))
    return df

# Main pipeline
def merge_model_scores(data_root, model_score_csv, reference_seq, assay_filename, output_csv, debug=False):
    score_map = pd.read_csv(model_score_csv)
    merged = None
    errors = []
    for _, row in score_map.iterrows():
        model_name, score_col = row["model"], row["col"]
        model_path = os.path.join(data_root, *model_name.split('.'))
        found_file = None
        
        # Check top-level model directory
        top_level_file = os.path.join(model_path, assay_filename)
        if os.path.isfile(top_level_file):
            found_file = top_level_file
        else:
            # Check subdirectories for version
            for submodel in os.listdir(model_path):
                subdir = os.path.join(model_path, submodel)
                candidate = os.path.join(subdir, assay_filename)
                if os.path.isfile(candidate):
                    found_file = candidate
                    break
        if not found_file:
            errors.append(f"{model_name}: file not found")
            continue
        if debug:
            print(f'Checking file for model {row["model"]}')
        try:
            df = pd.read_csv(found_file)
            if debug:
                print(f'Loaded CSV for {row["model"]} from {found_file}')
            df = repair_mutant_sequence_columns(df, reference_seq, debug=debug)
            if debug:
                print(f'Repaired mutant sequence column in {found_file}')
            if score_col not in df.columns:
                errors.append(f"{model_name}: missing score column '{score_col}'")
                continue
            df_model = df[["mutant", score_col]].copy()
            df_model.rename(columns={score_col: model_name}, inplace=True)
            if merged is None:
                merged = df_model
            else:
                merged = pd.merge(merged, df_model, on="mutant", how="outer")
        except Exception as e:
            errors.append(f"{model_name}: {e}")

    # Save result
    if merged is not None:
        merged.to_csv(output_csv, index=False)
        print(f"✅ Merged dataset saved to {output_csv}")
    else:
        print("❌ No valid dataframes were merged.")

    if errors:
        print("\n⚠️ Errors encountered:")
        for err in errors:
            print(" -", err)

    return merged

import pandas as pd
import numpy as np

def consolidate_duplicate_indices(df):
    """
    Consolidate duplicate indices in a DataFrame.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input DataFrame that may contain duplicate indices
    
    Returns:
    --------
    pandas.DataFrame
        DataFrame with duplicates consolidated (if any existed)
    
    Raises:
    -------
    ValueError
        If categorical columns have inconsistent values for the same index
    """
    # (a) Detect if there are duplicate indices
    if not df.index.duplicated().any():
        # (b) No duplicates found, return the same dataframe
        return df
    
    # (c) Print that duplicate indices were found
    duplicate_indices = df.index[df.index.duplicated(keep=False)].unique()
    print(f"Found {len(duplicate_indices)} duplicate indices")
    
    # Identify numeric and categorical columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()
    
    # (e) Check if categorical columns are consistent for duplicate indices
    if categorical_cols:
        for idx in duplicate_indices:
            subset = df.loc[idx]
            if isinstance(subset, pd.Series):
                continue  # Only one row, no conflict possible
            
            for col in categorical_cols:
                unique_values = subset[col].unique()
                if len(unique_values) > 1:
                    print(
                        f"Warning: inconsistent categorical values found for index '{idx}' "
                        f"in column '{col}': {list(unique_values)}"
                    )
    
    # (d) Group by index and aggregate
    agg_dict = {}
    
    # Mean for numeric columns
    for col in numeric_cols:
        agg_dict[col] = 'mean'
    
    # First (since they should all be the same) for categorical columns
    for col in categorical_cols:
        agg_dict[col] = 'first'
    
    df_consolidated = df.groupby(df.index).agg(agg_dict)
    
    print(f"Consolidated {len(df)} rows into {len(df_consolidated)} rows")
    
    return df_consolidated
        