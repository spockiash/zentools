import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
from zentools.data_operations import slice_dataframe_by_date

class TestSliceDataFrameByDate(unittest.TestCase):
    def setUp(self):
        # Sample DataFrame
        self.data = pd.DataFrame({
            'Symbol': ['ETHUSDT'] * 5,
            'Open': [1564.22, 1563.45, 1566.51, 1568.00, 1561.66],
            'High': [1567.31, 1568.00, 1567.72, 1573.15, 1569.92],
            'Low': [1563.70, 1563.39, 1563.39, 1563.72, 1561.20],
            'Close': [1566.57, 1564.22, 1563.46, 1566.51, 1568.00],
            'Volume ETH': [3403.82350, 4833.05790, 5240.29830, 8725.29650, 6092.96190],
            'Volume USDT': [5.327189e+06, 7.566292e+06, 8.200644e+06, 1.369178e+07, 9.540306e+06],
            'tradecount': [12103, 12073, 15157, 19124, 16003]
        }, index=pd.to_datetime([
            '2023-10-19 23:00:00',
            '2023-10-19 22:00:00',
            '2023-10-19 21:00:00',
            '2023-10-19 20:00:00',
            '2023-10-19 19:00:00'
        ]))
        self.data.index.name = 'Date'
        # Sort the DataFrame by index
        self.data = self.data.sort_index()

    def test_valid_slice(self):
        # Define start and end datetime
        start_date = '2023-10-19 21:00:00'
        end_date = '2023-10-19 23:00:00'

        # Expected result
        expected_result = self.data.loc['2023-10-19 21:00:00':'2023-10-19 23:00:00']

        # Call the function
        result = slice_dataframe_by_date(self.data, start_date, end_date)

        # Assert the result
        assert_frame_equal(result, expected_result)

    def test_no_rows_in_range(self):
        # Define start and end datetime
        start_date = '2025-01-01 00:00:00'
        end_date = '2025-01-02 00:00:00'

        # Expected result (empty DataFrame)
        expected_result = self.data.iloc[0:0]

        # Call the function
        result = slice_dataframe_by_date(self.data, start_date, end_date)

        # Assert the result
        assert_frame_equal(result, expected_result)

    def test_invalid_index_type(self):
        # Create a DataFrame with a non-DateTime index
        invalid_data = self.data.reset_index()

        # Define start and end datetime
        start_date = '2023-10-19 21:00:00'
        end_date = '2023-10-19 23:00:00'

        # Assert that a ValueError is raised
        with self.assertRaises(ValueError):
            slice_dataframe_by_date(invalid_data, start_date, end_date)

    def test_invalid_date_format(self):
        # Define invalid start and end datetime
        start_date = 'invalid_date'
        end_date = '2023-10-19 23:00:00'

        # Assert that a ValueError is raised
        with self.assertRaises(ValueError):
            slice_dataframe_by_date(self.data, start_date, end_date)


if __name__ == '__main__':
    unittest.main()
