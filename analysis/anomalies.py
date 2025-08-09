import pandas as pd
from pandas import DataFrame


def anomalies_detector(df: DataFrame, threshold: float = 0.30) -> list[dict]: # Func5
    """Detect sudden changes in daily production rates.

    Args:
        df (DataFrame): Cleaned production data.
        threshold (float): Fractional threshold (e.g., 0.3 = 30%)  to flag anomalies.

    Returns:
        list[dict]: A list of anomaly dictionaries with well name: date, rate type, and values.
    """
    anomalies = []
    df_sorted = df.sort_values(['Well_name', 'Date'])

    for well, group in df_sorted.groupby('Well_name'):
        group = group.copy().sort_values('Date')

        for rate_type in ['Oil_rate', 'Gas_rate', 'Water_rate']:
            group[f'prev_{rate_type}'] = group[rate_type].shift(1)
            group[f'{rate_type}_change'] = (group[rate_type] - group[f'prev_{rate_type}']) / group[f'prev_{rate_type}']

            for _, row in group.iterrows():
                prev_val = row[f'prev_{rate_type}']
                change = row[f'{rate_type}_change']

                if pd.notna(change) and abs(change) > threshold:
                    anomalies.append({
                        'Well_name': row['Well_name'],
                        'Date': row['Date'].strftime('%Y-%m-%d'),
                        'Type': rate_type,
                        'Current Rate': round(row[rate_type], 2),
                        'Previous Rate': round(prev_val, 2),
                        'Change (%)': round(change * 100, 1)
                    })
    # (Step 5) Save anomalies to CSV file
    if anomalies:
        pd.DataFrame(anomalies).to_csv('anomalies_detected.csv', index=False)
        print('\n<   Anomalies saved to "anomalies_detected.csv"   >')
    else:
        print('<   No anomalies detected. Nothing saved.   >')

    return anomalies

def anomalies_printer(anomalies: list[dict]) -> None: # Func6
    """Print formatted anomaly results.

    Args:
        anomalies (list[dict]): List of anomalies in dictionary format

    Returns:
        None (for preview only)
    """
    if not anomalies:
        print('\n<   No anomalies detected based on the given threshold.   >')
        return

    print(f'\n<   Detected Anomalies! ({len(anomalies)})   >\n')
    for entry in anomalies:
        print(f'Well: {entry['Well_name']} | Date: {entry['Date']} | Type: {entry['Type']}')
        print(f'  ➤  {entry['Type'].replace('_', ' ').title()}: {entry['Current Rate']} | Change: {entry['Change (%)']}%')
        print(f'  ➤  Previous Day: {entry['Previous Rate']}\n')
