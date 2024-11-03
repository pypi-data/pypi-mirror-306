
import numpy as np
import pandas as pd
from scipy.stats import norm
from scipy.special import gammaln, psi, factorial
from scipy.optimize import fmin_l_bfgs_b as optim
from statsmodels.genmod.generalized_linear_model import GLM
from statsmodels.genmod.families import NegativeBinomial

from pydgea.prework import obtain_contrast_vec


def fit_glm(counts, design_matrix) :
    
    """
    Parameters
    ----------
    counts : pandas.Series
        Raw counts for a given gene.
    
    design_matrix : pandas.DataFrame
        Design matrix.
    
    Returns
    -------
    statsmodels.GLMResultsWrapper
    """
    
    exog = design_matrix.copy()
    endog = counts.copy()
        
    model = GLM(endog=endog, exog=exog, family=NegativeBinomial())
    res = model.fit()
        
    return res


## Fit negative binomial distribution with the maximum likelihood estimation. 

def ll_nbinom(params, data):
    
    """
    Parameters
    ----------
    params : list 
        List of the form ``[r, p]``.
        r : float greater than or equal to 0. The number of success. 
        p : float between 0 and 1. The probability of a single success.
    
    data : numpy.ndarray
        Observed data.
        
    Returns
    -------
    float
        Negative log likelihood of fitted negative binomial model.
    """
    
    infinitesimal = np.finfo(float).eps
    
    r, p = params 
    if r < 0 :
        raise ValueError('number of success must be positive or 0')
    elif p < 0 or p > 1 :
        raise ValueError('success probability must be between 0 and 1')
    
    # Refer http://en.wikipedia.org/wiki/Negative_binomial_distribution#Maximum_likelihood_estimation
    N = len(data)
    ll = np.sum(gammaln(data + r)) \
        - np.sum(np.log(factorial(data))) \
        - N*(gammaln(r)) \
        + N*r*np.log(p) \
        + np.sum(data*np.log(1-(p if p < 1 else 1-infinitesimal)))

    return -ll


def ll_nbinom_deriv(params, data) :
    
    """
    Parameters
    ----------
    params : list 
        List of the form ``[r, p]``.
        r : float greater than or equal to 0. The number of success. 
        p : float between 0 and 1. The probability of a single success.
    
    data : numpy.ndarray
        Observed data.
        
    Returns
    -------
    numpy.ndarray
        First element is a partial derivative value of log likelihood with respect to r. 
        Second element is a partial derivative value with respect to p.
    """
    
    infinitesimal = np.finfo(float).eps
    
    r, p = params 
    if r < 0 :
        raise ValueError('number of success must be positive or 0')
    elif p < 0 or p > 1 :
        raise ValueError('success probability must be between 0 and 1')

    # Refer http://en.wikipedia.org/wiki/Negative_binomial_distribution#Maximum_likelihood_estimation
    N = len(data)
    pderiv = (N*r)/p - np.sum(data)/(1-(p if p < 1 else 1-infinitesimal))
    rderiv = np.sum(psi(data + r)) \
            - N*psi(r) \
            + N*np.log(p)

    return np.array([rderiv, pderiv])


def obtain_mu(counts, design_matrix, size_factors) :
    
    """
    Parameters
    ----------
    counts : pandas.Series
        Raw counts for a given gene.
    
    design_matrix : pandas.DataFrame
        Design matrix.
    
    size_factors : pandas.Series
        Normalization factors.
        
    Returns
    -------
    pandas.Series
        Mean estimates for a given gene.
    """
    
    glm = fit_glm(counts/size_factors, design_matrix)
    
    mu = np.exp(design_matrix @ glm.params)
    mu = mu * size_factors
    
    return mu
    

def fit_mle_nbinom(counts, design_matrix, size_factors, init_alpha) :
    
    """
    Parameters
    ----------
    counts : pandas.Series
        Raw counts for a given gene.
    
    design_matrix : pandas.DataFrame
        Design matrix.
    
    size_factors : pandas.Series
        Normalization factors.
        
    init_alpha : float
        Initial alpha(= 1/r).
        
    Returns
    -------
    float
        Dispersion estimate for a given gene.
    """

    infinitesimal = np.finfo(float).eps
    
    mu = obtain_mu(counts, design_matrix, size_factors)
    mu = mu.values
    design_matrix = design_matrix.values

    def loss(log_alpha: float) -> float:

        alpha = np.exp(log_alpha) 
        r = 1/alpha
        
        nll = 0 
        for i in range(len(counts)) :
            count = counts[i]
            mean = mu[i] 

            p = 1/(1 + mean*alpha)

            nll += ll_nbinom([r,p], np.array([count]))
            
        weight = mu / (1 + mu * alpha)
        reg = 0.5 * np.linalg.slogdet((design_matrix.T * weight) @ design_matrix)[1]

        return nll + reg

    def dloss(log_alpha: float) -> float:

        alpha = np.exp(log_alpha)  
        r = 1/alpha

        ll_deriv = 0
        for i in range(len(counts)) :
            count = counts[i]
            mean = mu[i] 

            p = 1/(1 + mean*alpha)

            ll_deriv += ll_nbinom_deriv([r,p], np.array([count]))[0]
            
        weight = mu / (1 + mu * alpha)
        d_weight = -(weight**2)
        reg_grad = (0.5 * (np.linalg.inv((design_matrix.T * weight) @ design_matrix)
                * ((design_matrix.T * d_weight) @ design_matrix)).sum()) * alpha

        return alpha * ll_deriv + reg_grad

    min_disp = infinitesimal
    max_disp = 1e+10
    optimres = optim(loss,
                    x0=np.log(init_alpha),
                    fprime=dloss,
                    approx_grad=1,
                    bounds=[(np.log(min_disp), np.log(max_disp))])
    
    return np.exp(optimres[0][0])
    

