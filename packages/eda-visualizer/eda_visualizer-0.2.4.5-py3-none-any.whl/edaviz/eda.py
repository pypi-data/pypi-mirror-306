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
            column_data = self.data[col].dropna().to_numpy().flatten()  # Ensure 1D array
            
            if num_plot_type == 'hist':
                sns.histplot(column_data, kde=True)
                plt.title(f'Histogram of {col}')
            elif num_plot_type == 'box':
                sns.boxplot(x=column_data)
                plt.title(f'Box plot of {col}')
            else:
                print(f"Unsupported plot type '{num_plot_type}' for numerical data.")
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
            column_data = self.data[col].dropna()  # Use pandas Series for categorical

            if cat_plot_type == 'bar':
                sns.countplot(y=column_data, order=column_data.value_counts().index)
                plt.title(f'Bar Chart of {col}')
                plt.xlabel('Frequency')
                plt.ylabel(col)
            elif cat_plot_type == 'pie':
                # Convert to 1D values for the pie chart
                column_data.value_counts().plot.pie(autopct='%1.1f%%')
                plt.title(f'Pie Chart of {col}')
                plt.ylabel('')
            else:
                print(f"Unsupported plot type '{cat_plot_type}' for categorical data.")
                continue
            plt.show()
