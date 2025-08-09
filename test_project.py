import os
import pytest
import pandas as pd
from pandas import DataFrame
from project import load_file, inspect_file, clean_data
from analysis.kpi import kpis_calculator
from analysis.anomalies import anomalies_detector
from analysis.plotting import(
    production_rate_plot,
    monthly_total_production,
    stacked_monthly_production,
    cumulative_and_ratios_plot
)

# Fixtures and sample data
@pytest.fixture
def sample_raw_df():
    return DataFrame({
        'Well_name': ['A1', 'A1', 'A2'],
        'Date': ['2024-01-01', '2024-01-02', '2024-01-01'],
        'Oil_rate': [100, 110, 95],
        'Gas_rate': [500, 510, 480],
        'Water_rate': [10, 12, 9]
    })

@pytest.fixture
def cleaned_df(sample_raw_df):
    return clean_data(sample_raw_df.copy())

# Tests for project.py
def test_load_file(tmp_path):
    # Create dummy CSV
    data = 'Well_name,Date,Oil_rate,Gas_rate,Water_rate\nA1,2024-01-01,100,500,10'
    file_path = tmp_path / 'test.csv'
    file_path.write_text(data)

    df = load_file(str(file_path))
    assert not df.empty
    assert list(df.columns) == ['Well_name', 'Date', 'Oil_rate', 'Gas_rate', 'Water_rate']

def test_inspect_file(capsys, sample_raw_df):
    inspect_file(sample_raw_df)
    captured = capsys.readouterr()
    assert 'Well_name' in captured.out
    assert 'Oil_rate' in captured.out

def test_clean_data(sample_raw_df):
    df = clean_data(sample_raw_df)
    assert df.isnull().sum().sum() == 0
    assert df['Date'].dtype.name == 'datetime64[ns]'

# Tests for kpis calculator
def test_kpis_calculator(cleaned_df):
    kpis = kpis_calculator(cleaned_df)
    assert isinstance(kpis, DataFrame)
    assert 'avg_oil_rate' in kpis.columns
    assert not kpis.empty

# Tests for anomaly detection
def test_anomalies_detector(cleaned_df):
    anomalies = anomalies_detector(cleaned_df, threshold=5)
    assert isinstance(anomalies, list)
    for entry in anomalies:
        assert 'Well_name' in entry
        assert 'Date' in entry
        assert 'Type' in entry
        assert 'Change (%)' in entry

# Tests for file outputs of plots
def test_production_rate_plot(cleaned_df):
    production_rate_plot(cleaned_df, 'Oil_rate', 'Test Plot', 'STB')
    assert os.path.exists('oil_rate_by_well.jpg')

def test_monthly_total_production(cleaned_df):
    monthly_total_production(cleaned_df)
    assert os.path.exists('monthly_oil_rate_totals.jpg')

def test_stacked_monthly_production(cleaned_df):
    stacked_monthly_production(cleaned_df)
    for well in cleaned_df['Well_name'].unique():
        assert os.path.exists(f'stacked_monthly_production_{well}.jpg')

def test_cumulative_and_ratios_plot(cleaned_df):
    cumulative_and_ratios_plot(cleaned_df)
    for well in cleaned_df['Well_name'].unique():
        assert os.path.exists(f'cumulative_production_{well}.jpg')
        assert os.path.exists(f'ratio_trends_{well}.jpg')
