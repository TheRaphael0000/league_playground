import pandas as pd
import numpy as np

def compute_ppmi(df):
    """
    thx gemini
    https://en.wikipedia.org/wiki/Pointwise_mutual_information
    """

    # 1. Total sum of all co-occurrences
    total_sum = df.values.sum()
    
    # 2. Sum of rows and columns (Marginals)
    row_sums = df.sum(axis=1).values
    col_sums = df.sum(axis=0).values
    
    # 3. Calculate Expected frequencies: (row_sum * col_sum) / total_sum
    # We use outer product to get a matrix of expected values
    expected = np.outer(row_sums, col_sums) / total_sum
    
    # 4. Calculate PMI: log2(Actual / Expected)
    # Using np.errstate to ignore division by zero/log of zero warnings
    with np.errstate(divide='ignore', invalid='ignore'):
        pmi = np.log2(df.values / expected)
    
    # 5. Convert to PPMI (Positive PMI)
    ppmi = np.maximum(0, pmi)
    
    # Clean up NaNs/Infs resulting from 0 counts
    ppmi = np.nan_to_num(ppmi)
    
    return pd.DataFrame(ppmi, index=df.index, columns=df.columns)