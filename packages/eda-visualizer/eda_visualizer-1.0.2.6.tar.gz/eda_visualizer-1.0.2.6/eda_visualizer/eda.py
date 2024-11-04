import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class eda_visualizer:
    def __init__(self, data, skip_high_cardinality=True, show_info=True):
        """
        Initialize with a pandas DataFrame and settings.
        
        Parameters:
            data (pd.DataFrame): The dataset to analyze.
            skip_high_cardinality (bool): If True, skips columns with more than 20 unique values in categorical plots.
            show_info (bool): If True, displays information like null value counts, describe statistics, and column names.
        """
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input data should be a pandas DataFrame.")
        
        self.data = data
        self.skip_high_cardinality = skip_high_cardinality
        self.show_info = show_info

        if self.show_info:
            self.display_data_info()

    def display_data_info(self):
        """Displays information about the dataset, such as missing values, descriptive stats, and column names."""
        print("Dataset Information:")
        print("-" * 120)
        print("\nNull values per column:\n", self.data.isnull().sum())
        print("\nDataset description:\n", self.data.describe())
        print("\nColumn names:\n", self.data.columns.tolist())
        print("-" * 120)

    def univariate_analysis(self, num_plot_type='hist', cat_plot_type='bar'):
        """
        Perform univariate analysis by plotting histograms (or other specified plot types) for numerical features
        and bar plots (or other specified plot types) for categorical features.

        Parameters:
            num_plot_type (str): Type of plot for numerical columns. Options: 'hist', 'box'.
            cat_plot_type (str): Type of plot for categorical columns. Options: 'bar', 'pie'.
        """
        # Separate numerical and categorical columns
        numerical_cols = self.data.select_dtypes(include=['int64', 'float64']).columns
        categorical_cols = self.data.select_dtypes(include=['object', 'category']).columns

        # Plot for numerical columns based on chosen plot type
        for col in numerical_cols:
            plt.figure(figsize=(8, 6))
            plot_type = input(f"Select plot type for numerical column '{col}' (hist/box/skip): ").strip().lower()
            if plot_type == 'skip':
                print(f"Skipping column '{col}'.")
                continue
            column_data = self.data[col].dropna().values
            
            if plot_type == 'hist':
                plt.hist(column_data, bins='auto', edgecolor='black')
                plt.title(f'Histogram of {col}')
            elif plot_type == 'box':
                plt.boxplot(column_data)
                plt.title(f'Box plot of {col}')
            else:
                print(f"Unsupported plot type '{plot_type}' for numerical data.")
                continue
            plt.xlabel(col)
            plt.ylabel('Frequency')
            plt.show()

        # Plot for categorical columns with cardinality check
        for col in categorical_cols:
            if self.skip_high_cardinality and self.data[col].nunique() > 20:
                print(f"Skipping '{col}' due to high cardinality.")
                continue

            plt.figure(figsize=(8, 6))
            plot_type = input(f"Select plot type for categorical column '{col}' (bar/pie/skip): ").strip().lower()
            if plot_type == 'skip':
                print(f"Skipping column '{col}'.")
                continue
            value_counts = self.data[col].value_counts()

            if plot_type == 'bar':
                plt.bar(value_counts.index, value_counts.values)
                plt.title(f'Bar Chart of {col}')
                plt.xlabel(col)
                plt.ylabel('Frequency')
                plt.xticks(rotation=45, ha='right')
            elif plot_type == 'pie':
                plt.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%')
                plt.title(f'Pie Chart of {col}')
            else:
                print(f"Unsupported plot type '{plot_type}' for categorical data.")
                continue
            plt.tight_layout()
            plt.show()