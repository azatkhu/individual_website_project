import pandas as pd 


def get_dataframe(path: str = "data/supermarket_large_dataset.csv"):
    df = pd.read_csv(path)
    
    return df
