from pandas import DataFrame
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def production_rate_plot(df: DataFrame, rate_column: str, title: str, unit: str) -> None: # Func7
    """Generate daily fluid production trends for all wells

    Args:
        df (DataFrame): Cleaned production data.

    Returns:
        None (saves line charts as JPS files).
    """
    # Sort
    df['Well_name'] = pd.Categorical(df['Well_name'], categories=sorted(df['Well_name'].unique()), ordered=True)

    # Plot and (Step 5) save to JPG file
    plt.figure(figsize=(10,5))
    sns.lineplot(data=df, x='Date', y=rate_column, hue='Well_name', marker='o')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel(f'{rate_column.replace('_', ' ').replace('rate', 'Rate').title()} ({unit})')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.legend(title='Well', loc='best')

    file_name = f'{rate_column.lower()}_by_well.jpg'
    plt.savefig(file_name, dpi=300)
    plt.close()
    print(f'\n<   Production Rate Plot saved as {file_name}   >')

def monthly_total_production(df: DataFrame) -> None: # Func8
    """Generate Bar Chart for monthly fluid total production per well.

    Args:
        df (DataFrame): Cleaned production data.

    Returns:
        None (saves bar charts as JPG files).
    """
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.to_period('M').astype(str)

    fluids = {
        'Oil_rate': 'Oil (STB)',
        'Gas_rate': 'Gas (SCF)',
        'Water_rate': 'Water (STB)',
    }

    for rate_column, y_label in fluids.items():
        # Group by Well and Month
        monthly = df.groupby(['Well_name', 'Month'], observed=True)[rate_column].sum().reset_index()

        # Sort wells alphabetically for consistent legend
        monthly['Well_name'] = pd.Categorical(monthly['Well_name'], ordered=True, categories=sorted(df['Well_name'].unique()))

        # Plot and (Step 5) save to JPG file
        plt.figure(figsize=(10, 5))
        sns.barplot(data=monthly, x='Month', y=rate_column, hue='Well_name')

        plt.title(f'Monthly {y_label} Production by Well')
        plt.xlabel('Month')
        plt.ylabel(f'Total {y_label}')
        plt.xticks(rotation=45)
        plt.legend(title='Well')
        plt.grid(True)
        plt.tight_layout()

        file_name = f'monthly_{rate_column.lower()}_totals.jpg'
        plt.savefig(file_name, dpi=300)
        plt.close()
        print(f'\n<   Monthly Totals Production Plot saved as {file_name}   >')

def stacked_monthly_production(df: DataFrame) -> None: # Func9
    """Generate and save stacked bar charts of monthly production rates for each well.

    Args:
        df (DataFrame): Cleaned production data.

    Returns:
        None (saves bar charts as JPG files).
    """
    from matplotlib.patches import Patch

    # Create a new column for year-month
    df['Month'] = df['Date'].dt.to_period('M').astype(str)

    # Group by Well and Month with summed production
    grouped = df.groupby(['Well_name', 'Month'], observed=True)[['Oil_rate', 'Gas_rate', 'Water_rate']].sum().reset_index()

    # Plot for each well and (Step 5) save to JPG file
    for well in grouped['Well_name'].unique():
        subset = grouped[grouped['Well_name'] == well].sort_values('Month')

        months = subset['Month']
        water = subset['Water_rate']
        oil = subset['Oil_rate']
        gas = subset['Gas_rate']

        # Total production per bar
        total = water + oil + gas

        plt.figure(figsize=(10, 5))

        # Arranged visuals in Water (bottom) to Gas (top)
        plt.bar(months, water, label='Water', color='skyblue')
        plt.bar(months, oil, bottom=water, label='Oil', color='black')
        plt.bar(months, gas, bottom=water + oil, label='Gas', color='orange')

        # Add total production per bar as label on top
        for i, month in enumerate(months):
            plt.text(i, total.iloc[i] + 15, f'{total.iloc[i]:.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

        # (Step 5) Save to JPG file
        plt.legend()
        plt.title(f'Monthly Stacked Production - {well}')
        plt.xlabel('Month')
        plt.ylabel('Production Volume')
        plt.xticks(rotation=45)
        plt.grid(True, axis='y', linestyle='--', alpha=0.5)
        plt.tight_layout()

        file_name= f'stacked_monthly_production_{well}.jpg'
        plt.savefig(file_name, dpi=300)
        plt.close()
        print(f'\n<   Stacked Bar Chart saved as {file_name}   >')

def cumulative_and_ratios_plot(df: DataFrame) -> None: # Func10
    """
    Generate and save cumulative production curves and WOR/GOR ratio plots for each well.

    Args:
        df (DataFrame): Cleaned production data.

    Returns:
        None (saves the plots as JPG files.
    """
    # Sort date
    df = df.sort_values(['Well_name', 'Date']).copy()

    # Init cumulative columns and ratios
    df['Cumulative_oil'] = df.groupby('Well_name', observed=True)['Oil_rate'].cumsum()
    df['Cumulative_gas'] = df.groupby('Well_name', observed=True)['Gas_rate'].cumsum()
    df['Cumulative_water'] = df.groupby('Well_name', observed=True)['Water_rate'].cumsum()

    # Prevent divide by zero in ratio calculations
    df['WOR'] = df['Water_rate'] / df['Oil_rate'].replace(0, np.nan)
    df['GOR'] = df['Gas_rate'] / df['Oil_rate'].replace(0, np.nan)

    # Plot for each well and (Step 5) save to JPG file
    for well in df['Well_name'].unique():
        subset = df[df['Well_name'] == well]

        # Cumulative plot
        plt.figure(figsize=(10, 5))
        plt.plot(subset['Date'], subset['Cumulative_gas'], label='Cumulative Gas', color='orange')
        plt.plot(subset['Date'], subset['Cumulative_oil'], label='Cumulative Oil', color='black')
        plt.plot(subset['Date'], subset['Cumulative_water'], label='Cumulative Water', color='skyblue')
        plt.title(f'Cumulative Production - {well}')
        plt.xlabel('Date')
        plt.ylabel('Cumulative Volume')
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.savefig(f'cumulative_production_{well}.jpg', dpi=300)
        plt.close()
        print(f'\n<   Cumulative Production saved as cumulative_production_{well}.jpg   >')

        # Ratio plot
        plt.figure(figsize=(10,5))
        plt.plot(subset['Date'], subset['GOR'], label='GOR (Gas/Oil)', color='orange')
        plt.plot(subset['Date'], subset['WOR'], label='WOR (Water/Oil)', color='blue')
        plt.title(f'GOR and WOR Trends - {well}')
        plt.xlabel('Date')
        plt.ylabel('Ratio')
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.savefig(f'ratio_trends_{well}.jpg', dpi=300)
        plt.close()
        print(f'\n<   Ratio Trends saved as ratio_trends_{well}.jpg   >')
