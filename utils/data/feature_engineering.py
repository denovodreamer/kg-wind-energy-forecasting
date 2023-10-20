
import numpy as np


def calendar_variables(df):
    df = df.copy()

    features = df.columns.tolist()
    features.remove("read_at")

    df["hour"] = (df["read_at"].dt.hour + df["read_at"].dt.minute / 60).round(2)
    df["month"] = df["read_at"].dt.month
    df["year"] = df["read_at"].dt.year

    df = df[["read_at", "hour", "month", "year"] + features].copy()

    df.reset_index(drop=True, inplace=True)

    return df


def find_skewed_boundaries(df, variable, distance):

    IQR = df[variable].quantile(0.75) - df[variable].quantile(0.25)

    lower_boundary = df[variable].quantile(0.25) - (IQR * distance)
    upper_boundary = df[variable].quantile(0.75) + (IQR * distance)

    return upper_boundary, lower_boundary


def remove_outliers(df, variable, distance):
    upper_limit, lower_limit = find_skewed_boundaries(df, variable, distance)

    outliers = np.where(
        (df[variable] > upper_limit)|(df[variable] < lower_limit),
        True,
        False
    )

    df = df[~outliers].copy()

    return df


def lag_window(df, feature, hours):
    df = df.copy()

    df.set_index("read_at", inplace=True)

    for window in hours:
        df[f"{feature}_lag_{window}_hours"] = df[feature].shift(periods=window, freq="H")
        df.dropna(subset=f"{feature}_lag_{window}_hours", inplace=True)

    df.reset_index(drop=False, inplace=True)

    return df


def add_lag_features(df, lagged_features):
    # lagged_features = {
    #     "wind_speed" : [1, 2, ..., 24], # feature and hours to lag
    # }

    df = df.copy()

    df.set_index("read_at", inplace=True)

    for feature, window_hours_lst in lagged_features.items():
        for window_hours in window_hours_lst:
            df[f"{feature}_previous_{window_hours}_hours"] = df[feature].shift(periods=window_hours, freq="H")
            df.dropna(subset=f"{feature}_previous_{window_hours}_hours", inplace=True)

    df.reset_index(drop=False, inplace=True)

    return df