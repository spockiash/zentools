import pandas as pd

def load_ohcl_csv(path: str, datetime_column: str = "Date", dt_format: str = "ISO8601") -> pd.DataFrame:
    # Load the CSV
    data = pd.read_csv(path, parse_dates=[datetime_column], index_col=datetime_column)
    # Convert the index to datetime (to ensure proper handling of any date format)
    data.index = pd.to_datetime(data.index, format=dt_format)
    # Sort the DataFrame by index
    data = data.sort_index()
    return data