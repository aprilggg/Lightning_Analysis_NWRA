# Intensification Analysis

* [About Directory](#about)
* [Code Requirements](#requirements)
* [Methods](#methods)

<a id="about"></a>

### About Directory
This folder contains files for analyzing lightning data in relation to tropical cyclone intensification. It includes statistical tests and visualizations to examine distribution patterns across different detection methods, cyclone categories, and ocean basins for both the inner-core and rainband regions.

<a id="requirements"></a>

### Code Requirements
The notebooks in this directory require the following libraries not built in to Python:
- matplotlib
- numpy
- pandas
- polars
- scipy
- seaborn

The notebooks require the following data files in the [analysis_data/](../analysis_data/) folder:
- Inner core dataset: `innercore_bursts.csv`
  - Used by: `innercore_burst_w_intensification.ipynb`
  - Contains: Lightning measurements from storm inner core
- Rainband dataset: `rainband_bursts.csv`
  - Used by: `rainband_burst_w_intensification.ipynb`
  - Contains: Lightning data from outer rainbands

<a id="methods"></a>

### Methods
We focus on the IQR1, IQR2, and LOGN1 methods for this analysis. We determined the MAD method to be too volatile, and the LOGN2 method to set the threshold consistently too high. Refer [here](../lightning_burst_identification/README.md#lightning-burst-detection-methods) for more details on the three methods not included in this analysis.

- [Interquartile Range](https://en.wikipedia.org/wiki/Interquartile_range) - 1 IQR (**IQR1**)
    - This method sets the threshold to be 1 interquartile range higher than the upper quartile (Q3) log-lightning count
    - Equation: threshold = Q3 + 1 * IQR
- Interquartile Range - 1.5 IQR (**IQR2**)
    - This method sets the threshold to be 1.5 interquartile ranges higher than the upper quartile (Q3) log-lightning count
    - Equation: threshold = Q3 + 1.5 * IQR
- [Lognormal](https://en.wikipedia.org/wiki/Log-normal_distribution) - 2 Standard Deviations (**LOGN1**)
    - This method sets the threshold to be 2 standard deviations higher than the mean log-lightning count
    - Equation: threshold = mean + 2 * std dev

We perform chi-squared tests to determine if bursts are detected differently for each of the intensification stages (Weakening, Neutral, Intensifying) and plot heatmaps of the burst proportion distributions to identify which intensification stage is associated with most of the detected bursts across all lightning, basins, current categories, and grouped categories. Note that the data includes an intensification category called "Unidentified" - this is attributed to the last 24 hours of a TC where there is not a 24-hour forward-looking wind speed difference and thereby we cannot assign an intensification stage. For more details on intensification stage and current category, refer to this [README](../README.md#background-information). Our category 0 includes wind speeds from 40-64 knots, as we did not consider data associated with wind speeds less than 40 knots in our lightning burst identification activity.