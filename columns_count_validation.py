from get_selected_columns import get_selected_columns
from get_html_table import get_html_table


def check_error_return_html_table(df, list_cols):
    tuple_df_error = get_selected_columns(df = df, list_cols=list_cols)

    if tuple_df_error[1] is not None:
        return tuple_df_error

    return (get_html_table(tuple_df_error[0]), None)
