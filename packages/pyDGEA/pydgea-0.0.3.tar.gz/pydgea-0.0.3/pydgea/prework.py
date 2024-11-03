
import pandas as pd
import numpy as np
import itertools
import statsmodels.api as sm

from pydgea.utils import dedupe, remove_all, combine_all


## I referred to the code in the link below :
## https://github.com/owkin/PyDESeq2/blob/main/pydeseq2/utils.py

def check_count_data(count_data) :
    
    """
    Parameters
    ----------
    count_data : pandas.DataFrame
        Raw counts.
    """
    
    if isinstance(count_data, pd.DataFrame) :  
        if count_data.isna().any().any() :
            raise ValueError("missing values are not allowed")  
        elif not set(count_data.dtypes) <= {np.dtype('int64'), np.dtype('float64')} :
            raise ValueError("only numbers are allowed")
        elif len(set(count_data.columns)) != len(count_data.columns) :
            raise ValueError('same column names are not allowed')
        elif len(set(count_data.index)) != len(count_data.index) :
            raise ValueError('same row names are not allowed')
    else :
        raise ValueError("argument 'count_data' must be pandas.DataFrame")
    
    if ((count_data % 1 != 0).any() | (count_data < 0).any()).any() :
        raise ValueError("only positive integers(or 0) are alllowed")   
    elif (count_data.sum(axis=0) == 0).any() or (count_data.sum(axis=1) == 0).any() :
        raise ValueError('there is a row or column whose sum is 0')


# after check_count_data
def check_metadata(metadata, count_data) :
    
    """
    Parameters
    ----------
    metadata : pandas.DataFrame
        Sample metadata.
    
    count_data : pandas.DataFrame
        Raw counts.
    """
    
    if isinstance(metadata, pd.DataFrame) : 
        if metadata.isna().any().any() :
            raise ValueError("missing values are not allowed")
        elif len(set(metadata.columns)) != len(metadata.columns) :
            raise ValueError('same column names are not allowed')
        elif len(set(metadata.index)) != len(metadata.index) :
            raise ValueError('same row names are not allowed')
        elif set(metadata.index) != set(count_data.columns) :
            raise ValueError("samples in the argument 'metadata' and the argument 'count_data' must be the same")
    else :
        raise ValueError("argument 'metadata' must be pandas.DataFrame")
        
    for colname in metadata.columns :
        if '~' in colname or '+' in colname or ':' in colname :
            raise ValueError("any column name of argument 'metadata' must not contain '~', '+', ':'")


# after check_metadata
def obtain_design_factors(design, metadata) :
    
    """
    Parameters
    ----------
    design : str
        Design formula.
    
    metadata : pandas.DataFrame
        Sample metadata.
        
    Returns
    -------
    list
        Column names of metadata to be used as design factors.
    """
    
    assert design.strip().startswith('~'), 'design formula must start with tilde(~)'
    
    table = design.maketrans({'~' : ' ', '+' : ' '})
    design_factors = design.translate(table).split(' ')
    design_factors = remove_all(design_factors, '')
    
    if design_factors == [] : 
        raise ValueError('no design factors')
        
    for i in range(len(design_factors)) :
        factor = design_factors[i]
        if ':' in factor :
            inter = factor.split(':')
            inter = [factor.strip() for factor in inter]
            design_factors[i] = tuple(inter)
            if len(inter) != 2 or len(set(inter)) != 2 :
                raise ValueError('interaction term must contain only two different factors')

    if len(dedupe(design_factors)) != len(design_factors) :
        raise ValueError('same design terms are not allowed')
        
    for factor in design_factors :
        if type(factor) == tuple :
            inter = factor
            factor1, factor2 = inter
            if (factor2, factor1) in design_factors :
                raise ValueError('same design terms are not allowed')
            elif factor1 not in design_factors or factor2 not in design_factors :
                raise ValueError('every factor with interaction must be a design factor')
        else :
            if factor not in metadata.columns :
                raise ValueError("every design factor must belong to the columns of argument 'metadata'")
    
    return design_factors


