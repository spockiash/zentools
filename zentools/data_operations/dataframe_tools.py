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
