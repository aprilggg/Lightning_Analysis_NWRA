# Exploratory Data Analysis

* [About Directory](#about)
* [Code Requirements](#requirements)

<a id="about"></a>

### About Directory
This directory contains all exploratory data analysis efforts created in the start of this project. We aim to understand WWLLN and TC track file data by plotting lightning events and storm centers for specific storms. We also explore different descriptive analytics at the overall level, the filtered TC level (TC category 1 or higher), and at basin levels. This directory requires data created in the [data_pipeline](../data_pipeline/) part of this project.

This directory contains the following notebooks:
- **`exploratory_analysis.ipynb`**
    - explore full WWLLN and storm track datasets
    - explore filtered WWLLN and storm track datasets (TC category 1 or higher)
    - explore descriptive analytics including storm duration, storm counts per year, lightning event distribution, wind-pressure relationship
- **`basin_descriptive_analysis.ipynb`**
    - explore inner core and rainband WWLLN data by basin
    - explore rainband lightning data by shear quadrant for each basin
    - explore lightning data by TC category, current category, and intensification stage by basin

<a id="requirements"></a>

### Code Requirements
The code in this directory require the following libraries not built-in to Python:
- cartopy
- matplotlib
- numpy
- pandas
- polars
- seaborn

The following data files are required for the notebooks in this directory:
- [Combined_Reduced_Trackfile.txt](../data_pipeline/intermediate_data/Combined_Reduced_Trackfile.txt)
- [Combined_WWLLN_Locations.txt](https://drive.google.com/file/d/1iXEjD-vr2B5csg-kcjQKZMcwl3jSwNqt/view?usp=drive_link) - in [Google Drive](https://drive.google.com/drive/folders/105AYgecVORsUCyOwinQRfb--TC0hhBva?usp=drive_link)
- [Filtered_Reduced_Trackfile.csv](../data_pipeline/intermediate_data/Filtered_Reduced_Trackfile.csv)
- [Filtered_WWLLN_Locations.txt](https://drive.google.com/file/d/1eGiSKw0vSCFcNohGniysSFnZm8h0WfQ0/view?usp=drive_link) - in [Google Drive](https://drive.google.com/drive/folders/105AYgecVORsUCyOwinQRfb--TC0hhBva?usp=drive_link)
- [innercore_timebin_joined.csv](../data_pipeline/data/innercore_timebin_joined.csv)
- [rainband_shear_timebin_joined.csv](../data_pipeline/data/rainband_shear_timebin_joined.csv)