# Lightning-Analysis
UW MSDS Capstone Project with Northwest Research Associates

## Table of Contents
* [Objective](#objective)
* [Background Information](#background)
* [Directory Overview](#directory-overview)
* [Repository Components](#deliverables)
* [Dependencies and Setting Up the Repository](#dependencies)
  * [Environment](#environment)
  * [Data](#data)
* [Future Work](#future-work)
* [Acknowledgements](#acknowledgements)

| Team Member  | GitHub                                   |
|------------------|--------------------------------------|
| April Gao       | [aprilggg](https://github.com/aprilggg)|
| Elaine Zhang     | [ezhang17](https://github.com/ezhang17)|
| Janice Kim      | [ymkim814](https://github.com/ymkim814)|

<a id="objective"></a>

## Objective
[wip]
<a id="background"></a>

## Background Information
[wip]
NWRA provided [WWLLN](https://wwlln.net/) and track data from 2010-2020, with 984 total TCs in the dataset. For this project, we only look at TCs of category 1 or higher (as defined by the Saffir-Simpson Hurricane Wind Scale provided below), leaving us with 479 TCs for the lightning burst evaluation.

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

About shear - only use for rainband bc rainband lightning tends to occur in a specific quadrant, shear quadrants behave differently

** insert the graphic here for the shear quad definition + formulas

<img src="shear_quadrant_graphic.png" width="200" height="200">

<a id="directory-overview"></a>

## Directory Overview

**analysis_data** - contains data files used in the Power BI dashboard and intensification analysis created from the lightning burst identification code

**data_pipeline** - contains notebooks used to upload, clean, process, filter, and create data files used in the analysis portion of this project

**exploratory_analysis** - contains notebooks as well as visualizations created in the exploratory analysis portion of this project

**intensification_analysis** - contains notebooks and visualizations for the statistical analysis of the relationship between lightning bursts and TC intensification change

**lightning_burst_identification** - contains notebooks, datasets, and visualizations created in the statistical identification of inner core and rainband lightning bursts at both the individual TC and basin levels

Intermediate files that are too large to upload to Github can be found here, along with the individual TC visualizations created in the lightning burst identification stage of the project: [Google Drive](https://drive.google.com/drive/folders/1VxhljPNirGQL2jP3-bbhCS94neifmepc?usp=sharing)

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
|       └── innercore_timebin_joined.csv
|       └── rainband_shear_timebin_joined.csv
|   └── intermediate_data
|       └── ...
|   └── README.md
|   └── data_file_cleaning.ipynb
|   └── data_processing.ipynb
|   └── data_upload.ipynb
|   └── rainband_data.ipynb
├── exploratory_analysis
|   └── README.md
|   └── basin_descriptive_analysis.ipynb
|   └── exploratory_analysis.ipynb
├── intensification_analysis
|   └── README.md
|   └── innercore_burst_w_intensification.ipynb
|   └── rainband_burst_w_intensification.ipynb
├── lightning_burst_identification
|   └── data
|       └── ...
|   └── visualizations
|       └── ...
|   └── README.md
|   └── __init__.py
|   └── dashboard_documentation.md
|   └── lightning_burst_dashboard.pbix
|   └── lightning_threshold_functions.py
|   └── lightning_threshold_innercore.ipynb
|   └── lightning_threshold_rainband.ipynb
|   └── vis_upload.ipynb
├── LICENSE
├── README.md
├── requirement.yml
├── requirement_simplified.yml
└── shear_quadrant_graphic.png
```

Detailed documentation on code requirements and file outputs can be found in each folder's README file.

<a id="deliverables"></a>

## Repository Components
 [wip]
### Data Pipeline

### Lightning Burst Identification
- Lightning burst identification Jupyter Notebooks
- Lightning burst identification Power BI dashboard

### Intensification Statistical Analysis
- jupyter notebooks
- written report ??


<a id="dependencies"></a>

## Dependencies and Setting Up the Repository

This repository can be cloned to local following these [instructions](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).

<a id="environment"></a>

### Environment
This repository consists mostly of Jupyter Notebook files. We include [requirement.yml](requirement.yml) and [requirement_simplified.yml](requirement_simplified.yml) files for user convenience.

The code in this repository requires the following installations:
- Python [Official Python Installation Documentation](https://www.python.org/downloads/)

We recommend using [conda](https://docs.conda.io/projects/conda/en/latest/index.html) to [set up the environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file) using the provided `.yml` files in the repository.

**A Simple Guide to Setting Up an Environment With Conda:**
1. Make sure you have the following:
    - [requirement.yml](requirement.yml) or [requirement_simplified.yml](requirement_simplified.yml)
    - [Miniconda or Anaconda installation](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html)
2. Create the environment from the [requirement.yml](requirement.yml) file - run the following in your terminal:
```
conda env create -f requirement.yml
```
Use either `requirement.yml` or `requirement_simplified.yml` in this code depending on your preferences.
3. Activate the new environment in your terminal:
```
conda activate nwra_capstone
```
4. Verify that the new environment was installed correctly - look for `nwra_capstone`:
```
conda env list
```

<a id="data"></a>

### Data
 [wip]

<a id="future-work"></a>

## Future Work
Due to time constraints, we note the following as future work to continue building on the analysis presented in this repository:
- Lightning burst identification accuracy improvements:
    - Removing landfall from lightning burst analysis - remove data points where TC storm center is within 100km of land since landfall is associated with higher lightning activity regardless of storm intensification stage
- Lightning burst dashboard improvements:
    - Alternatives to using Python visualizations in Power BI due to limitations (developers need Python installed, cannot publish to Power BI web, etc.)
    - Prevent burst markers from overlapping when there are multiple markers on one lightning bin for readability
- Inclusion of GLM data:
    - WWLLN data tends to include more intense lightning strokes due to the nature of the data collection methods. Using GLM data to perform the same analysis may yield more insightful results.
- Machine learning in lightning burst detection:
    - The use of machine learning to detect lightning bursts may show unexpected patterns, and can be a more flexible method of identifying lightning bursts than the ones used in this project.

<a id="acknowledgements"></a>

## Acknowledgements

Thank you to our sponsors, Dr. Jeremy Thomas and Dr. Natalia Solorzano at NWRA, for making this project happen.

WWLLN Data Acknowledgment - The authors are using data from the World Wide Lightning Location Network, a collaborative consortium of over 70 worldwide collaborators, managed at the University of Washington.