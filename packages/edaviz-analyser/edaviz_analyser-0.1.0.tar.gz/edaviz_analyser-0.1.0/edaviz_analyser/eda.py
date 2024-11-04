import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Edaviz_analyser:
    def __init__(self, data):
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input data should be a pandas DataFrame.")
        self.data = data

    def univariate_analysis(self):
        numerical_cols = self.data.select_dtypes(include=['int64', 'float64']).columns
        categorical_cols = self.data.select_dtypes(include=['object', 'category']).columns

        for col in numerical_cols:
            plt.figure(figsize=(8, 6))
            sns.histplot(self.data[col].dropna(), kde=True)
            plt.title(f'Histogram of {col}')
            plt.xlabel(col)
            plt.ylabel('Frequency')
            plt.show()

        for col in categorical_cols:
            plt.figure(figsize=(8, 6))
            sns.countplot(y=self.data[col].dropna(), order=self.data[col].value_counts().index)
            plt.title(f'Bar Chart of {col}')
            plt.xlabel('Frequency')
            plt.ylabel(col)
            plt.show()
