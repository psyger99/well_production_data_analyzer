# Well Production Data Analyzer

#### Video Demo: [Youtube]([URL](https://youtu.be/GkwPdZG_Ooc))

#### Description:

The **Well Production Data Analyzer** is a Python-based program designed to automate the loading, cleaning, analysis, and visualization of production data from oil and gas wells. This tool helps engineers and analysts to quickly inspect well performance, detect anomalies in production rates, and generate meaningful visual summaries such as trend lines, bar graphs, and cumulative production plots. The project demonstrates proficiency in data manipulation, modular programming, plotting, and unit testing using Python language.

This project was developed as the final requirement for Harvard's edX CS50P (Introduction to Programming with Python) course, aligning with my professional background in Petroleum Engineering. The program works with production data stored in CSV format and is designed to be modular, scalable, and easy to interpret.

---

## File Descriptions

- **`project.py`**: The main script that runs the program. It contains the entry-point `main()` function and three core functions: `load_file`, `inspect_file`, `clean_data`. It handles user interaction and calls the appropriate modules for analysis and visualization.
- **`analysis/kpi.py`**: Calculate the KPIs for each well from the production data.
- **`analysis/anomalies.py`**: Detects anomalies in oil, gas, and water rates based on certain threshold.
- **`analysis/plotting.py`**: Handles all the visualization functions:
    - Daily production line plots
    - Monthly production bar graphs
    - Stacked fluid production
    - Cumulative and GOR/WOR plots
- **`test_project.py`**: Unit tests that validate core logic and file generation using mocks.
- **`/data` folder**: This directory contains sample input CSV used for testing and demonstration.
- **`README.md`**: This file. It describes the project, structure, usage, and design considerations.

---

## How It Works

1. **User Input**: User must indicate a CSV file to analyze in CLI. Only 1 CSV file at a time.
    ```
    <bash>

    python project.py production_data.csv
    ```
2. **Data Cleaning**: Removes missing data and enforces correct types.
3. **Anomaly Detection**: Anomalies in fluid production are flagged if the day-to-day rate change exceeds the user's threshold.
4. **Visualization**: Multiple plots are saved automatically, including:
    - Daily production rate trends (line plots)
    - Monthly totals (bar charts)
    - Stacked monthly fluid production
    - Cumulative production and GOR/WOR plots
5. **Output**: Cleaned data and anomalies are optionally exported as new CSV files. Graphs are saved as `.jpg` images for reporting and presentations.

---

## Design Decisions

- **User Input Handling**: Prompts are designed to avoid crashing on bad input.
- **Modularity**: Organized into logical modules for easier testing and reusability.
- **Testability**: The plotting functions were designed to save files rather than show them live to simplify automated testing.
- **Visualization Choices**: `seaborn` and `matplotlib` are used for clean, visually appealing, and industry-style plots.
- **Docstring Conventions**: `PEP 257` was used as it remains the core reference for Python documentation.
- **FILE I/O**: `pandas` library was utilized for reading csv file instead of the conventional, built-in csv module because it's better when working with structured tabular data due to its headers, data types, and missing values handling which acts like an automatic parser. It also allowed the creator to handle output (DataFrame) easily for data analysis function like filtering, aggregation, or plotting.
- **Handling Negative Rates**: Replaced negative production values with NaN, instead of 0 or using forward fill method of `pandas`. Bad data should be excluded from the calculations to maintain data integrity without artificially inflated/deflated values.

---

## Testing Instructions

To run the unit tests:
```
<bash>

pytest test_project.py
```
Ensure you have `pytest`, `pandas`, `numpy`, `matplotlib`, and `seaborn` installed in your environment.

Mocking techniques were used to simulate file input/output and ensure that all core functions behave as expected without depending on actual files during tests.

---

## Future Improvements
- Support for Excel input files (`.xlsx`).
- Export summary report as `PDF`.
- Display the summary of generated output files (`.jpg` & `.csv`) in print.
- `MemoryError` handling for large data.
- Computes expected production using historical trends.
- Classifies anomalies as Warning, Critical, or Emergency (at different acceptable threshold).

---

## Author
```
Rainer Alano /// psyger-99
Petroleum Engineer
```
>>>>>>> master
