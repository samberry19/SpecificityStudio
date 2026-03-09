import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from bioviper import selector 

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['font.sans-serif'] = 'Arial'


import pickle 

import matplotlib.pyplot as plt
import pandas as pd 
#import seaborn as sns 
from matplotlib.colors import LogNorm

default_palette={"altered-specificity":"orangered", "native-specificity":"dodgerblue", "inactive":"lightgray", "other":"darkgray"}
default_hue_order = ["native-specificity", "altered-specificity", "inactive"]

def plot_boxplot(data, model, ax, palette=default_palette, hue_order=default_hue_order, w=0.9, gap=0.2, lw=1.5):

    sns.boxplot(data=data, y=model, hue="specificity_category", width=w, gap=gap, linewidth=lw, palette=palette, 
                dodge=True, ax=ax, 
                hue_order=hue_order)
    
    ax.legend('')
    ax.set_title(model.replace("_", " "), fontsize=8)

def StudioBoxplots(dataset, model_names, standardize_to_wt=True):

    default_palette={"altered-specificity":"orangered", "native-specificity":"dodgerblue", "inactive":"lightgray", "other":"darkgray"}
    default_hue_order = ["native-specificity", "altered-specificity", "inactive"]

    fig, ax = plt.subplots(1,len(model_names), figsize=(1*len(model_names), 3), sharey=True)

    model_scores = dataset[model_names]

    if standardize_to_wt:
        model_scores_standardized = (model_scores - model_scores.loc['WT']) / model_scores.std(axis=0)
    else:
        model_scores_standardized = (model_scores - model_scores.mean(axis=0)) / model_scores.std(axis=0)

    data = pd.concat([model_scores_standardized.set_index(dataset.index), dataset.specificity_category], axis=1).dropna()

    for i in range(len(model_names)):

        plot_boxplot(data, model_names[i], ax[i], palette=default_palette, hue_order=default_hue_order)

        #plot_boxplot(data, model_names[i], ax[i], palette=default_palette, hue_order=default_hue_order)
        if standardize_to_wt:
            ax[i].axhline(0, ls='-', c='k', lw=1)

    ax[0].set_ylabel("Standardized model score")
    return fig, ax

def hexbin_plot(data, x, y, ax=None, figsize=(5.5,5), cmap='cividis', log_hue=True, vmin=1, vmax=100, cbar_shrink=0.5, **kwargs):
    
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    
    if log_hue:
        kwargs['norm'] = LogNorm(vmin=vmin, vmax=vmax)
    
    hb = ax.hexbin(data[x], data[y], cmap=cmap, **kwargs)
    plt.colorbar(hb, shrink=cbar_shrink)
    
    return ax, hb

color_key = {'conservation': 'darkgray',
            'alignment_covariation':'#8da0cb',
                'plm':'#a6d854',
                'inverse_folding':'#fc8d62',
                'msa_plm':'#66c2a5',
                'structure_sequence':'#ffd92f'}

from sklearn.metrics import roc_auc_score, average_precision_score
from scipy.stats import spearmanr
from matplotlib import cm

model_names = ['Site_independent', "EVmutation", "EVE", "GEMME", "ESM1v", "ESM2", "Progen2", "Tranception_no_retrieval", "MSA_Transformer", "PoET", "ProteinMPNN", "ESM-IF1", "SaProt_650M_AF2", "ESCOTT"]

model_classification = {
    'Site_independent': 'conservation',
    "EVmutation": 'alignment_covariation',
    "EVE": 'alignment_covariation',
    "GEMME":'alignment_covariation',
    "ESM1v": 'plm',
    "ESM2": 'plm',
    "Progen2": 'plm',
    "Tranception_no_retrieval": 'plm',
    "MSA_Transformer": 'msa_plm',
    "PoET": 'msa_plm',
    "ProteinMPNN": 'inverse_folding',
    "ESM-IF1": 'inverse_folding',
    "SaProt_650M_AF2": 'structure_sequence',
    'ESCOTT': 'structure_sequence'
}

