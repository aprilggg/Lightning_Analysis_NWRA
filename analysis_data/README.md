## Analysis Data
This folder contains the files used to power the visualizations in the Power BI dashboard and the statistical analyses in the `intensification_analysis` directory. All data files in this directory are created using the two notebooks in the `lightning_burst_identification` directory.

### Data Files and Schema
* [innercore_bursts.csv](#innercore-bursts)
* [innercore_lightning_data.csv](#innercore-lightning)
* [innercore_threshold_summary.csv](#innercore-summary)
* [rainband_bursts.csv](#rainband-bursts)
* [rainband_lightning_data.csv](#rainband-lightning)
* [rainband_threshold_summary.csv](#rainband-summary)

<a id="innercore-bursts"></a>

#### innercore_bursts.csv
This dataset contains the bursts detected for the inner core data using the 6 threshold methods at the individual TC level. This dataset powers the marks on the dashboard denoting if a particular time bin had a burst of lightning. Note that this dataset only contains time bins with lightning counts greater than 0.

| Column Name   | Data Type | Description |
| -------- | ------- | ------- |
| time_bin | Datetime | 30 minute bin |
| storm_code | String | formatted as basin_year_stormnumber|
| lightning_count | Integer | number of inner core lightning events in time bin |
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
| iqr1_threshold | Float | log10 transformed threshold for IQR1 method burst |
| iqr2_threshold | Float | log10 transformed threshold for IQR2 method burst |
| burst_mad1 | Boolean | denotes if MAD1 method detected timebin as burst |
| burst_mad2 | Boolean | denotes if MAD2 method detected timebin as burst |
| mad1_threshold | Float | log10 transformed threshold for MAD1 method burst |
| mad2_threshold | Float | log10 transformed threshold for MAD2 method burst |
| burst_logn1 | Boolean | denotes if Lognormal1 method detected timebin as burst |
| burst_logn2 | Boolean | denotes if Lognormal2 method detected timebin as burst |
| logn1_threshold | Float | log10 transformed threshold for LOGN1 method burst |
| logn2_threshold | Float | log10 transformed threshold for LOGN2 method burst |

<a id="innercore-lightning"></a>

#### innercore_lightning_data.csv
This dataset provides the lightning count (in 30 minute bins), wind, and pressure data for the visualization for inner core lightning only. This dataset also provides the intensification category and current category used to color-code the background of the visualizations.

| Column Name   | Data Type | Description |
| -------- | ------- | ------- |
| time_bin | Datetime | 30 minute bin |
| storm_code | String | formatted as basin_year_stormnumber|
| lightning_count | Integer | number of inner core lightning events in time bin |
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


<a id="innercore-summary"></a>

#### innercore_threshold_summary.csv
This dataset contains an aggregated summary of each TC's individual inner core lightning burst detection. Each TC has only one row in this dataset.

| Column Name   | Data Type | Description |
| -------- | ------- | ------- |
| storm_code | String | formatted as basin_year_stormnumber|
| storm_name | String | |
| mad1_bursts | Integer | number of MAD1 detected bursts for this TC |
| mad2_bursts | Integer | number of MAD2 detected bursts for this TC |
| mad1_threshold | Float | log10 transformed threshold for MAD1 method burst |
| mad2_threshold | Float | log10 transformed threshold for MAD2 method burst |
| iqr1_bursts | Integer | number of IQR1 detected bursts for this TC |
| iqr2_bursts | Integer | number of IQR2 detected bursts for this TC |
| iqr1_threshold | Float | log10 transformed threshold for IQR1 method burst |
| iqr2_threshold | Float | log10 transformed threshold for IQR2 method burst |
| logn1_bursts | Integer | number of LOGN1 detected bursts for this TC |
| logn2_bursts | Integer | number of LOGN2 detected bursts for this TC |
| logn1_threshold | Float | log10 transformed threshold for LOGN1 method burst |
| logn2_threshold | Float | log10 transformed threshold for LOGN2 method burst |
| total_bins | Integer | number of time bins included in lightning burst identification analysis |
| mad1_prop | Float | percent of time bins detected as lightning burst using MAD1 method |
| mad2_prop | Float | percent of time bins detected as lightning burst using MAD2 method |
| iqr1_prop | Float | percent of time bins detected as lightning burst using IQR1 method |
| iqr2_prop | Float | percent of time bins detected as lightning burst using IQR2 method |
| logn1_prop | Float | percent of time bins detected as lightning burst using LOGN1 method |
| logn2_prop | Float | percent of time bins detected as lightning burst using LOGN2 method |

<a id="rainband-bursts"></a>

#### rainband_bursts.csv
This dataset contains the bursts detected for the rainband data using the 6 threshold methods at the individual TC level. This dataset powers the marks on the dashboard denoting if a particular time bin had a burst of lightning. Note that this dataset splits each timebin into the 4 shear quadrants - UR, UL, DR, DL and only contains time bins with lightning counts greater than 0.

| Column Name   | Data Type | Description |
| -------- | ------- | ------- |
| time_bin | Datetime | 30 minute bin |
| shear_quad | String | shear quadrant |
| storm_code | String | formatted as basin_year_stormnumber|
| lightning_count | Integer | number of inner core lightning events in time bin |
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
| iqr1_threshold | Float | log10 transformed threshold for IQR1 method burst |
| iqr2_threshold | Float | log10 transformed threshold for IQR2 method burst |
| burst_mad1 | Boolean | denotes if MAD1 method detected timebin as burst |
| burst_mad2 | Boolean | denotes if MAD2 method detected timebin as burst |
| mad1_threshold | Float | log10 transformed threshold for MAD1 method burst |
| mad2_threshold | Float | log10 transformed threshold for MAD2 method burst |
| burst_logn1 | Boolean | denotes if Lognormal1 method detected timebin as burst |
| burst_logn2 | Boolean | denotes if Lognormal2 method detected timebin as burst |
| logn1_threshold | Float | log10 transformed threshold for LOGN1 method burst |
| logn2_threshold | Float | log10 transformed threshold for LOGN2 method burst |


<a id="rainband-lightning"></a>

#### rainband_lightning_data.csv
This dataset provides the lightning count (in 30 minute bins), wind, and pressure data for the visualization for rainband lightning only. This dataset also provides the intensification category and current category used to color-code the background of the visualizations.

| Column Name   | Data Type | Description |
| -------- | ------- | ------- |
| time_bin | Datetime | 30 minute bin |
| shear_quad | String | shear quadrant |
| storm_code | String | formatted as basin_year_stormnumber|
| lightning_count | Integer | number of rainband lightning events in time bin |
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


<a id="rainband-summary"></a>

#### rainband_threshold_summary.csv
This dataset contains an aggregated summary of each TC's individual rainband lightning burst detection. Each TC will have up to 4 rows in this dataset, one per shear quadrant.

| Column Name   | Data Type | Description |
| -------- | ------- | ------- |
| storm_code | String | formatted as basin_year_stormnumber|
| storm_name | String | |
| shear_quad | String | shear quadrant |
| mad1_bursts | Integer | number of MAD1 detected bursts for this TC |
| mad2_bursts | Integer | number of MAD2 detected bursts for this TC |
| mad1_threshold | Float | log10 transformed threshold for MAD1 method burst |
| mad2_threshold | Float | log10 transformed threshold for MAD2 method burst |
| iqr1_bursts | Integer | number of IQR1 detected bursts for this TC |
| iqr2_bursts | Integer | number of IQR2 detected bursts for this TC |
| iqr1_threshold | Float | log10 transformed threshold for IQR1 method burst |
| iqr2_threshold | Float | log10 transformed threshold for IQR2 method burst |
| logn1_bursts | Integer | number of LOGN1 detected bursts for this TC |
| logn2_bursts | Integer | number of LOGN2 detected bursts for this TC |
| logn1_threshold | Float | log10 transformed threshold for LOGN1 method burst |
| logn2_threshold | Float | log10 transformed threshold for LOGN2 method burst |
| total_bins | Integer | number of time bins included in lightning burst identification analysis |
| mad1_prop | Float | percent of time bins detected as lightning burst using MAD1 method |
| mad2_prop | Float | percent of time bins detected as lightning burst using MAD2 method |
| iqr1_prop | Float | percent of time bins detected as lightning burst using IQR1 method |
| iqr2_prop | Float | percent of time bins detected as lightning burst using IQR2 method |
| logn1_prop | Float | percent of time bins detected as lightning burst using LOGN1 method |
| logn2_prop | Float | percent of time bins detected as lightning burst using LOGN2 method |