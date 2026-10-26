import pandas as pd


def get_selected_columns(df: pd.DataFrame, list_cols: list[str] = []):

    if len(list_cols) > 20:
        error = "Выбери до 20 столбцов включительно"
        new_df_with_ten_rows_cols = None

    else:
        new_df_with_ten_rows_cols = df[list_cols].iloc[:10]
        error = None

    return (new_df_with_ten_rows_cols, error)
