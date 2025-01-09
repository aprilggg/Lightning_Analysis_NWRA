# Lighting-Analysis
UW MSDS Capstone Project with Northwest Research Associates

### Code
!! need to add file description and any intermediate output files with their schema and description

`data_upload.ipynb` - Upload raw txt files from provided USB to Google Drive

`data_file_cleaning.ipynb` - Clean duplicate txt files from Google Drive

`data_cleaning_combined_data.ipynb` - Extract tropical cyclone ID and name from file name, combine individual trackfiles and WWLLN data files into one overall trackfile and one WWLLN data file.

Outputs:
- `processed_files/` - add TC ID and name to each raw file and save as an intermediate file
- `combined_files/Combined_Reduced_Trackfile.txt` - combined trackfiles for all TCs from 2010-2020
- `combined_files/Combined_WWLLN_Locations.txt` - combined WWLLN location data for all TCs from 2010-2020

`cyclone_EDA.ipynb` -

Upload the data - Done

Clean and combine the data - tracking and location data - Done; with headers and cyclone code (unique) & name (not unique)