models = model_classification.keys()

def model_classification_plot(dataset, protein, good_label="native-specificity",
                              bad_label="inactive",
                              native_ligand="DMS_score",
                              x="AUC", ax=None, figsize=(4,4),
                              auc_xlim=(0.6, 1),
                              filter_to_subs=1,
                              reverse_EVE=True,
                              ymax=1.45,
                              ms=80):
    
    data = dataset[protein]

    if filter_to_subs:
        data = data.loc[(data.n_subs==filter_to_subs)|(data.n_subs==0)]
    
    if ax is None:
        fig, ax = plt.subplots(1,1, figsize=figsize)
    
    scores = []; colors = []
    for i,model in enumerate(model_names):
        
        if model in data.columns:
            spec_change = selector(data, {'specificity_category': "altered-specificity"})[model]
            no_spec_change = selector(data, {'specificity_category': good_label})[model]
            low_abundance = selector(data, {'specificity_category': bad_label})[model]
            
            data_nsc = data[np.isin(data.specificity_category, [good_label, bad_label])][["specificity_category", model]].dropna()
            
            data_copy = data[[model, native_ligand]].dropna(thresh=2)
            
            wt_spearman = spearmanr(data_copy[model], data_copy[native_ligand])[0]
            
            try:
                auc = roc_auc_score(data_nsc.specificity_category==good_label, data_nsc[model])
                
                if auc > 0.6:
                    scale = np.nanmean(no_spec_change) - np.nanmean(low_abundance)
                    specificity_score = (np.nanmean(spec_change) - np.nanmean(low_abundance)) / scale

                else:
                    specificity_score = np.nan
            
                color = color_key[model_classification[model]]
                scores.append([model, auc, specificity_score, wt_spearman, color])
                
            except ValueError:
                print(data_nsc)
                print(f"Error with model scores for {model}")
            

        else:
            print(f"No model scores for {model}")
        
    X = pd.DataFrame(scores, columns=["model", "AUC", "specificity_score", "wt_spearman", "color"]).set_index("model").sort_values("specificity_score", ascending=False)

    ax.scatter(data=X, x=x, y="specificity_score", ec='k', s=ms, c=X["color"].values)

    ax.set_ylim(0, ymax)
    
    if x=="AUC":
        ax.set_xlim(auc_xlim[0], auc_xlim[1])
    elif x=="wt_spearman":
        ax.set_xlabel("Spearman correlation with wild-type fitness")
        ax.set_xlim(0.23, 0.65)

    ax.axhline(1, c='k', ls='dashed')
    
    return X




### DESIGN PLOTS ###


def hexbin_plot(data, x, y, ax=None, figsize=(5.5,5), cmap='cividis', log_hue=True, vmin=1, vmax=100, cbar_shrink=0.5, **kwargs):
    
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    
    if log_hue:
        kwargs['norm'] = LogNorm(vmin=vmin, vmax=vmax)
    
    hb = ax.hexbin(data[x], data[y], cmap=cmap, **kwargs)
    plt.colorbar(hb, shrink=cbar_shrink)
    
    return ax, hb

import numpy as np
from scipy.optimize import minimize
from scipy.special import expit  # logistic sigmoid
from sklearn.metrics import roc_auc_score, average_precision_score
import pandas as pd

