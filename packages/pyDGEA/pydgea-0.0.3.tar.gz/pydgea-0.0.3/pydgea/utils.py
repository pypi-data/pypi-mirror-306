
import pandas as pd
import numpy as np


## Perform various operations on sequence data.

def dedupe(arr) :

    """
    Parameters
    ----------
    arr : sequence
    
    Returns
    -------
    list
    """
    
    deduped = []
    for elt in arr :
        if elt not in deduped :
            deduped.append(elt)

    return deduped


def remove_all(arr, target_elt) : 
    
    """
    Parameters
    ----------
    arr : sequence
    
    Returns
    -------
    list
    """
    
    removed = []
    for elt in arr :
        if elt != target_elt :
            removed.append(elt)
        
    return removed


def replace_all(arr, from_elt, to_elt) :
    
    """
    Parameters
    ----------
    arr : sequence
    
    Returns
    -------
    list
    """
    
    replaced = []
    for elt in arr :
        if elt == from_elt :
            replaced.append(to_elt)
        else :
            replaced.append(elt)
        
    return replaced


def multiply_all(arr) :
    
    """
    Parameters
    ----------
    arr : sequence
    
    Returns
    -------
    float
    """
    
    result = 1
    for elt in arr :
        result *= elt
        
    return result


def combine_all(arrs) :
    
    """
    Parameters
    ----------
    arrs : sequence
        Every element must be a sequence.
    
    Returns
    -------
    list
    """
    
    combined = []
    for arr in arrs :
        for elt in arr :
            combined.append(elt)
        
    return combined


def arr_sub(arr1, arr2) :
    
    """
    Parameters
    ----------
    arr1 : sequence
    
    arr2 : sequence
    
    Returns
    -------
    list
    """
    
    subed = []
    for elt in arr1 :
        if elt not in arr2 :
            subed.append(elt)
    
    return subed


def arr_add(arr1, arr2) :
    
    """
    Parameters
    ----------
    arr1 : sequence
    
    arr2 : sequence
    
    Returns
    -------
    list
    """
    
    added = [elt for elt in arr1]
    for elt in arr2 :
        if elt not in added :
            added.append(elt)
        
    return added


def geometric_mean(arr) :
    
    """
    Parameters
    ----------
    arr : sequence
    
    Returns
    -------
    float
    """
    
    n = len(arr)
    
    result = multiply_all(arr)
    result = result**(1/n)
    
    return result
    
