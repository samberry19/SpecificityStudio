import numpy as np
from EVE.VAE_model import VAE_model
import json
import torch
from utils import data_utils
import pandas as pd
import torch.nn.functional as F

def score_sequences(vae_model, sequences, batch_size=256, num_samples=20000):

    '''
    Return the ELBO score ("evolutionary index") of a set of sequences given a pretrained VAE model.
    '''

    dataloader = torch.utils.data.DataLoader(sequences.one_hot_encoding, batch_size=batch_size, shuffle=False, num_workers=4, pin_memory=True)

    z_dim = vae_model.encoder.z_dim
    N = len(sequences)

    elbo_matrix = torch.zeros((N, num_samples))
    mu_matrix = torch.zeros((N, z_dim))
    log_var_matrix = torch.zeros((N, z_dim))

    with torch.no_grad():
        for i, batch in enumerate(dataloader):

            # Make sure we have the appropriate data type (?)
            x = batch.type(vae_model.dtype).to(vae_model.device)

            # Encode the sequences in the latent space and store those encodings
            #  (both means and log variances)
            mu, log_var = vae_model.encoder(x)
            mu_matrix[i*batch_size:i*batch_size+len(x)] = mu
            log_var_matrix[i*batch_size:i*batch_size+len(x)] = log_var

            # Average over num_samples samples from the latent space
            for j in range(num_samples):

                # sample a vector given the latent dimension and decode it
                z = vae_model.sample_latent(mu, log_var)
                recon_x_log = vae_model.decoder(z)

                # I don't know what this does
                recon_x_log = recon_x_log.view(-1, vae_model.alphabet_size*vae_model.seq_len)
                x = x.view(-1, vae_model.alphabet_size*vae_model.seq_len)

                BCE_batch_tensor = torch.sum(F.binary_cross_entropy_with_logits(recon_x_log, x, reduction='none'),dim=1)
                KLD_batch_tensor = (-0.5 * torch.sum(1 + log_var - mu.pow(2) - log_var.exp(),dim=1))

                ELBO_batch_tensor = -(BCE_batch_tensor + KLD_batch_tensor)

                # store the elbo batch tensor
                elbo_matrix[i*batch_size:i*batch_size+len(x),j] = ELBO_batch_tensor

        # take the mean and std elbo over the batches
        mean_predictions = elbo_matrix.mean(dim=1, keepdim=False)
        std_predictions = elbo_matrix.std(dim=1, keepdim=False)

        # here we calculate the elbo relative to the reference sequence to get 'mutation effect'
        #   and call (-) this the evolutionary_index
        delta_elbos = mean_predictions - mean_predictions[0]
        evol_indices =  -delta_elbos.detach().cpu().numpy()   # store it as a numpy array

    # put all of these things into a pandas dataframe
    evo_dict = {}
    evo_dict['name'] = sequences.seq_names
    evo_dict['mean score'] = mean_predictions
    evo_dict['std'] = std_predictions
    evo_dict['evol_indices'] = evol_indices
    for i in range(z_dim):
        evo_dict['mu_'+str(i+1)] = mu_matrix[:,i]
        evo_dict['log_var_'+str(i+1)] = log_var_matrix[:,i]

    return pd.DataFrame.from_dict(evo_dict)