class MultiDatasetAlphaOptimizer:
    """
    Learns optimal alpha for combining two scores across multiple datasets.
    
    For each dataset, fits: P(y=1) = sigmoid(β₀ + β₁ * (score₁ + α * score₂))
    Optimizes α to minimize average loss across datasets.
    """
    
    def __init__(self, balance_classes=True, regularization=0.01):
        """
        Parameters:
        -----------
        balance_classes : bool
            If True, weight samples to balance classes within each dataset
        regularization : float
            L2 regularization strength on alpha (to prevent extreme values)
        """
        self.balance_classes = balance_classes
        self.regularization = regularization
        self.alpha_opt = None
        self.dataset_params = {}
        
    def _get_sample_weights(self, y):
        """Compute sample weights to balance classes"""
        if not self.balance_classes:
            return np.ones(len(y))
        
        n_pos = np.sum(y)
        n_neg = len(y) - n_pos
        
        # Weight so that total weight of pos = total weight of neg
        weights = np.where(y == 1, 
                          1.0 / (2 * n_pos) if n_pos > 0 else 0,
                          1.0 / (2 * n_neg) if n_neg > 0 else 0)
        return weights * len(y)  # Scale back to same order of magnitude
    
    def _fit_logistic_for_dataset(self, combined_scores, y, weights):
        """Fit logistic regression params (β₀, β₁) for given combined scores"""
        
        def neg_log_likelihood(params):
            beta0, beta1 = params
            logits = beta0 + beta1 * combined_scores
            probs = expit(logits)
            
            # Avoid log(0)
            probs = np.clip(probs, 1e-15, 1 - 1e-15)
            
            # Weighted negative log likelihood
            nll = -np.sum(weights * (y * np.log(probs) + (1 - y) * np.log(1 - probs)))
            return nll
        
        # Initialize with simple estimates
        init_params = [0.0, 1.0]
        result = minimize(neg_log_likelihood, init_params, method='BFGS')
        
        return result.x  # Returns [β₀, β₁]
    
    def _compute_loss_for_alpha(self, alpha, datasets):
        """
        Compute average loss across all datasets for a given alpha
        
        Parameters:
        -----------
        alpha : float
            Weight for score_2
        datasets : list of dict
            Each dict has keys: 'score_1', 'score_2', 'y' (all numpy arrays)
        """
        total_loss = 0.0
        
        for dataset in datasets:
            score_1 = dataset['score_1']
            score_2 = dataset['score_2']
            y = dataset['y']
            
            # Compute combined scores
            combined_scores = score_1 + alpha * score_2
            
            # Get sample weights for class balancing
            weights = self._get_sample_weights(y)
            
            # Fit logistic regression for this dataset
            beta0, beta1 = self._fit_logistic_for_dataset(combined_scores, y, weights)
            
            # Compute loss
            logits = beta0 + beta1 * combined_scores
            probs = expit(logits)
            probs = np.clip(probs, 1e-15, 1 - 1e-15)
            
            nll = -np.sum(weights * (y * np.log(probs) + (1 - y) * np.log(1 - probs)))
            
            # Normalize by sum of weights so each dataset contributes equally
            total_loss += nll / np.sum(weights)
        
        # Average across datasets
        avg_loss = total_loss / len(datasets)
        
        # Add L2 regularization on alpha
        avg_loss += self.regularization * alpha**2
        
        return avg_loss
    
    def fit(self, datasets, alpha_init=0.0, alpha_bounds=(-10, 10)):
        """
        Find optimal alpha across datasets
        
        Parameters:
        -----------
        datasets : list of dict
            Each dict has keys: 'score_1', 'score_2', 'y' (all numpy arrays)
        alpha_init : float
            Initial value for alpha
        alpha_bounds : tuple
            (min, max) bounds for alpha
        """
        # Optimize alpha
        result = minimize(
            lambda a: self._compute_loss_for_alpha(a, datasets),
            x0=[alpha_init],
            method='L-BFGS-B',
            bounds=[alpha_bounds]
        )
        
        self.alpha_opt = result.x[0]
        
        # Fit final logistic regression params for each dataset
        for i, dataset in enumerate(datasets):
            score_1 = dataset['score_1']
            score_2 = dataset['score_2']
            y = dataset['y']
            
            combined_scores = score_1 + self.alpha_opt * score_2
            weights = self._get_sample_weights(y)
            
            beta0, beta1 = self._fit_logistic_for_dataset(combined_scores, y, weights)
            self.dataset_params[i] = {'beta0': beta0, 'beta1': beta1}
        
        return self
    
    def predict_proba(self, dataset_idx, score_1, score_2):
        """
        Predict probabilities for a specific dataset
        
        Parameters:
        -----------
        dataset_idx : int
            Index of the dataset (for selecting appropriate logistic params)
        score_1, score_2 : array-like
            Model scores
        """
        if self.alpha_opt is None:
            raise ValueError("Model not fitted yet. Call fit() first.")
        
        combined_scores = score_1 + self.alpha_opt * score_2
        params = self.dataset_params[dataset_idx]
        logits = params['beta0'] + params['beta1'] * combined_scores
        
        return expit(logits)
    
    def evaluate(self, datasets):
        """
        Evaluate performance on datasets
        
        Returns dict with metrics for each dataset
        """
        results = {}
        
        for i, dataset in enumerate(datasets):
            y_true = dataset['y']
            y_pred_proba = self.predict_proba(i, dataset['score_1'], dataset['score_2'])
            
            results[f'dataset_{i}'] = {
                'auc_roc': roc_auc_score(y_true, y_pred_proba),
                'auc_pr': average_precision_score(y_true, y_pred_proba),
                'n_samples': len(y_true),
                'n_positive': np.sum(y_true),
                'frac_positive': np.mean(y_true)
            }
        
        return results
    
