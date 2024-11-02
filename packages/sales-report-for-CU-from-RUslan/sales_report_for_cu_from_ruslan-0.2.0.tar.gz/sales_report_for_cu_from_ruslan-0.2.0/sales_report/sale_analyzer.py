import pandas as pd

class SalesAnalyzer:
    def __init__(self, input_file):
        self.input_file = input_file
        self.data = pd.read_csv(input_file)

    def generate_report(self):
        report = self.data.groupby('category').agg(
            sales=('sales_report', 'sum'),
            quantity=('quantity', 'sum')
        ).reset_index()
        return report
