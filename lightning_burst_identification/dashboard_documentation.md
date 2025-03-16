# Lightning Burst Dashboard Usage & Development Guide

This document provides usage and development guides for the `lightning_burst_dashboard.pbix` Power BI dashboard.

## Dependencies

** check if necessary for all or just development??

This dashboard requires [Power BI Desktop](https://learn.microsoft.com/en-us/power-bi/fundamentals/desktop-get-the-desktop) and the following files from the [analysis_data](../analysis_data/) directory:
- `innercore_bursts.csv`
- `innercore_lightning_data.csv`
- `rainband_bursts.csv`
- `rainband_lightning_data.csv`

These files are created in the `lightning_threshold_innercore.ipynb` and `lightning_threshold_rainband.ipynb` notebooks in this folder.

The Python visualizations in this dashboard require installation of Python and the following non-native Python libraries:
- pandas
- matplotlib

Refer to the [Power BI Python visualization documentation](https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-python-visuals) for more details.

## Usage Guide

After installing Power BI Desktop, open the `` file.

You will first see
![alt text](image.png)

## Development Guide