## Estimate dispersion.

def estimate_dispersions(count_data, design_matrix, size_factors) : 
    
    """
    Parameters
    ----------
    count_data : pandas.DataFrame
        Raw counts.
    
    design_matrix : pandas.DataFrame
        Design matrix.
    
    size_factors : pandas.Series
        Normalization factors.
        
    Returns
    -------
    pandas.DataFrame
        Dispersion estimate for each gene.
    """
    
    genes = count_data.index
    
    disps = pd.DataFrame(index=genes, columns=['dispersion'])
    for gene in genes :
        counts = count_data.loc[gene,:]
        
        mean = np.mean(counts)
        var = np.var(counts)
        init_r = (mean**2)/((var - mean) if var > mean else 10)
        
        init_alpha = 1/init_r
        alpha = fit_mle_nbinom(counts, design_matrix, size_factors, init_alpha)
        disps.loc[gene, 'dispersion'] = alpha
        
    return disps


## Estimate log2 fold change.

def estimate_lfcs(count_data, design_matrix, size_factors) :
    
    """
    Parameters
    ----------
    count_data : pandas.DataFrame
        Raw counts.
    
    design_matrix : pandas.DataFrame
        Design matrix.
    
    size_factors : pandas.Series
        Normalization factors.
        
    Returns
    -------
    pandas.DataFrame
        Log2 fold change estimates for each gene.
    """
    
    genes = count_data.index
    
    levels = design_matrix.columns
    lfcs = pd.DataFrame(index=genes, columns=levels) 
    for gene in genes : 
        counts = count_data.loc[gene,:]
        
        glm = fit_glm(counts/size_factors, design_matrix)
        lfc = glm.params
        
        lfcs.loc[gene,levels] = lfc[levels]
        
    return lfcs
        

def obtain_lfc(lfcs, contrast, design_matrix) : 
    
    """
    Parameters
    ----------
    lfcs : pandas.DataFrame
        Log2 fold change estimates for each gene.
        
    contrast : list
        List of the form ``[factor of interest, treat, control]``.
        
    design_matrix : pandas.DataFrame
        Design matrix.
        
    Returns
    -------
    pandas.DataFrame
        Log2 fold change estimates between control and treat.
    """

    contrast = obtain_contrast_vec(contrast, design_matrix)
    
    lfc = (lfcs @ contrast).astype('float64')
    lfc = lfc/np.log(2)
    lfc = lfc.to_frame(name='lfc')
    
    return lfc


# Wald test

def wald_test(count_data, design_matrix, size_factors, disps, lfcs, contrast) :
    
    """
    Parameters
    ----------
    count_data : pandas.DataFrame
        Raw counts.
    
    design_matrix : pandas.DataFrame
        Design matrix.
    
    size_factors : pandas.Series
        Normalization factors. 
    
    disps : pandas.DataFrame
        Dispersion estimate for each gene.
    
    lfcs : pandas.DataFrame
        Log2 fold change estimates for each gene.
    
    contrast : list
        List of the form ``[factor of interest, treat, control]``.
        
    Returns
    -------
    pandas.DataFrame
        Estimated p-value for each gene.
    """
    
    genes = count_data.index
    
    contrast = obtain_contrast_vec(contrast, design_matrix)
    
    num_levs = design_matrix.shape[1]
    ridge_factor = np.diag(np.repeat(1e-6, num_levs))
    
    mu = np.exp((design_matrix @ lfcs.T).astype('float64')).T
    mu = mu * size_factors
    weight = mu / (1 + mu.T * disps['dispersion']).T
    
    p_values = pd.DataFrame(index=genes, columns=['pvalue'])
    for gene in genes :
        hessian = (design_matrix.T * weight.loc[gene, :]) @ design_matrix
        cov = np.linalg.inv(hessian.values.astype('float64') + ridge_factor)
        cov = cov @ contrast

        wald_se = np.sqrt(cov.T @ hessian @ cov)
        wald_statistic = contrast @ lfcs.loc[gene, :] / wald_se
        wald_p_value = 2 * norm.sf(np.abs(wald_statistic))

        p_values.loc[gene, 'pvalue'] = wald_p_value
        
    return p_values 

