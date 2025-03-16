# Lightning Burst Identification

* [Directory Overview](#directory-overview)
* [Lightning Burst Detection Methods](#methods)
* [Code Requirements](#requirements)
* [Output Files](#outputs)
    * [Analysis Data](#analysis-data)
    * [Lightning Burst Threshold Visualizations](#visualizations)
    * [Lightning Burst Threshold Dashboard](#dashboard)
    * [Inner Core Basin-Level Data](#basin-data)

<a id="directory-overview"></a>

### Directory Overview

The files in this directory include:
- **`dashboard_documentation.ipynb`**
    - documentation for Power BI dashboard (`lightning_burst_dashboard.pbix`)
    - includes user guide and developer guide
- **`lightning_burst_dashboard.pbix`**
    - Power BI dashboard visualizing detected bursts in graphical and tabular form
    - includes both inner core and rainband lightning types
- **`lightning_threshold_functions.py`**
    - contains functions used in both inner core and rainband analyses
    - functions include:
        - threshold calculation
        - threshold application
        - plotting wind/pressure/lightning/detected bursts
        - generating a TC-level summary
        - plotting basin-level threshold distributions
        - calculating basin-level thresholds
- **`lightning_threshold_innercore.ipynb`**
    - applies threshold calculation, TC plotting functions to inner core dataset
    - identifies lightning bursts at individual TC level and basin level (excluding CPAC)
    - generates .png files of TC wind/pressure/lightning/burst plots
    - creates data files used in intensification analysis and dashboard ([analysis_data/](../analysis_data/))
- **`lightning_threshold_rainband.ipynb`**
    - applies threshold calculation, TC plotting functions to rainband dataset
    - identifies lightning bursts at individual TC level and sorts them into shear quadrants
    - generates .png files of TC wind/pressure/lightning/burst plots at both overall and shear quadrant granularity
    - creates data files used in intensification analysis and dashboard ([analysis_data/](../analysis_data/))
- **`vis_upload.ipynb`**
    - uploads visualizations in `visualizations/` directory to specified Google Drive folder
    - requires [Google Drive API](https://developers.google.com/drive/api/guides/about-sdk)
- **`visualizations/`**
    - contains visualizations generated in `lightning_threshold_innercore.ipynb` and `lightning_threshold_rainband.ipynb`
    - more details in this [section](#lightning-burst-threshold-visualizations)
- **`data/`**
    - contains inner core basin-level data files generated in `lightning_threshold_innercore.ipynb`
    - these data files are not used in subsequent intensification analyses
    - more details in this [section](#inner-core-basin-level-data)

<a id="methods"></a>

### Lightning Burst Detection Methods
We define a lightning "burst" as a time period, specifically a 30-minute time bin, with a spike in lightning relative to the storm's overall lightning.  In this section of the project, we seek to calculate lightning burst thresholds using statistical methods for each storm, and also explore basin-level lightning burst thresholds.
We log transform the lightning counts per time bin and then calculate a lightning burst threshold based off each storm's log-lightning count distribution. Note that thresholds are evaluated off the log-lightning count, and threshold numbers are also represented on the log scale. We do not include counts associated with wind speeds less than 40 knots, and we do not include time bins with 0 lightning counts in the calculation of our thresholds.

In the lightning burst detection process, we use the following 6 threshold methods (referred to by the names in parentheses hereafter):
- [Median Absolute Deviation](https://en.wikipedia.org/wiki/Median_absolute_deviation)
    - MAD is defined as: `MAD = median(|X_i - median(X)|)` where:
        - `X_i` are the data points
        - `median(X)` is the median of the dataset
        - `|X_i - median(X)|` represents absolute deviations from the median
    - 4 MAD (**MAD1**)
        - This method sets the threshold to be 4 times the median absolute deviation (MAD) above the median log-lightning count
        - Equation: threshold = median + 4 * MAD
    - 5 MAD (**MAD2**)
        - This method sets the threshold to be 5 times the median absolute deviation (MAD) above the median log-lightning count
        - Equation: threshold = median + 5 * MAD
- [Interquartile Range](https://en.wikipedia.org/wiki/Interquartile_range)
    - IQR is defined as: `IQR = Q_3 - Q_1` where:
        - `Q_1` = First quartile (25th percentile)
        - `Q_3` = Third quartile (75th percentile)
        - `IQR` = Range covering the middle 50% of the data
    - 1 IQR (**IQR1**)
        - This method sets the threshold to be 1 interquartile range higher than the upper quartile (Q3) log-lightning count
        - Equation: threshold = Q3 + 1 * IQR
    - 1.5 IQR (**IQR2**)
        - This method sets the threshold to be 1.5 interquartile ranges higher than the upper quartile (Q3) log-lightning count
        - Equation: threshold = Q3 + 1.5 * IQR
- [Lognormal](https://en.wikipedia.org/wiki/Log-normal_distribution)
    - IQR is defined as: `SD = e^(μ + (σ² / 2)) * √(e^(σ²) - 1)` where:
        - `\mu` = Mean of the associated normal distribution
        - `\sigma` = Standard deviation of the associated normal distribution
        - `e` = Euler's number (≈ 2.718)
    - 2 Standard Deviations (**LOGN1**)
        - This method sets the threshold to be 2 standard deviations higher than the mean log-lightning count
        - Equation: threshold = mean + 2 * std dev
    - 3 Standard Deviations (**LOGN2**)
        - This method sets the threshold to be 3 standard deviations higher than the mean log-lightning count
        - Equation: threshold = mean + 3 * std dev

**note that all methods use the log-lightning count as base (e.g. median refers to median log-lightning count, not median lightning count)


<a id="requirements"></a>

### Code Requirements
The lightning burst identification notebooks require the following libraries not built in to Python:
- pandas
- polars
- numpy
- matplotlib
- scipy

The `lightning_threshold_innercore.ipynb` and `lightning_threshold_rainband.ipynb` files import functions from the `lightning_threshold_functions.py` file.

The `vis_upload.ipynb` notebook requires the following libraries not built in to Python:
- pydrive

<a id="outputs"></a>

### Output Files
The code in this directory outputs data files into both the [lightning_burst_identification/data/](data/) and [analysis_data/](../analysis_data/) directories. Inner core basin-level threshold evaluations are in the [lightning_burst_identification/data/](data/) folder, and individual-level threshold evaluation datasets are in the [analysis_data/](../analysis_data/) folder, later used in both the dashboard and TC intensification statistical analysis. Individual TC visualizations are saved as .png files in the [visualizations/](visualizations/) folder.

<a id="analysis-data"></a>

#### Analysis Data

The following data files are generated and saved to the `analysis_data/` directory:
* innercore_bursts.csv
* innercore_lightning_data.csv
* innercore_threshold_summary.csv
* rainband_bursts.csv
* rainband_lightning_data.csv
* rainband_threshold_summary.csv

Column details for these files can be found in [analysis_data/README.md](../analysis_data/README.md)

<a id="visualizations"></a>

#### Lightning Burst Threshold Visualizations
Visualizations in the [visualizations directory](visualizations/) can also be found in this [Google Drive folder](https://drive.google.com/drive/folders/1iIZx4ThnT8KyQc6pDPAemjYb0Ma_OFd_?usp=drive_link). There are 2172 files in the `visualizations` folder. Files are named with the storm code (basin_year_num) followed by the storm name and one of the 6 possible file patterns below:

| Lightning Visualization Type   | Background Color-Coding Type  | File Name Ends With |
| -------- | ------- | ------- |
| Inner Core | Current Category (5 categories) | innercore_c5.png |
| Inner Core | Intensification Stages (3 categories) | innercore_i3.png |
| Rainband | Current Category (5 categories) | rainband_c5.png |
| Rainband | Intensification Stages (3 categories) | rainband_i3.png |
| Rainband Shear (2x2) | Current Category (5 categories) | rainband_shear_c5.png |
| Rainband Shear (2x2) | Intensification Stages (3 categories) | rainband_shear_i3.png |

*note that not all TCs have shear data available, and as such will not have been included in rainband analysis

The current category background color-coding type includes categories 0-5, while the intensification stages color-coding type includes the simplified intensification stage bins (Weakening, Neutral, Intensifying). The visualizations in this directory are created in [lightning_threshold_innercore.ipynb](lightning_threshold_innercore.ipynb) and [lightning_threshold_rainband.ipynb](lightning_threshold_rainband.ipynb), which use the functions in [lightning_threshold_functions.py](lightning_threshold_functions.py) to graph each TC. Note that the plotting functions also include a 5 intensification stage color-coding option that we did not generate for this directory.

<a id="dashboard"></a>

#### Lightning Burst Threshold Dashboard
The visualizations in the `visualizations/` directory are also available in the Power BI dashboard `lightning_burst_dashboard.pbix`. Detailed documentation for this dashboard (including a user guide and developer guide) can be found [here](dashboard_documentation.md).

<a id="basin-data"></a>

#### Inner Core Basin-Level Data

The files in this section use the idea of an "effective" threshold - that is, a threshold value where at least one time bin is marked as a burst when applied to a TC individually. This allows the basin-level threshold to consider only thresholds that actually mark a burst, and prevent the basin-level threshold value from being too high for the average storm in the basin.

The `lightning_threshold_innercore.ipynb` notebook creates the following files for each basin (fill in {basin name} with either ATL, EPAC, IO, SHEM, or WPAC):

*Note that all threshold values, mean, median, standard deviation, min, max of threshold values are in log-lightning counts. These should **not** be interpreted as "any time bin with more than x lightning counts is a burst", rather "any time bin with more than x **log-lightning counts** is a burst".

**innercore_{basin name}_basin_bursts_summary.csv**

Contains basin-level summary statistics for thresholds, as well as calculated basin category group level threshold values at various standard deviations from the summary statistic (mean/median). Expect 3 rows per threshold method, with 6 threshold methods per basin (18 rows per basin).

| Column Name   | Data Type | Description |
| -------- | ------- | ------- |
| Basin | String | Either ATL, EPAC, IO, SHEM, or WPAC |
| Category Group | String | Either 0-2, 1-2, or 3-5 |
| Threshold | String | Either mad1, mad2, iqr1, iqr2, logn1, or logn2, represents threshold calculation method |
| Mean | Float | Mean log10 transformed threshold value across all TCs in basin for threshold method |
| Std Dev | Float | Standard deviation for log10 transformed threshold values across all TCs in basin for threshold method |
| Median | Float | Median log10 transformed threshold value across all TCs in basin for threshold method |
| Min | Float | Smallest log10 transformed threshold value across all TCs in basin for threshold method |
| Max | Float | Largest log10 transformed threshold value across all TCs in basin for threshold method |
| Burst Count | Integer | Number of time bins marked as a burst for this threshold method across all TCs in basin |
| Timebin Count | Integer | Number of time bins considered in threshold evaluation across all TCs in basin (does not include time bins with wind speeds less than 40 knots and time bins with no lightning) |
| Burst Percentage | Float | Percent of evaluated time bins marked as a burst using this threshold method |
| Basin-Category Effective Threshold (Mean-Based) 2 SD | Float | Effective thresholds mean + 2*effective thresholds standard deviation |
| Basin-Category Effective Threshold (Median-Based) 2 SD | Float | Effective thresholds median + 2*effective thresholds standard deviation |
| Basin-Category Effective Threshold Bursts (Mean-Based) 2 SD | Integer | Number of evaluated time bins marked as a burst using the effective mean 2 SD threshold |
| Basin-Category Effective Threshold Burst Percentage (Mean-Based) 2 SD	| Float | Percent of evaluated time bins marked as a burst using the effective mean 2 SD threshold |
| Basin-Category Effective Threshold Bursts (Median-Based) 2 SD	| Integer | Number of evaluated time bins marked as a burst using the effective median 2 SD threshold |
| Basin-Category Effective Threshold Burst Percentage (Median-Based) 2 SD	| Float | Percent of evaluated time bins marked as a burst using the effective median 2 SD threshold |
| Basin-Category Effective Threshold (Mean-Based) 1.5 SD	| Float | Effective thresholds mean + 1.5*effective thresholds standard deviation |
| Basin-Category Effective Threshold (Median-Based) 1.5 SD	| Float | Effective thresholds median + 1.5*effective thresholds standard deviation |
| Basin-Category Effective Threshold Bursts (Mean-Based) 1.5 SD	| Integer | Number of evaluated time bins marked as a burst using the effective mean 1.5 SD threshold |
| Basin-Category Effective Threshold Burst Percentage (Mean-Based) 1.5 SD	| Float | Percent of evaluated time bins marked as a burst using the effective mean 1.5 SD threshold |
| Basin-Category Effective Threshold Bursts (Median-Based) 1.5 SD | Integer | Number of evaluated time bins marked as a burst using the effective median 1.5 SD threshold |
| Basin-Category Effective Threshold Burst Percentage (Median-Based) 1.5 SD | Float | Percent of evaluated time bins marked as a burst using the effective median 1.5 SD threshold |
| Mean (Effective) | Float | Mean effective threshold value |
| Median (Effective) | Float | Median effective threshold value |
| Std Dev (Effective) | Float | Standard deviation of effective threshold values |

**innercore_{basin name}_basin_threshold_bursts.csv**

Contains time bin level data for each storm, with columns denoting if the particular time bin is detected as a burst using the basin-level effective threshold. Note that threshold values will be the same across TCs for each basin/category group pair.

| Column Name   | Data Type | Description |
| -------- | ------- | ------- |
| time_bin | Datetime | 30 minute bin |
| storm_code | String | formatted as basin_year_stormnumber|
| lightning_count | Integer | number of inner core lightning strokes in time bin |
| year | Integer | |
| month | Integer |  |
| day | Integer | |
| hour | Integer | |
| minute | Integer | |
| lat | Float | TC storm center |
| lon | Float | TC storm center |
| pressure | Integer | |
| knots | Integer | wind speed in knots |
| storm_name | String | |
| category | Integer | TC category based off max wind speeds |
| basin | String | |
| minute_right | Integer | |
| 24_hour_knots_diff | Float | forward-looking change in wind speed |
| 24_hour_pressure_diff | Float | forward-looking change in pressure |
| Current_Category | String | category calculated based off the wind speed of the time bin |
| Intensification_Category_5 | String | includes rapidly intensifying/weakening |
| log_lightning_count | Float | log10 transformed lightning count |
| Intensification_Category_3 | String | combines rapidly intensifying with intensifying, rapidly weakening with weakening |
| burst_iqr1 | Boolean | denotes if IQR1 method detected timebin as burst |
| burst_iqr2 | Boolean | denotes if IQR2 method detected timebin as burst |
| iqr1_threshold | Float | log10 transformed basin-level effective threshold for IQR1 method burst |
| iqr2_threshold | Float | log10 transformed basin-level effective threshold for IQR2 method burst |
| burst_mad1 | Boolean | denotes if MAD1 method detected timebin as burst |
| burst_mad2 | Boolean | denotes if MAD2 method detected timebin as burst |
| mad1_threshold | Float | log10 transformed basin-level effective threshold for MAD1 method burst |
| mad2_threshold | Float | log10 transformed basin-level effective threshold for MAD2 method burst |
| burst_logn1 | Boolean | denotes if Lognormal1 method detected timebin as burst |
| burst_logn2 | Boolean | denotes if Lognormal2 method detected timebin as burst |
| logn1_threshold | Float | log10 transformed basin-level effective threshold for LOGN1 method burst |
| logn2_threshold | Float | log10 transformed basin-level effective threshold for LOGN2 method burst |
| std_dev | Float | Number of standard deviations from the mean/median used to calculate the basin-level threshold |
| threshold_calc_type | String | Either "mean" or "median", denotes the statistic used to calculate the basin-level threshold |
| category_group | String | Either 0-2, 1-2, or 3-5 |


**innercore_{basin name}_basin_threshold_tc_summary.csv**

Contains TC-level statistics for each basin/category group threshold method - number of bursts detected, log10 transformed basin-level effective threshold values, burst detection percentages, etc. Expect 3 rows per TC - each TC's time bins are split into 0-2, 1-2, and 3-5 current category groups.

| Column Name   | Data Type | Description |
| -------- | ------- | ------- |
| storm_code | String | formatted as basin_year_stormnumber|
| storm_name | String | |
| mad1_bursts | Integer | number of MAD1 detected bursts for this TC |
| mad2_bursts | Integer | number of MAD2 detected bursts for this TC |
| mad1_threshold | Float | log10 transformed basin-level effective threshold for MAD1 method burst |
| mad2_threshold | Float | log10 transformed basin-level effective threshold for MAD2 method burst |
| iqr1_bursts | Integer | number of IQR1 detected bursts for this TC |
| iqr2_bursts | Integer | number of IQR2 detected bursts for this TC |
| iqr1_threshold | Float | log10 transformed basin-level effective threshold for IQR1 method burst |
| iqr2_threshold | Float | log10 transformed basin-level effective threshold for IQR2 method burst |
| logn1_bursts | Integer | number of LOGN1 detected bursts for this TC |
| logn2_bursts | Integer | number of LOGN2 detected bursts for this TC |
| logn1_threshold | Float | log10 transformed basin-level effective threshold for LOGN1 method burst |
| logn2_threshold | Float | log10 transformed basin-level effective threshold for LOGN2 method burst |
| total_bins | Integer | number of time bins included in lightning burst identification analysis |
| mad1_prop | Float | percent of time bins detected as lightning burst using MAD1 method |
| mad2_prop | Float | percent of time bins detected as lightning burst using MAD2 method |
| iqr1_prop | Float | percent of time bins detected as lightning burst using IQR1 method |
| iqr2_prop | Float | percent of time bins detected as lightning burst using IQR2 method |
| logn1_prop | Float | percent of time bins detected as lightning burst using LOGN1 method |
| logn2_prop | Float | percent of time bins detected as lightning burst using LOGN2 method |
| std_dev | Float | Number of standard deviations from the mean/median used to calculate the basin-level threshold |
| threshold_calc_type | String | Either "mean" or "median", denotes the statistic used to calculate the basin-level threshold |
| category_group | String | Either 0-2, 1-2, or 3-5 |

The combined files (all basins in one file) follow the same naming convention and just leave out a specific basin name from the file name. Column structures are the same. Use these files for comparisons between basins:
- innercore_basin_bursts_summary.csv
- innercore_basin_threshold_bursts.csv
- innercore_basin_threshold_tc_summary.csv