# after obtain_design_factors
def obtain_design_matrix(design_factors, metadata) :
    
    """
    Parameters
    ----------
    design_factors : list
        Design factors.
    
    metadata : pandas.DataFrame
        Sample metadata.
        
    Returns
    -------
    pandas.DataFrame
        Dataframe with experiment design informatiion. 
    """
           
    total =[]
    inters = []
    for factor in design_factors :
        if type(factor) == tuple :
            inters.append(factor)
        else :
            total.append(factor)

    non_inters = total
    for factor in dedupe(combine_all(inters)) :
        non_inters = remove_all(non_inters, factor)
    
    design_matrix = metadata[non_inters]
    design_matrix = pd.get_dummies(design_matrix, dtype='int', drop_first=True)
    
    if inters != [] :
        for inter in inters :
            factor1, factor2 = inter 
            dm_factor1 = pd.get_dummies(metadata[factor1], dtype='int', drop_first=True)
            dm_factor2 = pd.get_dummies(metadata[factor2], dtype='int', drop_first=True)
            dm_inter = pd.DataFrame(index = dm_factor1.index)
            for level1, level2 in itertools.product(dm_factor1.columns, dm_factor2.columns) :
                dm_inter['{}_{}_and_{}_{}'.format(factor1, level1, factor2, level2)] = dm_factor1[level1] * dm_factor2[level2]
            dm_inter = pd.concat([dm_factor1, dm_factor2, dm_inter], axis=1)
            design_matrix = pd.concat([design_matrix, dm_inter], axis=1)
            
    design_matrix = sm.add_constant(design_matrix)
    design_matrix.columns.values[0] = 'intercept'
    
    return design_matrix


def check_contrast(contrast, design_factors, metadata) :
    
    """
    Parameters
    ----------
    contrast : list
        List of the form ``[factor of interest, treat, control]``.
    
    design_factors : list
        Design factors.
    
    metadata : pandas.DataFrame
        Sample metadata.
    """
    
    assert type(contrast) == list, "argument 'contrast' must be list"

    if len(contrast) != 3 :
        raise ValueError("argument 'contrast' must be length of 3")
    else :
        factor, treat, control = contrast[0], contrast[1], contrast[2]   
        
    levels = dedupe(metadata[factor])
    
    if control == treat :
        raise ValueError("argument 'control' and 'treat' must be different")
    elif control not in levels or treat not in levels :
        raise ValueError("argument 'control' and 'treat' must belong to the levels of factor of interest.")
        

# after check_contrast
def obtain_contrast_vec(contrast, design_matrix) : 
    
    """
    Parameters
    ----------
    contrast : list
        List of the form ``[factor of interest, treat, control]``.
    
    design_matrix : pandas.DataFrame
        Design matrix.
        
    Returns
    -------
    numpy.ndarray
        Vector encoding the argument ``contrast``.
    """
    
    factor, treat, control = contrast[0], contrast[1], contrast[2]   
    
    design_levels = design_matrix.columns
    contrast_vec = pd.Series(0, index=design_levels)
    
    control_level = '{}_{}'.format(factor, control)
    treat_level = '{}_{}'.format(factor, treat)
    if control_level in design_levels and treat_level not in design_levels :
        contrast_vec['{}_{}'.format(factor, control)] = -1
    elif treat_level in design_levels and control_level not in design_levels :
        contrast_vec['{}_{}'.format(factor, treat)] = -1
    elif control_level in design_levels and treat_level in design_levels :
        contrast_vec['{}_{}'.format(factor, control)] = -1
        contrast_vec['{}_{}'.format(factor, treat)] = 1
    else :
        raise ValueError("invalid argument 'contrast'")
    
    return np.array(contrast_vec)

