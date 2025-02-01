# Data Pipeline

### About Code
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

### Output Files
- `Combined_Reduced_Trackfile.txt`
- `Combined_WWLLN_Locations.txt`
- `Filtered_Reduced_Trackfile.csv`
- `Filtered_WWLLN_Locations.txt`
- `WWLLN_innercore.csv`
- `WWLLN_rainband.csv`
- `WWLLN_innercore_w_time.csv`
- `WWLLN_innercore_timebin_count.csv`
- `WWLLN_rainband_timebin_count.csv`
- `WWLLN_rainband_w_time.csv`
- `innercore_joined.csv`*
- `innercore_joined_w_time.csv`
- `rainband_joined.csv`*
- `rainband_joined_w_time.csv`

*denotes files used in the subsequent lightning burst threshold analysis.