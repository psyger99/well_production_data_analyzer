import sys
import numpy as np
import pandas as pd
from pandas import DataFrame
from analysis.kpi import kpis_calculator
from analysis.anomalies import anomalies_detector, anomalies_printer
from analysis.plotting import (
    production_rate_plot,
    monthly_total_production,
    stacked_monthly_production,
    cumulative_and_ratios_plot
)

def main():
    # Step 1: Data Loading and Overviewing
    try:
        if len(sys.argv) < 2:
            sys.exit('Too few command-line arguments.')

        if len(sys.argv) > 2:
            sys.exit(' Too many command-line arguments.')

        if not sys.argv[1].endswith('.csv'):
            sys.exit('Not a CSV file')

        df: DataFrame | None = load_file(sys.argv[1])

    except FileNotFoundError:
        sys.exit('File does not exist')

    except OSError:
        sys.exit('File cannot be opened.')

    # Step 2: Data Cleaning
    if df is not None:
        print('\nRaw Data Preview:')
        inspect_file(df)

        df_cleaned = clean_data(df)
        print('\nCleaned Data Preview:')
        inspect_file(df_cleaned)

        # Step 3: KPI Calculation and Anomaly Detection
        anomalies = anomalies_detector(df_cleaned, threshold=0.3)
        anomalies_printer(anomalies)

        print('\n<   KPI Calculation Complete!   >')
        print('\n', kpis_calculator(df_cleaned))

        # Step 4: Visualization (Daily, Monthly, Cummulative curves, and Ratio plots)
        # Daily fluid production trends for all wells
        production_rate_plot(df_cleaned, 'Oil_rate', 'Daily Oil Production by Well', 'STB/day')
        production_rate_plot(df_cleaned, 'Gas_rate', 'Daily Gas Production by Well', 'MSCF/day')
        production_rate_plot(df_cleaned, 'Water_rate', 'Daily Water Production by Well', 'STB/day')

        # Monthly fluid production trends for all wells
        monthly_total_production(df_cleaned)
        # Monthly stacked fluid production for each well
        stacked_monthly_production(df_cleaned)
        # Cummulative curves and ratio plots for each well
        cumulative_and_ratios_plot(df_cleaned)

def load_file(path: str) -> DataFrame | None: # Func1
    """Load production data from a CSV file.

    Args:
        path (str): The path to the CSV file.

    Returns:
        DataFrame | None: The loaded data as a DataFrame, or None if loading still fails.

    Example:
        >>> load_file(data.csv)
        Data loaded successfully.
    """
    try:
        df = pd.read_csv(path, na_values=['NA', 'N/A', 'null'], encoding='latin1', engine='python', on_bad_lines='skip')
        print('\n<   Data loaded successfully!   >')
        return df

    except FileNotFoundError:
        sys.exit('File is incorrect or file does not exist!')

    except PermissionError:
        sys.exit('Insufficient permissions to read the file')

    except pd.errors.EmptyDataError:
        sys.exit('File is empty!')

    return None

def inspect_file(df: DataFrame) -> None: # Func2
    """Display data preview

    Args:
        df (DataFrame): The raw production data to inspect.

    Returns:
        None (for terminal preview only)

    """
    print('\nData Overview:')
    print(df.info())

    print('\n\nFirst 10 Rows:')
    print(df.head(10))

    print('\n\nBasic Stats:')
    rate_columns = ['Oil_rate', 'Gas_rate', 'Water_rate']
    print(df[rate_columns].describe())

def clean_data(df: DataFrame) -> DataFrame: # Func3
    """Clean and preprocess the production data.

    Steps:
    / Convert 'Date' column to datetime and drops invalid dates
    / Replace negative rate values with NaN
    / Drop missing rate values

    Args:
        df (DataFrame): Raw production data.

    Returns:
        DataFrame: Cleaned production data.
    """
    # Convert Date column to Datetime
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Drop rows with missing or invalid dates
    df = df.dropna(subset=['Date'])

    # Replace negative production values with NaN
    rate_columns = ['Oil_rate', 'Gas_rate', 'Water_rate']
    for col in rate_columns:
        # Ensures numeric values
        df.loc[:, col] = pd.to_numeric(df[col], errors='coerce')
        # Replace negative values with None = NaN in pandas
        df.loc[:, col] = df[col].apply(lambda x: x if x>= 0 else np.nan)

    # Treat missing rate values
    df = df.dropna(subset=rate_columns)

    print('\n<   Data Cleaning Done!   >')
    return df

if __name__ == "__main__":
    main()
