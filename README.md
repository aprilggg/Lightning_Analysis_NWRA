# Lightning-Analysis
UW MSDS Capstone Project with Northwest Research Associates

## Objective

## Table of Contents

| Team Member  | GitHub                                   |
|------------------|--------------------------------------|
| April Gao       | [aprilggg](https://github.com/aprilggg)    |
| Elaine Zhang     | [ezhang17](https://github.com/ezhang17)|
| Janice Kim      | [ymkim814](https://github.com/ymkim814)|
## Directory Summary
**data_pipeline** - contains notebooks used to upload, clean, process, and create data files used in the analysis portion of this project

**exploratory_analysis** - contains notebooks as well as visualizations created in the exploratory analysis portion of this project

**intensification_analysis** - contains notebooks and visualizations for the statistical analysis of the relationship between lightning bursts and TC intensification change

**lightning_burst_identification** - contains notebooks, datasets, and visualizations created in the statistical identification of inner core and rainband lightning bursts at both the individual TC and basin levels

**vis_data** - contains data files used in the Power BI dashboard

### Directory Structure
```
.
├── data_pipeline
|   └── data
|       └── ...
|   └── README.md
|   └── data_file_cleaning.ipynb
|   └── data_processing.ipynb
|   └── data_upload.ipynb
|   └── rainband_data.ipynb
|   └── shear_data_file_log.txt
├── exploratory_analysis
|   └── basin_descriptive_analysis.ipynb
|   └── exploratory_analysis.ipynb
├── intensification_analysis
|   └── burst_w_intensification.ipynb
├── lightning_burst_identification
|   └── data
|       └── ...
|   └── visualizations
|       └── ...
|   └── README.md
|   └── __init__.py
|   └── lightning_threshold_functions.py
|   └── lightning_threshold_innercore.ipynb
|   └── lightning_threshold_rainband.ipynb
├── vis_data
|   └── README.md
|   └── basin_bursts_summary.csv
|   └── basin_threshold_bursts.csv
|   └── basin_threshold_tc_summary.csv
|   └── tc_lightning_vis_data.csv
|   └── tc_threshold.csv
|   └── threshold_summary.csv
├── LICENSE
└── README.md
```

Detailed documentation on code requirements and file outputs can be found in each folder's README file.

