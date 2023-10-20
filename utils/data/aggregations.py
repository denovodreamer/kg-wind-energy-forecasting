
import pandas as pd


def per_hour(df, variable, agg_function, timestamp="read_at"):
    df = df[[timestamp, variable]].copy()

    df["year"] = df[timestamp].dt.year
    df["month"] = df[timestamp].dt.month
    df["day"] = df[timestamp].dt.day
    df["hour"] = df[timestamp].dt.hour

    if agg_function == "first":
        df_agg = df.groupby(["year", "month", "day", "hour"]).first()
    elif agg_function == "mean":
        df_agg = df.groupby(["year", "month", "day", "hour"]).mean()
    elif agg_function == "sum":
        df_agg = df.groupby(["year", "month", "day", "hour"]).sum()
    else:
        df_agg = df.groupby(["year", "month", "day", "hour"]).agg(agg_function)

    df_agg.reset_index(drop=False, inplace=True)

    df_agg[timestamp] = pd.to_datetime(df_agg[["year", "month", "day", "hour"]])
    df_agg.drop(["year", "month", "day", "hour"], axis=1, inplace=True)

    df_agg = df_agg[[timestamp, variable]].copy()

    return df_agg


def per_day(df, variable, agg_function, timestamp="read_at"):
    df = df[[timestamp, variable]].copy()

    df["year"] = df[timestamp].dt.year
    df["month"] = df[timestamp].dt.month
    df["day"] = df[timestamp].dt.day

    if agg_function == "mean":
        df_agg = df.groupby(["year", "month", "day"]).mean()
    elif agg_function == "sum":
        df_agg = df.groupby(["year", "month", "day"]).sum()
    else:
        df_agg = df.groupby(["year", "month", "day"]).agg(agg_function)

    df_agg.reset_index(drop=False, inplace=True)

    df_agg[timestamp] = pd.to_datetime(df_agg[["year", "month", "day"]])
    df_agg.drop(["year", "month", "day"], axis=1, inplace=True)

    df_agg = df_agg[[timestamp, variable]].copy()

    return df_agg


def per_month(df, variable, agg_function, timestamp="read_at"):
    df = df[[timestamp, variable]].copy()

    df["year"] = df[timestamp].dt.year
    df["month"] = df[timestamp].dt.month

    if agg_function == "mean":
        df_agg = df.groupby(["year", "month"]).mean()
    elif agg_function == "sum":
        df_agg = df.groupby(["year", "month"]).sum()
    else:
        df_agg = df.groupby(["year", "month"]).agg(agg_function)

    df_agg.reset_index(drop=False, inplace=True)

    df_agg["day"] = 1
    df_agg[timestamp] = pd.to_datetime(df_agg[["year", "month"]])
    df_agg.drop(["year", "month"], axis=1, inplace=True)

    df_agg = df_agg[[timestamp, variable]].copy()

    return df_agg


def agg_variable(df, variable, agg_function, freq):
    df = df.copy()

    if freq == "hour":
        df_agg = per_hour(df, variable, agg_function, timestamp="read_at")
    elif freq == "day":
        df_agg = per_day(df, variable, agg_function, timestamp="read_at")
    elif freq == "month":
        df_agg = per_month(df, variable, agg_function, timestamp="read_at")

    return df_agg


def agg_variables(df, variables, agg_function, freq):
    from utils.data import wrangling

    df_agg_lst = []
    for variable in variables:
        df_agg = agg_variable(df, variable, agg_function, freq)
        df_agg_lst.append(df_agg)

    df_aggs = wrangling.merge_dataframes(df_agg_lst)

    return df_aggs


# TODO aggregate per farm ?