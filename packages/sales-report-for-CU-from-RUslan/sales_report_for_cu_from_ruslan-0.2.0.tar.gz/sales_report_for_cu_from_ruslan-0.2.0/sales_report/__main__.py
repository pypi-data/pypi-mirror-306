import argparse
import pandas as pd
from .sale_analyzer import SalesAnalyzer

def main():
    parser = argparse.ArgumentParser(description='Анализатор продаж')
    parser.add_argument('--input-file', required=True, help='Путь к входному CSV-файлу')
    parser.add_argument('--output-file', required=True, help='Путь к выходному CSV-файлу')

    args = parser.parse_args()

    analyzer = SalesAnalyzer(args.input_file)
    report = analyzer.generate_report()

    report.to_csv(args.output_file, index=False)


if __name__ == '__main__':
    main()
