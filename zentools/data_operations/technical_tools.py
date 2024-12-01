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
    Adds RSI (Relative Strength Index) calculations to a DataFrame.

    This function computes the RSI for the given closing price data and appends it as a new column to the DataFrame.

    Args:
       data (pd.DataFrame): The input DataFrame containing a 'Close' column with closing prices.
       period (int): The period for calculating RSI (default is 14).

    Returns:
       pd.DataFrame: The input DataFrame with an additional 'RSI' column.
   """
    # Ensure DataFrame does not contain any NaN values in the 'Close' column
    if data['Close'].isnull().any():
        # TODO: raise exception
        return data

    # Calculate percentage price changes (delta)
    delta = data['Close'].diff()

    # Separate gains and losses
    gains = delta.where(delta > 0, 0)
    losses = delta.where(delta < 0, 0)

    # Calculate average gains and losses for the period
    avg_gain = gains.rolling(period, min_periods=1).mean()
    avg_loss = losses.rolling(period, min_periods=1).mean()
    # Calculate the relative strength
    rs = avg_gain / avg_loss

    # Calculate RSI
    data['RSI'] = 100 - (100 / (1 + rs))
    return data

def add_ewm_rsi(data: pd.DataFrame, period: int = 14):
    """
    Adds smoothed RSI (Relative Strength Index) calculations to a DataFrame.

    This function computes the RSI for the given closing price data and appends it as a new column to the DataFrame.

    Args:
       data (pd.DataFrame): The input DataFrame containing a 'Close' column with closing prices.
       period (int): The period for calculating RSI (default is 14).

    Returns:
       pd.DataFrame: The input DataFrame with an additional 'RSI' column.
   """
    # Ensure DataFrame does not contain any NaN values in the 'Close' column
    if data['Close'].isnull().any():
        # TODO: raise exception
        return data

    # Calculate percentage price changes (delta)
    delta = data['Close'].diff()

    # Separate gains and losses
    gains = delta.where(delta > 0, 0)
    losses = delta.where(delta < 0, 0)

    # Calculate average gains and losses for the period
    avg_gain = gains.ewm(span=period, adjust=False).mean()  # Exponentially weighted mean of gains
    avg_loss = losses.ewm(span=period, adjust=False).mean()  # Exponentially weighted mean of losses
    # Calculate the relative strength
    rs = avg_gain / avg_loss

    # Calculate RSI
    data['RSI'] = 100 - (100 / (1 + rs))
    return data


