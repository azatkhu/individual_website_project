import pandas as pd


def check_size(df):
    
    return df.shape

def get_columns(df):

    result = []
    for i, col in enumerate(df.columns):
        result.append({
            "index": i,
            "column": col, 
            "dtype": df[col].dtype,
            }
        )
    
    return result