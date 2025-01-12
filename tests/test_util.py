import unittest
from gannpy.util import calculate_gann_values, test_data

class TestUtilFunctions(unittest.TestCase):

    def test_calculate_gann_values(self):
        result = calculate_gann_values(100)
        self.assertIsInstance(result, dict)
        self.assertIn("buy_above", result)
        self.assertIn("sell_below", result)

    def test_test_data(self):
        df = test_data()
        self.assertTrue(isinstance(df, pd.DataFrame))
        self.assertTrue('time' in df.columns)

if __name__ == '__main__':
    unittest.main()
