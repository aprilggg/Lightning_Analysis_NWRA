# Data Pipeline

* [About Directory](#about)
* [Calculation Methods](#calculations)
* [Code Requirements](#requirements)
* [Output Files](#outputs)


<a id="about"></a>

### About Directory
The Juptyer Notebook files in this directory are used to upload data to Google Drive, clean up duplicate files, and create combined files for use in the analysis portion of this project.

The notebooks should be executed in the following order:
1. **`data_upload.ipynb`**
    - upload .txt files from USB to Google Drive folder
2. **`data_file_cleaning.ipynb`**
    - clean up duplicate .txt files in Google Drive folder
3. **`data_processing.ipynb`**
    - combine individual files from Google Drive folder into one
    - parse tropical cyclone names and IDs
    - create combined files for WWLLN lightning and TC trackfile datasets
    - calculate lightning distances and filter TCs by category
    - bin lightning strokes into 30-minute bins for inner core data
    - join lightning bins with TC wind and pressure data for inner core data
    - calculate current category and intensification change for inner core data
    - create `innercore_timebin_joined.csv`
4. **`rainband_data.ipynb`**
    - look for shear data files stored in USB
    - combine individual TC shear data files into one consolidated file
    - calculate shear angle and quadrant for rainband lightning strokes
    - create timebins for rainband data
    - join rainband WWLLN data to trackfiles for rainband data
    - calculate current category and intensification change for rainband data
    - create `rainband_shear_timebin_joined.csv`

This directory also includes an [intermediate_data/](intermediate_data/) directory containing the outputted intermediate files from the data pipeline used in subsequent data pipeline activities. Files used for subsequent analysis are in the [data/](data/) folder.

*note that intermediate data files too large for upload to Github can be found in this [Google Drive folder](https://drive.google.com/drive/folders/105AYgecVORsUCyOwinQRfb--TC0hhBva?usp=drive_link). These should be placed in the `intermediate_data/` directory.

<a id="calculations"></a>

### Calculation Methods
The data pipeline performs the following calculations on the data:
#### Inner Core/Rainband Lightning
We define inner core lightning to be lightning strokes within 100 km of storm center, and rainband lightning to be lightning strokes between 200 and 400 km of storm center.

#### Intensification Stages
Intensification stages are defined using the following table:

**Intensification Stage Bins**
| Intensification Stage | Change in Winds (Knots) in 24 Hours (Jiang and Ramirez, 2013)|
| --------------------- | ----------------------|
| Rapidly Weakening | <-30 |
| Weakening | -30 to -10 |
| Neutral | -10 to 10 |
| Intensifying | 10 to 30 |
| Rapidly Intensifying | >30 |

A simplified 3 stage definition combines the Rapidly Weakening with the Weakening stage, and the Rapidly Intensifying with Intensifying stage.

#### Category
Categories are defined using the following [Saffir-Simpson Hurricane Wind Scale](https://www.nhc.noaa.gov/aboutsshws.php):

**TC Category Bins - Saffir-Simpson Hurricane Wind Scale**
| TC Category | Sustained Winds (Knots) |
|  ---------- | ------------|
| 1 | 64-82 kt |
| 2 | 83-95 kt |
| 3 | 96-112 kt |
| 4 | 113-136 kt |
| 5 | 137 kt or higher |

We use the term "current category" to refer to the category of the storm at the given point in time, while the overall TC category is defined using the maximum wind speeds over the duration of the TC.

#### Shear Quadrant
Vertical wind shear is the change in wind speed or direction with altitude, represented by a vector showing the difference between wind vectors at different heights. We use the shear vector angle to calculate the shear vector, shown below in the diagram.

<img src="shear_quadrant_graphic.png" width="200" height="200">

We calculate shear quadrant for rainband lightning using the following formulas.

We use the formula to get the shear angle:
```
shearAngleCG = geoAngleCG - shearAngle
```
We calculate geoAngleCG (geographic angle of lightning relative to North, where lightning due East of the storm center would give an angle of 90 degrees) using arctan and the distance east/north of the storm center. shearAngle is provided in the `.mat` dataset and included in the `unbinned_shear_data.txt` file.

We then assign the lightning event to a shear quadrant using shearAngleCG: (note that the shear vector in the diagram is going towards the right, while the shear angle is calculated relative to North)
- 0-90 - Downshear Left (DL)
- 90-180 - Downshear Right (DR)
- 180-270 - Upshear Right (UR)
- 270 -360 - Upshear Left (UL)

<a id="requirements"></a>

### Code Requirements
The data pipeline notebooks require the following libraries not built in to Python:
- pydrive
- google-api-python-client
- google-auth-httplib2
- google-auth-oauthlib
- pandas
- polars
- numpy

The code in this directory requires a Google account with about 9GB of free space, as well as a Google Cloud project to use the [Google Drive API](https://developers.google.com/drive/api/guides/about-sdk). Detailed instructions on setup and references can be found in the [data_upload.ipynb](/data_upload.ipynb) notebook.
We use Google Drive as a way to host our data files online to facilitate collaboration amongst our group members.

This pipeline assumes that the raw data is contained in a folder structure like the one below, where each TC's data is contained in a separate file:
```
.
├── year
|   └── basin
|       └── storm number
|           └── trackfile
|           └── WWLLN data
|           └── shear file
```
example:
```
.
├── 10
|   └── ATL
|       └── 1
|           └── ATL_10_1_Trackfile.txt
|           └── ATL_10_1_WWLLN_Locations.txt
|           └── ATL_10_1_Intensity_Shear.mat
```

We also assume that each file contains the storm code formatted as basin_year_stormnumber. We look for specific file name patterns when extracting and combining data files.

<a id="outputs"></a>

### Output Files
The following 2 files are created and outputted to the `data/` directory for use in the [lightning_burst_identification](../lightning_burst_identification/) notebooks.

**`innercore_timebin_joined.csv`**

Used in [lightning_threshold_innercore.ipynb](../lightning_burst_identification/lightning_threshold_innercore.ipynb)

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
| Intensification_Category | String | possible values: Rapidly Intensifying, Intensifying, Neutral, Weakening, Rapidly Weakening |

**`rainband_shear_timebin_joined.csv`**

Used in [lightning_threshold_rainband.ipynb](../lightning_burst_identification/lightning_threshold_rainband.ipynb)

| Column Name   | Data Type | Description |
| -------- | ------- | ------- |
| time_bin | Datetime | 30 minute bin |
| shear_quad | String | shear quadrant |
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
| Intensification_Category | String | possible values: Rapidly Intensifying, Intensifying, Neutral, Weakening, Rapidly Weakening |

The following files are created as part of the data pipeline and kept in the `intermediate_data/` directory. Files not in Github can be found in this [Google Drive folder](https://drive.google.com/drive/folders/105AYgecVORsUCyOwinQRfb--TC0hhBva?usp=drive_link).

- `Combined_Reduced_Trackfile.txt` - all TC track files combined
- `Combined_WWLLN_Locations.txt` - all TC WWLLN files combined
- `Filtered_Reduced_Trackfile.csv` - filtered TCs (category 1 or higher) track files
- `Filtered_WWLLN_Locations.txt` - filtered TCs (category 1 or higher) WWLLN lightning data
- `filtered_tc_list.csv` - list of TCs retained after filtering for category 1 or higher
- `shear_data_file_log.txt` - log of which TCs have a shear file when creating shear combined dataset
- `storm_time_period.csv` - TC start and end timestamps from track files for filtered TCs
- `WWLLN_innercore.csv` - WWLLN inner core lightning for filtered TCs (category 1 or higher)
- `WWLLN_rainband.csv` - WWLLN rainband lightning for filtered TCs (category 1 or higher)
- `WWLLN_innercore_timebin_count.csv` - WWLLN inner core binned lightning counts for filtered TCs (category 1 or higher)
- `unbinned_shear_data.txt` - WWLLN lightning data for filtered TCs (category 1 or higher) with shear angle