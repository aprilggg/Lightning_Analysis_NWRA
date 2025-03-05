# Data Pipeline

### About Directory
The Juptyer Notebook files in this directory are used to upload data to Google Drive, clean up duplicate files, and create combined files for use in the analysis portion of this project.

The notebooks should be executed in the following order:
1. **`data_upload.ipynb`**
    - upload .txt files from USB to Google Drive folder
2. **`data_file_cleaning.ipynb`**
    - clean up duplicate .txt files in Google Drive folder
3. **`data_processing.ipynb`**
    - parse tropical cyclone names and IDs
    - create combined files for WWLLN lightning and TC trackfile datasets
    - calculate lightning distances and filter TCs by category
    - bin lightning events into 30-minute bins
    - join lightning bins with TC wind and pressure data
    - calculate current category and intensification change
4. **`rainband_data.ipynb`**
    - combine individual TC shear data files into one consolidated file
    - calculate shear angle and quadrant for rainband lightning events
    - create timebins for rainband data
    - join rainband WWLLN data to trackfiles

This directory also includes a `intermediate_data/` directory containing the outputted intermediate files from the data pipeline used in subsequent analysis.

### Code Requirements
The data pipeline notebooks require the following libraries not built in to Python:
- pydrive
- google-api-python-client
- google-auth-httplib2
- google-auth-oauthlib
- pandas
- polars
- numpy

The code in this directory requires a Google account with about 9GB of free space, as well as a Google Cloud project to use the [Google Drive API](https://developers.google.com/drive/api/guides/about-sdk). Detailed instructions on setup and references can be found in the `data_upload.ipynb` notebook.

### Output Files - add schema?
These files are created and outputted to the `data/` directory for use in subsequent analysis.
- `filtered_tc_list.csv`
- `innercore_timebin_joined.csv`*
- `rainband_shear_timebin_joined.csv`*
- `rainband_timebin_joined.csv`
- `unbinned_shear_data.txt` - not uploaded to Github due to size

*denotes files used in the subsequent lightning burst threshold analysis.