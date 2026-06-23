import numpy as np
from numba import jit
from evcouplings.couplings import CouplingsModel
import os
import pandas as pd

import argparse

def DCAEnergy(s, model, independent=False):

    '''DCA energy function that can take in numeric or one-hot encoded sequences.

    Parameters
    ----------
    s: a protein sequence, either a numpy array of length L or a
            one-hot encoded array of length 20*L
    model: a CouplingsModel object (the DCA model to score with)

    optional:
        independent : calculate without couplings terms (using only h_i); defaults to FALSE
        one_hot : whether the input sequence is one-hot encoded (defaults to FALSE)

    Returns
    -------
    E : the DCA energy of the sequence
    '''

    return potts_model_hamiltonian(s, model.h_i, model.J_ij, independent=independent)


@jit(nopython=True)
def potts_model_hamiltonian(seq, hi, Jij, independent=False):

    ''' This jit-compiled function does the actual math because it's faster '''

    E = 0

    for i,x in enumerate(seq):

        E += hi[(i,x)]

        if not independent:
            for j,y in enumerate(seq[:i]):

                E += Jij[(i, j, x, y)]

    return E

def map_to_alphabet(sequence, alphabet):

    return np.array([np.where(alphabet==i)[0][0] for i in sequence])

def EVmutation_score_sequences(model, df, seq_col="aa_seq", wt_id="WT", offset=1):

    ind_model = model.to_independent_model()

    seq_list = list(df[seq_col])
    # if 'WT' not in seq_list and 'M1M' not in seq_list:
    #     seq_list.append('WT')
    seqs_num = np.array([map_to_alphabet(seq, model.alphabet) for seq in df[seq_col]])

    ind_energies = pd.Series([DCAEnergy(s[ind_model.index_list-offset], ind_model) for s in seqs_num], index=df.index, name="independent_energy")
    dca_energies = pd.Series([DCAEnergy(s[model.index_list-offset], model) for s in seqs_num], index=df.index, name="couplings_energy")

    try:
        ind_scores = ind_energies - ind_energies.loc['WT']
        dca_scores = dca_energies - dca_energies.loc['WT']
    except:
        ind_scores = ind_energies - ind_energies.loc[df.mutant=='M1M']
        dca_scores = dca_energies - dca_energies.loc[df.mutant=='M1M']
    
    return pd.concat([ind_energies, dca_energies, ind_scores.rename("independent_score"), dca_scores.rename("couplings_score")], axis=1)
    

if __name__ == "__main__":

    # Create the parser
    parser = argparse.ArgumentParser()
    
    # Add arguments
    parser.add_argument("--DMS_reference_file_path", type=str, help="reference file")
    parser.add_argument("--DMS_index", type=int)
    parser.add_argument("--DMS_data_folder", type=str)
    parser.add_argument("--model_folder", type=str)
    parser.add_argument("--output_scores_folder", type=str, default="./")
    
    # Parse the arguments
    args = parser.parse_args()

    mapping = pd.read_csv(args.DMS_reference_file_path)

    list_DMS = mapping["DMS_id"]
    DMS_id = list_DMS[args.DMS_index]
    DMS_filename = mapping["DMS_filename"][mapping["DMS_id"]==DMS_id].values[0]
    offset = mapping["MSA_start"][mapping["DMS_id"]==DMS_id].values[0] - 1
    data = pd.read_csv(args.DMS_data_folder + os.sep + DMS_filename, index_col=0)
    
    model = CouplingsModel(f"{args.model_folder}/{DMS_id}.model")

    scores = EVmutation_score_sequences(model, data, seq_col='mutated_sequence')
    
    scores = pd.concat([data[['mutated_sequence']], scores], axis=1)

    scores.to_csv(f"{args.output_scores_folder}/{DMS_id}.csv")