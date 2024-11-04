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
        print("-" * 115)
        print("\nNull values per column:\n", self.data.isnull().sum())
        print("-" * 115)
        print("\nDataset description:\n", self.data.describe())
        print("-" * 115)
        print("\nColumn names:\n", self.data.columns.tolist())
        print("-" * 115)

    def univariate_analysis(self,auto_mode=False, num_plot_type='hist', cat_plot_type='bar'):
        """
        Perform univariate analysis by plotting histograms (or other specified plot types) for numerical features
        and bar plots (or other specified plot types) for categorical features.

        Parameters:
            auto_mode (bool): If True, uses default plot types without prompting. If False, prompts user for each column.
            num_plot_type (str): Default plot type for numerical columns if auto_mode is True. Options: 'hist', 'box'.
            cat_plot_type (str): Default plot type for categorical columns if auto_mode is True. Options: 'bar', 'pie'.
        """
        # Separate numerical and categorical columns
        numerical_cols = self.data.select_dtypes(include=['int64', 'float64']).columns
        categorical_cols = self.data.select_dtypes(include=['object', 'category']).columns

        # Plot for numerical columns based on chosen plot type
        for col in numerical_cols:
            plt.figure(figsize=(8, 6))

            if auto_mode:
                plot_type = num_plot_type
            else:
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
            if auto_mode:
                plot_type = cat_plot_type
            else:
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

    def bivariate_analysis(self, auto_mode=False, num_num_plot_type='scatter', num_cat_plot_type='box', cat_cat_plot_type='count'):
        """
        Perform bivariate analysis by plotting relationships between pairs of columns in a (2, 2) subplot layout.

        Parameters:
            auto_mode (bool): If True, uses default plot types without prompting. If False, prompts user for each pair of columns.
            num_num_plot_type (str): Default plot type for numerical-numerical pairs if auto_mode is True. Options: 'scatter'.
            num_cat_plot_type (str): Default plot type for numerical-categorical pairs if auto_mode is True. Options: 'box'.
            cat_cat_plot_type (str): Default plot type for categorical-categorical pairs if auto_mode is True. Options: 'count'.
        """
        # Separate numerical and categorical columns
        numerical_cols = self.data.select_dtypes(include=['int64', 'float64']).columns
        categorical_cols = self.data.select_dtypes(include=['object', 'category']).columns

        plot_count = 0

        # Helper function to create a new (2, 2) figure when needed
        def new_figure():
            return plt.subplots(2, 2, figsize=(14, 10))

        fig, ax = new_figure()

        # Plot for numerical-numerical pairs
        for i, col1 in enumerate(numerical_cols):
            for col2 in numerical_cols[i + 1:]:
                if auto_mode:
                    plot_type = num_num_plot_type
                else:
                    plot_type = input(f"Select plot type for numerical-numerical pair '{col1}' and '{col2}' (scatter/skip): ").strip().lower()

                if plot_type == 'skip':
                    print(f"Skipping pair '{col1}' and '{col2}'.")
                    continue

                row, col = divmod(plot_count, 2)
                if plot_type == 'scatter':
                    ax[row, col].scatter(self.data[col1], self.data[col2], alpha=0.5)
                    ax[row, col].set_title(f'Scatter Plot of {col1} vs {col2}')
                    ax[row, col].set_xlabel(col1)
                    ax[row, col].set_ylabel(col2)

                plot_count += 1

                # Display and reset figure after 4 plots
                if plot_count % 4 == 0:
                    plt.tight_layout()
                    plt.show()
                    fig, ax = new_figure()
                    plot_count = 0

        # Plot for numerical-categorical pairs
        for num_col in numerical_cols:
            for cat_col in categorical_cols:
                if self.skip_high_cardinality and self.data[cat_col].nunique() > 20:
                    print(f"Skipping '{cat_col}' due to high cardinality.")
                    continue

                if auto_mode:
                    plot_type = num_cat_plot_type
                else:
                    plot_type = input(f"Select plot type for numerical-categorical pair '{num_col}' and '{cat_col}' (box/skip): ").strip().lower()

                if plot_type == 'skip':
                    print(f"Skipping pair '{num_col}' and '{cat_col}'.")
                    continue

                row, col = divmod(plot_count, 2)
                if plot_type == 'box':
                    sns.boxplot(x=self.data[cat_col], y=self.data[num_col], ax=ax[row, col])
                    ax[row, col].set_title(f'Box Plot of {num_col} by {cat_col}')
                    ax[row, col].set_xlabel(cat_col)
                    ax[row, col].set_ylabel(num_col)
                    ax[row, col].tick_params(axis='x', rotation=45)

                plot_count += 1

                # Display and reset figure after 4 plots
                if plot_count % 4 == 0:
                    plt.tight_layout()
                    plt.show()
                    fig, ax = new_figure()
                    plot_count = 0

        # Plot for categorical-categorical pairs
        for i, cat_col1 in enumerate(categorical_cols):
            for cat_col2 in categorical_cols[i + 1:]:
                if self.skip_high_cardinality and (self.data[cat_col1].nunique() > 20 or self.data[cat_col2].nunique() > 20):
                    print(f"Skipping pair '{cat_col1}' and '{cat_col2}' due to high cardinality.")
                    continue

                if auto_mode:
                    plot_type = cat_cat_plot_type
                else:
                    plot_type = input(f"Select plot type for categorical-categorical pair '{cat_col1}' and '{cat_col2}' (count/skip): ").strip().lower()

                if plot_type == 'skip':
                    print(f"Skipping pair '{cat_col1}' and '{cat_col2}'.")
                    continue

                row, col = divmod(plot_count, 2)
                if plot_type == 'count':
                    sns.countplot(x=self.data[cat_col1], hue=self.data[cat_col2], ax=ax[row, col])
                    ax[row, col].set_title(f'Count Plot of {cat_col1} by {cat_col2}')
                    ax[row, col].set_xlabel(cat_col1)
                    ax[row, col].set_ylabel('Count')
                    ax[row, col].tick_params(axis='x', rotation=45)

                plot_count += 1

                # Display and reset figure after 4 plots
                if plot_count % 4 == 0:
                    plt.tight_layout()
                    plt.show()
                    fig, ax = new_figure()
                    plot_count = 0

        # Show any remaining plots
        if plot_count % 4 != 0:
            plt.tight_layout()
            plt.show()
