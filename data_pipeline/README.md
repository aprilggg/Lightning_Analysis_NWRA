# Data Pipeline

* [About Directory](#about)
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
    - bin lightning events into 30-minute bins
    - join lightning bins with TC wind and pressure data
    - calculate current category and intensification change
4. **`rainband_data.ipynb`**
    - looks for shear data files stored in USB
    - combine individual TC shear data files into one consolidated file
    - calculate shear angle and quadrant for rainband lightning events
    - create timebins for rainband data
    - join rainband WWLLN data to trackfiles

This directory also includes a `intermediate_data/` directory containing the outputted intermediate files from the data pipeline used in subsequent data pipeline activities. Files used for subsequent analysis are in the `data/` folder.

*note that intermediate data files too large for upload to Github can be found in this [Google Drive folder](https://drive.google.com/drive/folders/105AYgecVORsUCyOwinQRfb--TC0hhBva?usp=drive_link). These should be placed in the `intermediate_data/` directory.

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

### Output Files - add schema?
These files are created and outputted to the `data/` directory for use in subsequent analysis.
- `filtered_tc_list.csv`
- `innercore_timebin_joined.csv`*
- `rainband_shear_timebin_joined.csv`*
- `rainband_timebin_joined.csv`
- `unbinned_shear_data.txt` - not uploaded to Github due to size

*denotes files used in the subsequent lightning burst threshold analysis.