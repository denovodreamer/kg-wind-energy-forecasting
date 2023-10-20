
from datetime import datetime
import pandas as pd


def to_csv(df, file_path):
    df = df.copy()
    df.to_csv(file_path, sep=";", encoding="utf-8", index=False)


def read_csv(file_path, convert_timestamp=True):
    df = pd.read_csv(file_path, sep=";", encoding="utf-8")
    if convert_timestamp:
        df["read_at"] = pd.to_datetime(df["read_at"])
    return df


def to_db(df, database, table_name):
    df.to_sql(table_name, database.engine, index=False, method="multi", if_exists="append")


def slice(df, variable, min_value, max_value, inclusive="either"):

    if isinstance(min_value, df[variable].dtype.type):
        return

    if isinstance(max_value, df[variable].dtype.type):
        return

    df = df.copy()
    if inclusive == "left":
        df = df[(df[variable] >= min_value) & (df[variable] < max_value)].copy()
    elif inclusive == "right":
        df = df[(df[variable] > min_value) & (df[variable] <= max_value)].copy()
    elif inclusive == "both":
        df = df[(df[variable] >= min_value) & (df[variable] <= max_value)].copy()
    elif inclusive == "neither":
        df = df[(df[variable] > min_value) & (df[variable] < max_value)].copy()

    return df


def slice_dates(df, start_date, end_date, inclusive="either", timestamp="read_at"):
    df = df.copy()

    if isinstance(start_date, str):
        start_date = datetime.fromisoformat(start_date)

    if isinstance(end_date, str):
        end_date = datetime.fromisoformat(end_date)

    df = slice(df, timestamp, start_date, end_date, inclusive)

    return df


def per_variable(df, variable, function, **params):
    df = df.copy()

    cols = df.columns.tolist()

    df_new = pd.DataFrame()
    for variable_id, df_var in df.groupby(variable):
        df_var = function(df_var, **params)
        df_var[variable] = variable_id
        df_new = pd.concat([df_new, df_var], axis=0)

    df_new = df_new[cols].copy()

    return df_new


def fill_time_index(df, freq, fill_value=0, start_date=None, end_date=None, timestamp="read_at"):
    """
    This function fills the missing timestamps with the fill_value provided.
    """
    df = df.copy()

    df[timestamp] = pd.to_datetime(df[timestamp])
    df.sort_values(timestamp, inplace=True)

    if start_date is None and end_date is None:
        start_date = df[timestamp].min()
        end_date = df[timestamp].max()

    full_index = pd.date_range(start_date, end_date, freq=freq, inclusive="left")
    df = df.set_index(timestamp).reindex(full_index)
    df = df.reset_index(drop=False).rename(columns={"index":timestamp})
    df.fillna(value=fill_value, inplace=True)

    df.sort_values(timestamp, inplace=True)

    return df


def fill_time_index_per_variable(df, variable, **params):
    """
    This function fills the missing timestamps with the fill_value provided,
    by segments of a given variable.

    Example:
        kpi_losses = wrangling.fill_time_index_per_variable(
            kpi_losses, variable="event_type_id",
            freq="H", start_date=start_date, end_date=end_date
        )
    """

    df = df.copy()

    f = fill_time_index
    df = per_variable(df, variable, f, **params)

    return df


def pivot_time_series(df, values_var, columns_var, freq, start_date=None, end_date=None, timestamp="read_at", ):
    """
        values_var is the variable to pivot (e.g. power_average)
        columns_var is the group variable (e.g. asset_id)
        index_var is the timestamp (e.g. "reat_at")
        freq is the time granularity (e.g. "10min")
    """

    df = df.copy()

    cols = [
        timestamp,
        columns_var,
        values_var,
    ]

    df = df[cols].copy()

    df[columns_var] = df[columns_var].astype(str)
    df = pd.pivot(df, index=timestamp, columns=columns_var, values=values_var).fillna(0)

    df.reset_index(drop=False, inplace=True)
    df.columns.name = None

    df = fill_time_index(df, freq, fill_value=0, start_date=start_date, end_date=end_date)

    return df



def merge_dataframes(df_lst, timestamp="read_at", how="outer"):
    """
    Merge list of dataframes on the timestamp.
    Outer join to preserve all data.
    """

    from functools import reduce

    df_merged = reduce(
        lambda df_1, df_2:
            pd.merge(df_1, df_2, on=timestamp, how=how),
            df_lst
    )

    return df_merged