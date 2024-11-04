class DataCleaner:
    """Handle basic data cleaning tasks"""

    def __init__(self):
        pass

    def clean(self, df):
        """Perform basic data cleaning"""
        print("Cleaning data...")

        # Make a copy to avoid modifying the original dataframe
        df_cleaned = df.copy()

        # 1. Remove rows with null values or NA
        initial_rows = len(df_cleaned)
        df_cleaned.dropna(inplace=True)
        rows_removed_null = initial_rows - len(df_cleaned)

        # 2. Remove duplicate data
        initial_rows = len(df_cleaned)
        df_cleaned.drop_duplicates(inplace=True)
        rows_removed_duplicates = initial_rows - len(df_cleaned)

        print(f"Data cleaning completed.")
        print(f"Rows removed due to null values: {rows_removed_null}")
        print(f"Rows removed due to duplicates: {rows_removed_duplicates}")
        print(f"Final dataset shape: {df_cleaned.shape}")

        return df_cleaned