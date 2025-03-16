# Lightning Burst Dashboard User & Development Guide

This document provides usage and development guides for the `lightning_burst_dashboard.pbix` Power BI dashboard included in this directory. This dashboard includes visualizations created in `lightning_threshold_innercore.ipynb` and `lightning_threshold_rainband.ipynb` and includes both inner core and rainband data.

* [Dependencies and Set Up](#dependencies)
* [User Guide](#user)
    * [Overview](#overview)
    * [Inner Core Visualizations](#inner-core)
    * [Rainband Visualizations](#rainband)
* [Developer Guide](#dev)
    * [Data Setup](#data)
    * [Dashboard Components](#components)
        * [Python Visualizations](#python)
* [Future Work and Improvements](#future)

<a id="dependencies"></a>

## Dependencies and Set Up

This dashboard requires [Power BI Desktop](https://learn.microsoft.com/en-us/power-bi/fundamentals/desktop-get-the-desktop). Users are not required to have the source data files on their local machine if the data does not need to be refreshed.

The [Python visualizations](https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-python-visuals) in this dashboard require [installation of Python](https://www.python.org/downloads/) and the following non-native Python libraries:
- pandas
- matplotlib

Install the above libraries by opening the terminal or command prompt and running the following:
```
pip install pandas matplotlib
```

Refer to the [Power BI Python scripts documentation](https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-python-scripts) for more details on Python script requirements in Power BI.

After installing Power BI Desktop and setting up the Python requirements, open the `lightning_burst_dashboard.pbix` file.

You will first see a pop-up asking if you wish to enable scripts - click Enable.

![enable scripts](images/dashboard_1.png)

<a id="user"></a>

## User Guide

In this section, we go over how to use and interpret the visualizations included in the dashboard.

<a id="overview"></a>

### Overview

The dashboard opens to this view with tabs at the bottom. Each tab contains a different set of visualizations and can be filtered using the slicer on the right-hand side. Slicers are synced between the inner core tabs and the rainband tabs.

![overview](images/dashboard_3.png)

#### Tabs
The dashboard includes 6 tabs:
- Inner Core TC Plots
- Inner Core TC Burst Data
- Rainband TC Plots
- Rainband Shear Quad - Intensification
- Rainband Shear Quad - Current Category
- Rainband TC Burst Data

#### Filtering the Dashboard
![slicer](images/dashboard_2.png)

Each tab includes a slicer to filter the data. Choose a specific TC by selecting the year, basin, and then the TC name. The number in parentheses next to the name denotes the TC's number. Visualizations are set up to only display one TC at a time.

![please select one TC](images/dashboard_12.png)

If more than one TC is selected accidentally on the graph views, the visualizations will display "Please select only one TC". This prevents the dashboard from attempting to graph more than one TC at a time, which may lead to the dashboard crashing due to the sheer amount of data loading at once.

#### Viewing Visualizations Individually
Each visualization can be shown individually by clicking on "Focus mode" in the menu at the upper right corner or lower right corner of the graph when hovering or clicking on the graph.

![focus mode](images/dashboard_10.png)

Clicking on "Focus mode" will show the chosen visualization on its own page. Select "Back to report" to return to the previous view.

![focus mode close](images/dashboard_11.png)

<a id="inner-core"></a>

### Inner Core Visualizations

The following tabs display inner core lightning data:
- Inner Core TC Plots
- Inner Core TC Burst Data

#### Inner Core TC Plots

![inner core tc plots](images/dashboard_4.png)

This tab displays inner core lightning detected bursts on intensification stage color-coded backgrounds on the top and current category color-coded backgrounds on the bottom. Each graph shows the lightning counts in gray, pressure in orange, and wind speed (knots) in blue for the whole duration of the selected TC (regardless of if the data was included in lightning burst threshold calculation). Each of the 6 burst identification methods is displayed with a differently colored marker.

For the intensification stage plot, we only display the 3-category intensification stages - Neutral, Intensifying, and Weakening. Rapidly Weakening and Rapidly Intensifying are combined with Weakening and Intensifying, respectively. The white background denotes the last 24 hours of the storm where we cannot calculate intensification stage using forward-looking 24-hour wind speed differences.

For the current category plot, we color the background using the Saffir-Simpson scale. The white background denotes wind speeds less than 64 knots.

#### Inner Core TC Burst Data

![inner core tc burst data](images/dashboard_5.png)

This tab displays inner core lightning detected bursts at the time bin level in a tabular format. Detected bursts are colored by their corresponding marker color used in the time series plot. Note that this view does not include data not used in the threshold calculation - excludes lightning associated with wind speeds less than 40 knots and time bins with no lightning strokes.Use this view to get a better view into overlapping detected bursts by different methods (e.g. the 9/18/2017 4AM time bin shows 3 methods detected this time bin as a burst, shown by the red, blue, and purple highlighted cells).


<a id="rainband"></a>

### Rainband Visualizations

The following tabs display rainband lightning data:
- Rainband TC Plots
- Rainband Shear Quad - Intensification
- Rainband Shear Quad - Current Category
- Rainband TC Burst Data

#### Rainband TC Plots

![rainband tc plots](images/dashboard_6.png)

This tab displays rainband lightning detected bursts on intensification stage color-coded backgrounds on the top and current category color-coded backgrounds on the bottom. Each graph shows the lightning counts in gray, pressure in orange, and wind speed (knots) in blue for the whole duration of the selected TC (regardless of if the data was included in lightning burst threshold calculation). Each of the 6 burst identification methods is displayed with a differently colored marker.

For the intensification stage plot, we only display the 3-category intensification stages - Neutral, Intensifying, and Weakening. Rapidly Weakening and Rapidly Intensifying are combined with Weakening and Intensifying, respectively. The white background denotes the last 24 hours of the storm where we cannot calculate intensification stage using forward-looking 24-hour wind speed differences.

For the current category plot, we color the background using the Saffir-Simpson scale. The white background denotes wind speeds less than 64 knots.

#### Rainband Shear Quad - Intensification

![rainband shear quad intensification](images/dashboard_7.png)

This view shows the intensification stage color-coded graph from the Rainband TC Plots tab at the top, and splits the data into each shear quadrant at the bottom for a 2x2 view. The bottom 4 graphs each display lightning counts, detected bursts, and associated wind/pressure data for each one of the 4 shear quadrants over time. The 2x2 view can be used to explore the distribution of detected bursts across the different shear quadrants.

#### Rainband Shear Quad - Current Category

![rainband shear quad current category](images/dashboard_8.png)

This view shows the current category color-coded graph from the Rainband TC Plots tab at the top, and splits the data into each shear quadrant at the bottom for a 2x2 view. The bottom 4 graphs each display lightning counts, detected bursts, and associated wind/pressure data for each one of the 4 shear quadrants over time. The 2x2 view can be used to explore the distribution of detected bursts across the different shear quadrants.

#### Rainband TC Burst Data

![rainband tc burst data](images/dashboard_9.png)

This tab displays rainband lightning detected bursts at the time bin level in a tabular format. Detected bursts are colored by their corresponding marker color used in the time series plot. Each time bin will have up to 4 rows, one for each shear quadrant. Note that this view does not include data not used in the threshold calculation - excludes lightning associated with wind speeds less than 40 knots and time bins with no lightning strokes. Use this view to get a better view into overlapping detected bursts by different methods (e.g. the 9/20/2017 3PM time bin includes one row per shear quadrant (UL, UR, DR, DL) and shows that the IQR1 and LOGN1 methods both detected a burst for the DL shear quadrant).

<a id="dev"></a>

## Developer Guide

This section goes over the data model setup, dashboard components, and an explanation of the Python visualizations in this dashboard. This section is geared towards developers and includes a section on improvements and expansions for future use.

<a id="data"></a>

### Data Setup

#### Data Sources
The dashboard uses the following files from the [analysis_data](../analysis_data/) directory:
- `innercore_bursts.csv`
- `innercore_lightning_data.csv`
- `rainband_bursts.csv`
- `rainband_lightning_data.csv`

These files are created in the `lightning_threshold_innercore.ipynb` and `lightning_threshold_rainband.ipynb` notebooks in this folder.

To transform the data and update data source paths, click the drop-down arrow next to the table with pencil icon at the top banner on the report view of the dashboard.

![transform data menu](images/dashboard_13.png)

Select "Data source settings" to check current file paths and update the data file paths - this is necessary if the source data changes and for viewing the data transformations applied to the source files.

![data source settings](images/dashboard_15.png)

**!!!!To add more data sources,[wip marker]**

#### Data Transformations
Transformations are applied to each of the files to faciliate the relationships between tables explained in the next section. We need to create a column with unique values to use as a primary key for the relationships, so we concatenate storm codes with time bins (+ shear quadrants for rainband).

Select "Transform data" to see the transformation steps for each data source.

![transform data page](images/dashboard_14.png)

When clicking on each step on the right (in the Applied Steps menu), the upper box will show the [Power Query M code](https://learn.microsoft.com/en-us/powerquery-m/) used to apply the transformations.

![power query m](images/dashboard_16.png)

Transformations applied (Applied Steps menu on the right) to each inner core data file using the Transform data page:
1. Source - import source data
2. Promoted Headers - read the first line of the file as headers
3. Changed Type - cast each column as its respective type (e.g. time_bin as datetime)
4. Duplicated Column - created a copy of the time_bin column
5. Changed Type - changed the type of the time_bin copy column to text instead of datetime
6. Added Custom - added a custom column concatenating the storm code with time bin
7. Renamed Columns - rename the previous added column to "storm_code_time_bin"
8. Removed Columns - remove the duplicated time bin column

Transformations applied to the rainband files:
1. Source - import source data
2. Promoted Headers - read the first line of the file as headers
3. Changed Type - cast each column as its respective type (e.g. time_bin as datetime)
4. Duplicated Column - created a copy of the time_bin column
5. Changed Type - changed the type of the time_bin copy column to text instead of datetime
6. Custom1 - added a custom column concatenating the storm code with time bin
7. Renamed Columns - rename the previous added column to "storm_code_time_bin"
8. Custom2 - added a custom column concatenating the storm name with storm_code_time_bin
9. Renamed Columns1 - rename the previous added column to "storm_code_time_bin_name"
10. Custom3 - added a custom column concatenating the storm_code_time_bin_name with shear quadrant
11. Renamed Column2 - rename the previous added column to "storm_code_time_bin_shear"
12. Removed Columns - remove the duplicated time bin column

#### Data Model - Custom Columns

Navigate to the Data Model view using the menu on the left bar.

![data model view](images/dashboard_18.png)

Here, we see the 4 data tables and the relationships in a diagram format. The tab on the right side shows each table, and can be expanded to view each column along with its data type for the table.

![data model view](images/dashboard_17.png)

The calculator icon denotes that the column is an added custom measure column. The top bar will display the custom measure's code. This code is in [DAX](https://learn.microsoft.com/en-us/dax/) syntax.

![measure](images/dashboard_19.png)

Similarly, the icons with a table in the back and either fx or a sigma also denotes a custom column. The top bar will display the custom column's code. This code is in [DAX](https://learn.microsoft.com/en-us/dax/) syntax.

![custom column](images/dashboard_20.png)

An easy way to check if the column is a custom column added in this menu or not is by clicking on the column name in the right-hand menu. If the top bar is grayed out or missing, the column is from the source data (or added in the transformations stage). If the top bar has code, the column is a custom column added using [DAX](https://learn.microsoft.com/en-us/dax/) syntax.

![ex 1](images/dashboard_21.png)
A blank/grayed out top bar.

![ex2](images/dashboard_22.png)

DAX code for the storm_display_name column.

**innercore_bursts custom columns:**
- burst_iqr1_me - used to color-code IQR1 burst detection cells in the Inner Core TC Burst Data tab
- burst_iqr2_me - used to color-code IQR2 burst detection cells in the Inner Core TC Burst Data tab
- burst_logn1_me - used to color-code LOGN1 burst detection cells in the Inner Core TC Burst Data tab
- burst_logn2_me - used to color-code LOGN2 burst detection cells in the Inner Core TC Burst Data tab
- burst_mad1_me - used to color-code MAD1 burst detection cells in the Inner Core TC Burst Data tab
- burst_mad2_me - used to color-code MAD2 burst detection cells in the Inner Core TC Burst Data tab
- storm_code_name - concatenates storm code with storm name

**innercore_lightning_data custom columns:**
- storm_code_name - concatenates storm code with storm name
- storm_display_name - formats the storm name by adding the storm number to the end in parentheses, parses out the storm number from the storm code
- storm_year - parses out the storm year from the storm code instead of using the year in the data (some storms include data for two years but are only attributed to one)

**rainband_bursts custom columns:**
- burst_iqr1_measure - used to color-code IQR1 burst detection cells in the Inner Core TC Burst Data tab
- burst_iqr2_measure - used to color-code IQR2 burst detection cells in the Inner Core TC Burst Data tab
- burst_logn1_measure - used to color-code LOGN1 burst detection cells in the Inner Core TC Burst Data tab
- burst_logn2_measure - used to color-code LOGN2 burst detection cells in the Inner Core TC Burst Data tab
- burst_mad1_measure - used to color-code MAD1 burst detection cells in the Inner Core TC Burst Data tab
- burst_mad2_measure - used to color-code MAD2 burst detection cells in the Inner Core TC Burst Data tab
- storm_code_name - concatenates storm code with storm name

**rainband_lightning_data custom columns:**
- storm_code_name - concatenates storm code with storm name
- storm_display_name - formats the storm name by adding the storm number to the end in parentheses, parses out the storm number from the storm code
- storm_year - parses out the storm year from the storm code instead of using the year in the data (some storms include data for two years but are only attributed to one)

#### Data Model - Relationships

To view the relationships in the data model, click the relationships icon on the top banner of the Home tab.

![relationships icon](images/dashboard_23.png)

This will open the relationships view, where relationships can be added or edited.

![relationships icon](images/dashboard_24.png)

We set up 2 relationships for this data model, one for the inner core data and one for the rainband data. These relationships ensure that the datasets are synced and properly displayed by preventing duplicates.

We set up a [1-to-1](https://www.geeksforgeeks.org/relationships-in-sql-one-to-one-one-to-many-many-to-many/) relationship for both the inner core and rainband datasets. To view or edit the relationships, either click the three dots at the right side of the relationship or select the check box at the left and click "Edit" at the top.

![relationships edit button](images/dashboard_25.png)

The Edit page will allow you to select the tables to form a relationship between, and select the column to use as the key between the two tables. We use the storm_code_time_bin column for the inner core tables, and the storm_code_time_bin_shear column for the rainband tables. Note that a 1-to-1 relationship requires that both columns contain unique values. Ensure that the "Make this relationship active" box is checked at the bottom to apply the relationship to the data.

![relationships edit page](images/dashboard_26.png)

For more information on data table relationships, refer to this [official documentation](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-create-and-manage-relationships).


<a id="components"></a>

### Dashboard Components

<a id="python"></a>

### Python Visualizations

<a id="future"></a>

## Future Work and Improvements