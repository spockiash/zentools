# zentools/tests/data_operations/test_dataframe_tools.py

import unittest
import pandas as pd
from zentools.data_operations.technical_tools import add_macd


class TestCalculateMACD(unittest.TestCase):

    def test_macd_columns_added(self):
        # Input DataFrame with valid data
        input_data = pd.DataFrame({
            'Close': [1564.22, 1563.45, 1566.51, 1568.00, 1561.66, 1561.66, 1561.66, 1561.66, 1561.66, 1561.66,
                      1561.66,1561.66, 1561.66, 1561.66, 1561.66, 1561.66, 1561.66, 1561.66, 1561.66, 1561.66,
                      1561.66, 1561.66, 1561.66, 1561.66, 1561.66, 1561.66, 1561.66, 1561.66, 1561.66, 1561.66,
                      1561.66, 1561.66, 1561.66, 1561.66, 1561.66, 1561.66, 1561.66, 1561.66, 1561.66, ]
        })

        # Call the function
        result = add_macd(input_data, fast_period=12, slow_period=26, signal_period=9)

        # Verify that the required columns are added
        expected_columns = ['Close', 'EMA_12', 'EMA_26', 'MACD', 'Signal_Line', 'Histogram']
        self.assertTrue(set(expected_columns).issubset(result.columns),
                        msg="The function should add the required MACD-related columns to the DataFrame.")
        # Verify that the added columns are not empty
        for col in expected_columns[1:]:  # Skip 'Close'
            self.assertFalse(result[col].isnull().all(),
                             msg=f"Column '{col}' should not be entirely NaN.")


if __name__ == "__main__":
    unittest.main()