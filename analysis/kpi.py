from pandas import DataFrame

def kpis_calculator(df: DataFrame) -> DataFrame: # Func4
    """Calculate KPIs for each well from production data.

    Args:
        df (DataFrame): Cleaned production data.

    Returns:
        DataFrame: Summary of KPIs per well.
    """
    kpis = df.groupby('Well_name').agg(
        production_days = ('Date', lambda x: (x.max() - x.min()).days + 1),
        first_production = ('Date', 'min'),
        last_production = ('Date', 'max'),
        cum_oil = ('Oil_rate', 'sum'),
        cum_gas = ('Gas_rate', 'sum'),
        cum_water = ('Water_rate', 'sum'),
        avg_oil_rate = ('Oil_rate', 'mean'),
        avg_gas_rate = ('Gas_rate', 'mean'),
        avg_water_rate = ('Water_rate', 'mean'),
    ).reset_index()

    # Additional KPIs
    kpis['water_cut (%)'] = (kpis['cum_water'] / (kpis['cum_oil'] + kpis['cum_water'])) * 100
    kpis['gas_oil_ratio (scf/stb)'] = kpis['cum_gas'] / kpis['cum_oil']

    # Date format
    kpis['first_production'] = kpis['first_production'].dt.strftime('%Y-%m-%d')
    kpis['last_production'] = kpis['last_production'].dt.strftime('%Y-%m-%d')

    # Round the float dtypes
    kpis[['cum_oil', 'cum_gas', 'cum_water', 'avg_oil_rate', 'avg_gas_rate', 'avg_water_rate', 'water_cut (%)', 'gas_oil_ratio (scf/stb)']] = kpis[['cum_oil', 'cum_gas', 'cum_water', 'avg_oil_rate', 'avg_gas_rate', 'avg_water_rate', 'water_cut (%)', 'gas_oil_ratio (scf/stb)']].round(2)

    # (Step 5) Save KPI Summary to CSV file
    kpis.to_csv('kpis_summary.csv', index=False)
    print('\n<   KPI Summary saved to "kpis_summary.csv"   >')

    return kpis
