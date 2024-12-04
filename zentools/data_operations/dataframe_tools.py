import numpy as np
import pandas as pd

def slice_dataframe_by_date(df: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Slices a DataFrame based on inclusive datetime boundaries provided as start and stop.

    Args:
        df (pd.DataFrame): The input DataFrame with a 'Date' index of type DateTime.
        start_date (str): The start datetime boundary (inclusive) in 'YYYY-MM-DD HH:MM:SS' format.
        end_date (str): The end datetime boundary (inclusive) in 'YYYY-MM-DD HH:MM:SS' format.

    Returns:
        pd.DataFrame: A sliced DataFrame containing rows within the specified datetime range.
    """
    # Ensure the index is a DatetimeIndex
    if not isinstance(df.index, pd.DatetimeIndex):
        raise ValueError("The DataFrame index must be of type pd.DatetimeIndex.")

    # Ensure the index is sorted
    if not df.index.is_monotonic_increasing:
        df = df.sort_index()

    # Convert start and end dates to datetime
    start_datetime = pd.to_datetime(start_date)
    end_datetime = pd.to_datetime(end_date)

    # Slice the DataFrame
    return df.loc[start_datetime:end_datetime]

def make_stationary(df: pd.DataFrame, columns: list[str] = None, use_pct: bool = False) -> pd.DataFrame:
    """
    Makes the specified columns of a DataFrame stationary by differencing.
    If no columns are provided, applies to all numeric columns.

    Args:
        df (pd.DataFrame): The input DataFrame.
        columns (list[str], optional): List of column names to process. Defaults to None.
        use_pct (bool, optional): Whether to use percentage difference instead of value difference. Defaults to False.

    Returns:
        pd.DataFrame: The DataFrame with modified columns made stationary.
    """
    # Determine columns to process
    if columns is None:
        columns = df.select_dtypes(include=['number']).columns.tolist()

    # Create a copy to avoid modifying the original DataFrame
    df = df.copy()

    # Apply differencing to make the columns stationary
    for column in columns:
        if column in df.columns:
            if use_pct:
                df[column] =  df[column].pct_change()
            else:
                df[column] = df[column].diff()

    return df

def clip_columns(df: pd.DataFrame, min_value: float, max_value: float, columns: list[str] = None, ) -> pd.DataFrame:
    """
    Clips the specified columns of a DataFrame to specified boundaries.
    If no columns are provided, applies to all numeric columns.

    Args:
        df (pd.DataFrame): The input DataFrame.
        min_value (float, optional): Minimum clipping value.
        max_value (float, optional): Maximum clipping value.
        columns (list[str], optional): List of column names to process. Defaults to None.
    Returns:
        pd.DataFrame: The DataFrame with clipped.
    """
    # Determine columns to process
    if columns is None:
        columns = df.select_dtypes(include=['number']).columns.tolist()

    # Create a copy to avoid modifying the original DataFrame
    df = df.copy()

    # Apply differencing to make the columns stationary
    for column in columns:
        if column in df.columns:
            df[column] =  df[column].clip(min_value, max_value)

    return df

def inf_to_nan(df: pd.DataFrame) -> pd.DataFrame:
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    return df

def nan_to_zero(df: pd.DataFrame) -> pd.DataFrame:
    df.fillna(0, inplace=True)