def fit_weighted_ensemble(all_scores, model_1, model_2, proteins):
    datasets = [get_dataset(all_scores, prot, model_1, model_2) for prot, dataset in all_scores.items() if prot in proteins]

    optimizer = MultiDatasetAlphaOptimizer(balance_classes=True, regularization=0.01)
    optimizer.fit(datasets, alpha_init=0.0)
    
    return optimizer.alpha_opt

def enrichment_curve(X, log_p=True, log_auc=False, n_steps=25, plot=True, ax=None, figsize=(5,5), **kwargs):
    
    '''Calculate an enrichment curve.'''
    
    X = X.copy().sort_values('score', ascending=False).reset_in# The above code is a Python comment.
    # Comments in Python start with a hash
    # symbol (#) and are used to provide
    # explanations or notes within the
    # code. Comments are ignored by the
    # Python interpreter and are not
    # executed as part of the program.
    dex(drop=True)
    
    aucs = {}
    if log_p:
        p_vals = [i for i in np.logspace(-2, 0, n_steps)]
    else:
        p_vals = [i for i in range(0, 1, n_steps)]

    n_vals = np.array([int(p*len(X)) for p in p_vals])

    curve = np.array([np.sum(X.iloc[:n].y) / (np.mean(X.y) * n) for n in n_vals])
    l_5 = X.iloc[:int(0.05*len(X))].y.sum() / (np.mean(X.y) * int(0.05*len(X)))

    if plot:
        if ax is None:
            plt.figure(figsize=(4,5))
            ax = plt.gca()
        # if c is None:
        #     ax.plot(n_vals, curve, **kwargs)
        # else:
        ax.plot(p_vals, curve, **kwargs)
    
    audc = np.trapz(curve, p_vals) / np.trapz([1]*len(curve), p_vals)
    
    return curve, p_vals, l_5, audc

def get_dataset(all_scores, prot, model_1, model_2=None, singles_only=True, doubles_only=False, target_category='altered-specificity'):
    
    dataset = all_scores[prot].copy()
    
    if singles_only:
        dataset = dataset.loc[dataset.n_subs==1]
    elif doubles_only:
        dataset = dataset.loc[dataset.n_subs==2]
        
    if target_category=='altered-specificity':
        dataset['y'] = dataset['specificity_category']=='altered-specificity'
    elif target_category=='any-functional':
        dataset['y'] = dataset['specificity_category'].isin(['altered-specificity', 'native-specificity'])
        
    if model_2 is None:
        dataset = dataset[[model_1, 'y']].dropna()
        return {
            'score_1': dataset[model_1].values,
            'y': dataset['y'].values
        }
    else:
        dataset = dataset[[model_1, model_2, 'y']].dropna()
        return {
            'score_1': dataset[model_1].values,
            'score_2': dataset[model_2].values,
            'y': dataset['y'].values
        }