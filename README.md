# Lightning-Analysis
UW MSDS Capstone Project with Northwest Research Associates

## Table of Contents
* [Objective](#objective)
* [Background Information](#background)
* [Directory Overview](#directory-overview)
* [Deliverables](#deliverables) - need a better name for this... process?
* [Dependencies](#dependencies)
  * [Environment](#environment)
  * [Data](#data)
* [Future Work](#future-work)

| Team Member  | GitHub                                   |
|------------------|--------------------------------------|
| April Gao       | [aprilggg](https://github.com/aprilggg)|
| Elaine Zhang     | [ezhang17](https://github.com/ezhang17)|
| Janice Kim      | [ymkim814](https://github.com/ymkim814)|

<a id="objective"></a>

## Objective

<a id="background"></a>

## Background Information

** flesh out later

inner core defined as <100km of center, rainband defined as 200-400km

We use the following standards to categorize intensification stage and category based off wind speed in knots.

**Intensification Stage Bins**
| Intensification Stage | Change in Winds (Knots) in 24 Hours (Jiang and Ramirez, 2013)|
| --------------------- | ----------------------|
| Rapidly Weakening | <-30 |
| Weakening | -30 to -10 |
| Neutral | -10 to 10 |
| Intensifying | 10 to 30 |
| Rapidly Intensifying | >30 |

**TC Category Bins - Saffir-Simpson Hurricane Wind Scale**
| TC Category | Sustained Winds (Knots) |
|  ---------- | ------------|
| 1 | 64-82 kt |
| 2 | 83-95 kt |
| 3 | 96-112 kt |
| 4 | 113-136 kt |
| 5 | 137 kt or higher |

<a id="directory-overview"></a>

## Directory Overview
**analysis_data** - contains data files used in the Power BI dashboard and intensification analysis, files created from the lightning burst identification code

**data_pipeline** - contains notebooks used to upload, clean, process, and create data files used in the analysis portion of this project

**exploratory_analysis** - contains notebooks as well as visualizations created in the exploratory analysis portion of this project

**intensification_analysis** - contains notebooks and visualizations for the statistical analysis of the relationship between lightning bursts and TC intensification change

**lightning_burst_identification** - contains notebooks, datasets, and visualizations created in the statistical identification of inner core and rainband lightning bursts at both the individual TC and basin levels

### Directory Structure
```
.
├── analysis_data
|   └── README.md
|   └── innercore_lightning_data.csv
|   └── innercore_bursts.csv
|   └── innercore_threshold_summary.csv
|   └── rainband_lightning_data.csv
|   └── rainband_bursts.csv
|   └── rainband_threshold_summary.csv
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
|   └── innercore_burst_w_intensification.ipynb
|   └── rainband_burst_w_intensification.ipynb
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
├── LICENSE
└── README.md
```

Detailed documentation on code requirements and file outputs can be found in each folder's README file.

<a id="deliverables"></a>

## Deliverables

### Data Pipeline

### Lightning Burst Identification
- Lightning burst identification Jupyter Notebooks
- Lightning burst identification Power BI dashboard

### Intensification Statistical Analysis
- jupyter notebooks
- written report ??

<a id="dependencies"></a>

## Dependencies

<a id="future-work"></a>

## Future Work
Due to time constraints, we note the following as future work to continue building on the analysis presented in this repository:
- Lightning burst identification accuracy improvements:
    - Removing landfall from lightning burst analysis - remove data points where TC storm center is within 100km of land
    - Include entire storm in lightning burst visualizations - currently not fully representing the entirety of storms where inner core/rainband lightning is present for only a subset of the storm length (e.g. if a TC lasts 4 days but only has inner core lightning for the first 3, the last day is not included in the plot)
- Lightning burst dashboard improvements:
    - Alternatives to using Python visualizations in Power BI due to limitations (developers need Python installed, cannot publish to Power BI web, etc.)
    - Prevent burst markers from overlapping when there are multiple markers on one lightning bin for readability
- Inclusion of GLM data:
    - WWLLN data tends to include more intense lightning events due to the nature of the data collection methods. Using GLM data to perform the same analysis may yield more insightful results.
- Machine learning in lightning burst detection:
    - The use of machine learning to detect lightning bursts may show unexpected patterns, and can be a more flexible method of identifying lightning bursts than the ones used in this project.