import unittest
class TestAnalyzeData(unittest.TestCase):
    def setUp(self):
        data = {
            'A': [1, 2, 3, 4, 5],
            'B': [5, 4, 3, 2, 1],
            'target': [0, 1, 0, 1, 0]
        }
        self.df = pd.DataFrame(data)
        self.analyze = AnalyzeData(self.df, 'target', "gsk-")

    def test_univariate_analysis_shape(self):
        shape_df, *_ = self.analyze.univariate_analysis()
        self.assertIn('5 rows and 3 columns', shape_df)

if __name__ == '__main__':
    resp= unittest.main(argv=['first-arg-is-ignored'], exit=False)