
import numpy as np
import pandas as pd

from pydgea.utils import geometric_mean


# counts per million
def cpm(count_data, log=False) :
    
    """
    Parameters
    ----------
    count_data : pandas.DataFrame
        Raw counts.
        
    log : bool
    
    Returns
    -------
    normalized : pandas.DataFrame
        Normalized counts. 

    size_factors : pandas.Series
        Normalization factors.
    """

    normalized = count_data.copy()
    
    size_factors = normalized.sum()/10**6
    normalized /= size_factors
    
    if log == True :
        normalized[normalized == 0] = 1e-3
        normalized = np.log(normalized)

    return normalized, size_factors


# median of ratios
def mor(count_data, log = False) :
    
    """
    Parameters
    ----------
    count_data : pandas.DataFrame
        Raw counts.
        
    log : bool
    
    Returns
    -------
    normalized : pandas.DataFrame
        Normalized counts. 

    size_factors : pandas.Series
        Normalization factors.
    """
    
    normalized = count_data.copy()
    
    genes = normalized.index  
    reference = pd.Series([geometric_mean(normalized.loc[gene,:]) for gene in genes], index=genes)
    filtered_genes = genes[reference != 0]
    
    ratios = normalized.loc[filtered_genes,:].T/reference[filtered_genes]
    ratios = ratios.T

    size_factors = ratios.median()
    normalized /= size_factors
    
    if log == True :
        normalized[normalized == 0] = 1e-3
        normalized = np.log(normalized)

    return normalized, size_factors

