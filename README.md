# COVID Tracking

An interactive PyQt5 application for visualizing global COVID-19 data. The
program plots confirmed cases or recoveries for multiple countries using time
series CSV files such as those published by Johns Hopkins University.

## Features
- Load custom CSV files and parse dates and country totals.
- Plot up to ten countries simultaneously for either confirmed cases or
  recoveries.
- Search for countries to quickly filter the selection list.
- Adjust the displayed time range with a dual-ended slider.
- Export the current chart to a PDF report.

## Installation
Requires Python 3 and the following libraries:

```
PyQt5
matplotlib
numpy
reportlab
```

Install dependencies with:

```
pip install PyQt5 matplotlib numpy reportlab
```

## Usage
1. Run the main application:
   ```
   python Covid_main.py
   ```
2. Use **Load file** in each tab to open a time series CSV file. Sample datasets
   are provided in the repository.
3. Select countries from the list and adjust the time slider to tailor the
   chart.
4. Click **Export to PDF** to save the visualization.

