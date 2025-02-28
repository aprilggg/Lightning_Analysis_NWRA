## Visualization Data
This folder contains the files used to power the visualizations in the Power BI dashboard.

### Data Schema


#### innercore_bursts.csv
This dataset contains the bursts detected for the inner core data using the 6 threshold methods at the individual TC level. This dataset powers the marks on the dashboard denoting if a particular time bin had a burst of lightning.

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
| Intensification_Category_3 | String | |


#### innercore_threshold_summary.csv
This dataset contains an aggregated summary of each TC's individual inner core lightning burst detection. Each TC has only one row in this dataset.

#### rainband_bursts.csv
need to fill in with schema and description
#### rainband_lightning_data.csv

#### rainband_threshold_summary.csv