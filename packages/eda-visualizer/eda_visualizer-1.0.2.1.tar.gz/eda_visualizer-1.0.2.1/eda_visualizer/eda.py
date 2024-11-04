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

    def univariate_analysis(self):
        """
        Perform univariate analysis by prompting the user to select plot types for each numerical and categorical column.
        """
        # Separate numerical and categorical columns
        numerical_cols = self.data.select_dtypes(include=['int64', 'float64']).columns
        categorical_cols = self.data.select_dtypes(include=['object', 'category']).columns

        # Interactive plot selection for numerical columns
        for col in numerical_cols:
            plt.figure(figsize=(8, 6))
            
            # Prompt user for plot type
            plot_type = input(f"Select plot type for numerical column '{col}' (hist/box): ").strip().lower()

            # Validate and apply selected plot type
            column_data = self.data[col].dropna().values
            if plot_type == 'hist':
                sns.histplot(column_data, kde=True)
                plt.title(f'Histogram of {col}')
                plt.xlabel(col)
                plt.ylabel('Frequency')
            elif plot_type == 'box':
                sns.boxplot(x=column_data)
                plt.title(f'Box plot of {col}')
                plt.xlabel(col)
                plt.ylabel('Frequency')
            else:
                print(f"Unsupported plot type '{plot_type}' for numerical data. Skipping column '{col}'.")
                continue
            plt.show()

        # Interactive plot selection for categorical columns
        for col in categorical_cols:
            # Check cardinality condition
            if self.skip_high_cardinality and self.data[col].nunique() > 20:
                print(f"Skipping '{col}' due to high cardinality.")
                continue

            plt.figure(figsize=(8, 6))
            
            # Prompt user for plot type
            plot_type = input(f"Select plot type for categorical column '{col}' (bar/pie): ").strip().lower()

            # Validate and apply selected plot type
            column_data = self.data[col].dropna()
            if plot_type == 'bar':
                sns.countplot(y=column_data, order=column_data.value_counts().index)
                plt.title(f'Bar Chart of {col}')
                plt.xlabel('Frequency')
                plt.ylabel(col)
            elif plot_type == 'pie':
                column_data.value_counts().plot.pie(autopct='%1.1f%%')
                plt.title(f'Pie Chart of {col}')
                plt.ylabel('')
            else:
                print(f"Unsupported plot type '{plot_type}' for categorical data. Skipping column '{col}'.")
                continue
            plt.show()
