import pandas as pd


def add_macd(data: pd.DataFrame, fast_period: int, slow_period: int, signal_period: int):
    """
    Adds MACD (Moving Average Convergence Divergence) calculations to a DataFrame.

    This function computes the MACD Line, Signal Line, and Histogram for the given
    closing price data and appends them as new columns to the DataFrame.

    Args:
        data (pd.DataFrame): The input DataFrame containing a 'Close' column with closing prices.
        fast_period (int): The period for the fast EMA.
        slow_period (int): The period for the slow EMA.
        signal_period (int): The period for the Signal Line EMA.

    Returns:
        pd.DataFrame: The input DataFrame with additional columns:
            - 'EMA_{fast_period}': Fast Exponential Moving Average.
            - 'EMA_{slow_period}': Slow Exponential Moving Average.
            - 'MACD': Difference between Fast EMA and Slow EMA.
            - 'Signal_Line': EMA of the MACD Line.
            - 'Histogram': Difference between MACD Line and Signal Line.
    """
    # Return the input DataFrame if it contains any NaN values
    if data.isnull().values.any():
        return data

    # Fast EMA
    data[f'EMA_{fast_period}'] = data['Close'].ewm(span=fast_period, adjust=False).mean()

    # Slow EMA
    data[f'EMA_{slow_period}'] = data['Close'].ewm(span=slow_period, adjust=False).mean()

    # MACD Line
    data['MACD'] = data[f'EMA_{fast_period}'] - data[f'EMA_{slow_period}']

    # Signal Line
    data['Signal_Line'] = data['MACD'].ewm(span=signal_period, adjust=False).mean()

    # Histogram
    data['Histogram'] = data['MACD'] - data['Signal_Line']

    return data

