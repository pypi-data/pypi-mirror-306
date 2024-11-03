
import warnings
import pandas as pd
import numpy as np
from scipy.stats import false_discovery_control as fdc

from pydgea.normalization import cpm, mor
from pydgea.utils import *
from pydgea.prework import *
from pydgea.stats import *


## I referred to the code in the link below :
## https://github.com/owkin/PyDESeq2/tree/main/pydeseq2

class pydgea_dataset :
    
    
    warnings.filterwarnings('ignore')
    
    
    def __init__(self, count_data, metadata, design) :

        """
        Parameters
        ----------
        count_data : pandas.DataFrame
            Raw counts. One row per gene and one column per sample.

        metadata : pandas.DataFrame
            Sample metadata. One row per sample and one column per design factor.

        design : str
            Design formula of the form ``~ x1 + x2 + x3 + x2:x3 +.....+ xn`` where xi is a design factor.
        """
            
        check_count_data(count_data)      
        
        check_metadata(metadata, count_data)           
        
        design_factors = obtain_design_factors(design, metadata)
        design_matrix = obtain_design_matrix(design_factors, metadata)
        
        genes = count_data.index
        samples = metadata.index    
    
        self.count_data = count_data
        self.metadata = metadata
        self.genes = list(genes)
        self.samples = list(samples)
        self.design = design
        self.design_factors = design_factors
        self.design_matrix = design_matrix

        
    def normalization(self, norm_method='mor') :
        
        """
        Parameters
        ----------
        norm_method : str
        
        Returns
        -------
        normalized : pandas.DataFrame
            Normalized counts. One row per gene and one column per sample.

        size_factors : pandas.Series
            Normalization factors.
        """
        
        norm_methods = {'cpm' : cpm, 'mor' : mor}
        
        if norm_method not in norm_methods.keys() :
            raise ValueError("argument 'norm_method' must be 'cpm' or 'mor'")
        else :
            normalized, size_factors = norm_methods[norm_method](self.count_data)
            
        return normalized, size_factors
        
        
    def dgea(self, norm_method='mor') :
        
        normalized, size_factors = self.normalization(norm_method)
        print('Finished estimating size factors.\n')
        
        disps = estimate_dispersions(self.count_data, self.design_matrix, size_factors)
        print('Finished estimating dispersions.\n')
        
        lfcs = estimate_lfcs(self.count_data, self.design_matrix, size_factors)
        print('Finished estimating log2 fold changes.\n')
        
        self.run_dgea = True
        self.normalized = normalized
        self.size_factors = size_factors
        self.disps = disps
        self.lfcs = lfcs
        
        
    def summary(self, contrast) :
        
        """
        Parameters
        ----------
        contrast : list
            List of the form ``[factor of interest, treat, control]``.
            Control and treat must be different, each belonging to the levels of factor of interest.

        Returns
        -------
        pandas.DataFrame
            Summary of statistical analysis.
        """
        
        assert self.run_dgea == True, 'please run the dgea() method first'

        factor, treat, control = contrast[0], contrast[1], contrast[2]
        check_contrast(contrast, self.design_factors, self.metadata)

        # log2 fold change
        lfc = obtain_lfc(self.lfcs, contrast, self.design_matrix)

        # basemean
        basemean = self.normalized.mean(axis = 1)
        basemean = basemean.to_frame(name='basemean')

        # p-value
        print('Finished running wald tests.\n')
        p_values = wald_test(self.count_data, self.design_matrix, self.size_factors, self.disps, self.lfcs, contrast)
        
        # adjusted p-value
        adj_p_values = fdc(list(p_values['pvalue']))
        adj_p_values = pd.DataFrame({'padj' : adj_p_values}, index=p_values.index)

        # result
        self.contrast = contrast
        self.basemean = basemean
        self.pvalue = p_values
        self.padj = adj_p_values
        self.lfc = lfc

        result = pd.concat([self.basemean, self.disps, self.lfc, self.pvalue, self.padj], axis=1)
        self.result = result

        print('Log2 fold change & wald test & p-value : {} {} vs {}\n'.format(factor, treat, control))
        print(result)

        return result

