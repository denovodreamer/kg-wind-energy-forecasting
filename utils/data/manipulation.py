
from pandas.api.types import is_numeric_dtype

def min_max_scale(df):
    df_min_max_scaled = df.copy()

    for column in df_min_max_scaled.columns:
        if not is_numeric_dtype(df_min_max_scaled[column]):
            continue
        df_min_max_scaled[column] = (
            df_min_max_scaled[column] - df_min_max_scaled[column].min()
            ) / (df_min_max_scaled[column].max() - df_min_max_scaled[column].min())

    return df_min_max_scaled