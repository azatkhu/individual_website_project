import pandas as pd


def get_html_table(df: pd.DataFrame):

    table_df = df.to_html(index = False, classes="table")

    return table_df
    