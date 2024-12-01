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

def add_rsi(data: pd.DataFrame, period: int = 14):
    """
    Calculates RSI (Relative Strength Index) using mathematically constrained method.

    Args:
       data (pd.DataFrame): The input DataFrame containing a 'Close' column with closing prices.
       period (int): The period for calculating RSI (default is 14).

    Returns:
       pd.DataFrame: The input DataFrame with an additional 'RSI' column.

    Raises:
       ValueError: If the 'Close' column contains NaN values.
    """
    # Check for NaN values
    if data['Close'].isnull().any():
        raise ValueError("Input DataFrame contains NaN values in the 'Close' column")

    # Calculate price changes
    delta = data['Close'].diff()

    # Separate gains and losses
    gains = delta.clip(lower=0)
    losses = -delta.clip(upper=0)

    # Compute average gains and losses
    avg_gain = gains.rolling(window=period, min_periods=period).mean()
    avg_loss = losses.rolling(window=period, min_periods=period).mean()

    # Calculate relative strength with mathematical constraint
    rs = avg_gain / avg_loss

    # Mathematical RSI calculation that is inherently between 0 and 100
    data['RSI'] = 100 - (100 / (1 + rs))

    return data

def add_ewm_rsi(data: pd.DataFrame, period: int = 14):
    """
    Calculates smoothed RSI using exponential weighted moving average.

    Args:
       data (pd.DataFrame): The input DataFrame containing a 'Close' column with closing prices.
       period (int): The period for calculating RSI (default is 14).

    Returns:
       pd.DataFrame: The input DataFrame with an additional 'RSI' column.

    Raises:
       ValueError: If the 'Close' column contains NaN values.
    """
    # Check for NaN values
    if data['Close'].isnull().any():
        raise ValueError("Input DataFrame contains NaN values in the 'Close' column")

    # Calculate price changes
    delta = data['Close'].diff()

    # Separate gains and losses
    gains = delta.clip(lower=0)
    losses = -delta.clip(upper=0)

    # Compute exponentially weighted average gains and losses
    avg_gain = gains.ewm(span=period, adjust=False).mean()
    avg_loss = losses.ewm(span=period, adjust=False).mean()

    # Calculate relative strength with mathematical constraint
    rs = avg_gain / avg_loss

    # Mathematical RSI calculation that is inherently between 0 and 100
    data['RSI'] = 100 - (100 / (1 + rs))

    return data


