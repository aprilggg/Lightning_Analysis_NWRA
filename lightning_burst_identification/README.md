# Lightning Burst Identification

* [Directory Overview](#directory-overview)
* [Lightning Burst Detection Methods](#methods)
* [Code Requirements](#requirements)
* [Output Files](#outputs)

<a id="directory-overview"></a>

### Directory Overview

The notebooks in this directory include:
1. **`lightning_threshold_functions.py`**
    - contains functions used in both inner core and rainband analyses
    - functions include:
        - threshold calculation
        - threshold application
        - plotting wind/pressure/lightning/detected bursts
        - generating a TC-level summary
        - plotting basin-level threshold distributions
        - calculating basin-level thresholds
2. **`lightning_threshold_innercore.ipynb`**
    - applies threshold calculation, TC plotting functions to inner core dataset
    - identifies lightning bursts at individual TC level and basin level
3. **`lightning_threshold_rainband.ipynb`**
    - applies threshold calculation, TC plotting functions to rainband dataset
    - identifies lightning bursts at individual TC level and sorts them into shear quadrants

This directory also includes:
**`data/`**
    - innercore_atl_basin_bursts_summary.csv
    - innercore_atl_basin_threshold_bursts.csv
    - innercore_atl_basin_threshold_tc_summary.csv
    - innercore_basin_bursts_summary.csv
    - innercore_basin_threshold_bursts.csv
    - innercore_basin_threshold_tc_summary.csv
    - innercore_epac_basin_bursts_summary.csv
    - innercore_epac_basin_threshold_bursts.csv
    - innercore_epac_basin_threshold_tc_summary.csv
    - innercore_io_basin_bursts_summary.csv
    - innercore_io_basin_threshold_bursts.csv
    - innercore_io_basin_threshold_tc_summary.csv
    - innercore_shem_basin_bursts_summary.csv
    - innercore_shem_basin_threshold_bursts.csv
    - innercore_shem_basin_threshold_tc_summary.csv
    - innercore_wpac_basin_bursts_summary.csv
    - innercore_wpac_basin_threshold_bursts.csv
    - innercore_wpac_basin_threshold_tc_summary.csv

<a id="methods"></a>

### Lightning Burst Detection Methods
We log transform the lightning counts per time bin and then calculate a lightning burst threshold based off each storm's log-lightning count distribution. Note that thresholds are evaluated off the log-lightning count, and threshold numbers are also represented on the log scale. We do not include counts associated with wind speeds less than 40 knots, and we do not include time bins with 0 lightning counts in the calculation of our thresholds.

In the lightning burst detection process, we use the following 6 threshold methods (referred to by the names in parentheses hereafter):
- Mean Absolute Deviation - 4 MAD (**MAD1**)
    - This method sets the threshold to be 4 times the median absolute deviation above the median log-lightning count
    - Equation: threshold = median + 4 * MAD
- Mean Absolute Deviation - 5 MAD (**MAD2**)
    - This method sets the threshold to be 5 times the median absolute deviation above the median log-lightning count
    - Equation: threshold = median + 5 * MAD
- Interquartile Range - 1 IQR (**IQR1**)
    - This method sets the threshold to be 1 interquartile range higher than the upper quartile (Q3) log-lightning count
    - Equation: threshold = Q3 + 1 * IQR
- Interquartile Range - 1.5 IQR (**IQR2**)
    - This method sets the threshold to be 1.5 interquartile ranges higher than the upper quartile (Q3) log-lightning count
    - Equation: threshold = Q3 + 1.5 * IQR
- Lognormal - 2 Standard Deviations (**LOGN1**)
    - This method sets the threshold to be 2 standard deviations higher than the mean log-lightning count
    - Equation: threshold = mean + 2 * std dev
- Lognormal - 3 Standard Deviations (**LOGN2**)
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

<a id="outputs"></a>

### Output Files
The code in this directory outputs data files into both the `lightning_burst_identification/data/` and `analysis_data/` directories. Basin-level threshold evaluations are in the `lightning_burst_identification/data/` folder, and individual-level threshold evaluation datasets are in the `analysis_data/` folder, later used in both the dashboard and TC intensification statistical analysis.