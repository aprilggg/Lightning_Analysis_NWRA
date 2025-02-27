#!/usr/bin/env python
# coding: utf-8

# # Inner Core Lightning Threshold Analysis
# In this notebook, we define the threshold for what constitutes a "lightning burst" in the inner core of a tropical cyclone.
#
# ### How do we define a burst of lightning?
# We define a lightning burst based off the number of lightning instances in a 30-minute time bin.
# We start by assuming the distribution of lightning in the inner core is Gaussian.
#
# *We look at each basin separately. Below are the basin codes:
# * ATL - Atlantic Ocean basin
# * CPAC -
# * EPAC - Eastern Pacific basin
# * IO - Indian Ocean basin
# * SHEM - Southern Hemisphere basin
# * WPAC - Western North Pacific basin
#
# ## Code
# ### Import Libraries and Files
# Let's start by importing necessary libraries and files. The inner core dataset is created in the `data_processing.ipynb` notebook as `innercore_timebin_joined.csv`.

# In[1]:


import pandas as pd
import numpy as np
import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import median_abs_deviation
import matplotlib.patches as mpatches


# import data from csv file
innercore_data = pl.read_csv("../data_pipeline/data/innercore_timebin_joined.csv")
innercore_data = innercore_data.with_columns(
    pl.col("time_bin").str.strptime(pl.Datetime).alias("time_bin"),
    pl.col("storm_code").str.extract(r"^(.*?)_", 1).alias("basin"),
    pl.col("lightning_count").log1p().alias("log_lightning_count"),
    pl.when(pl.col("pressure") == 0)
    .then(None)  # Replace 0 with None -> 0 is not possible, treat these as null but don't remove row bc the wind speed value is valid
    .otherwise(pl.col("pressure"))
    .alias("pressure")  # Keep the column name as "pressure"
)
innercore_data = innercore_data.with_columns(
    pl.when(pl.col("TC_Category") == "Unidentified")
    .then(pl.lit("0")) # Replace "unidentified" with 0 for current category
    .otherwise(pl.col("TC_Category"))
    .alias("TC_Category")
)
innercore_data = innercore_data.rename({"Intensification_Category":"Intensification_Category_5", "TC_Category":"Current_Category"})
innercore_data.head()


# We map the intensification bins into 3, combining the rapidly weakening and weakening bins, and the rapidly intensifying and intensifying bins.


# Mapping intensification bins into 3 category instead of 5
category_mapping = {
    "Rapidly Weakening": "Weakening",
    "Weakening": "Weakening",
    "Neutral": "Neutral",
    "Intensifying": "Intensifying",
    "Rapidly Intensifying": "Intensifying"
}

# Apply mapping to create new column
innercore_data = innercore_data.with_columns(
    innercore_data["Intensification_Category_5"].replace(category_mapping).alias("Intensification_Category_3")
)

innercore_data.head()


# In[4]:


# Create dataframe for filtering later
storm_names = innercore_data[["storm_code", "storm_name"]].unique()


# ### Functions
#
# Below are the functions used to evaluate 6 different lightning burst thresholds at the individual TC level. We compare each TC's lightning to itself to identify a burst using the IQR, MAD, and Lognormal methods. The thresholds defined by each of these functions act as a standard for a lightning burst for that TC. If the count in the bin is more than the threshold, we mark it as a lightning burst. Note that we use log-transformed lightning counts in this analysis. We do not include data associated with current wind speeds less than 40 knots in this threshold analysis.
#
# We also create functions to apply the thresholds and aggregate results, as well as functions used to plot individual TCs for analysis.


# IQR threshold function
def detect_bursts_iqr(group):
    Q1 = group['log_lightning_count'].quantile(0.25)
    Q3 = group['log_lightning_count'].quantile(0.75)
    IQR = Q3 - Q1

    # Set burst threshold for each cyclone individually
    threshold1 = Q3 + 1 * IQR
    threshold2 = Q3 + 1.5* IQR

    # Mark bursts specific to the cyclone
    group['burst_iqr1'] = group['log_lightning_count'] > threshold1
    group['burst_iqr2'] = group['log_lightning_count'] > threshold2
    group['iqr1_threshold'] = threshold1
    group['iqr2_threshold'] = threshold2
    return group


# MAD threshold function
def detect_bursts_mad(group):
    median_log = group['log_lightning_count'].median()
    mad_log = median_abs_deviation(group['log_lightning_count'])

    # Set burst threshold based on MAD for each cyclone
    threshold1 = median_log + 4 * mad_log
    threshold2 = median_log + 5 * mad_log

    # Mark bursts specific to the cyclone
    group['burst_mad1'] = group['log_lightning_count'] > threshold1
    group['burst_mad2'] = group['log_lightning_count'] > threshold2
    group['mad1_threshold'] = threshold1
    group['mad2_threshold'] = threshold2
    return group


# Log normal threshold function
def detect_bursts_lognormal(group):
     # Calculate the mean and standard deviation of the log-transformed lightning count
    mean_log = group['log_lightning_count'].mean()
    std_log = group['log_lightning_count'].std()

    # Set burst thresholds based on log-normal distribution (mean + 2σ and mean + 3σ)
    threshold1 = mean_log + 2 * std_log
    threshold2 = mean_log + 3 * std_log

    # Mark bursts specific to the cyclone
    group['burst_logn1'] = group['log_lightning_count'] > threshold1
    group['burst_logn2'] = group['log_lightning_count'] > threshold2
    group['logn1_threshold'] = threshold1
    group['logn2_threshold'] = threshold2
    return group


# Function to apply the 3 methods, 6 thresholds for individual TCs
def apply_individual_thresholds(df):
    bursts = df.groupby(["storm_code"]).apply(detect_bursts_iqr)
    bursts.reset_index(drop=True, inplace=True)
    bursts = bursts.groupby(["storm_code"]).apply(detect_bursts_mad)
    bursts.reset_index(drop=True, inplace=True)
    bursts = bursts.groupby(["storm_code"]).apply(detect_bursts_lognormal)
    bursts.reset_index(drop=True, inplace=True)
    # Reset index to keep data points in chronological order
    bursts.sort_values(by=["storm_code", "time_bin"], inplace=True)
    bursts.reset_index(drop=True, inplace=True)
    return bursts

# Function to apply the 3 methods, 6 thresholds for individual TCs
# def apply_individual_thresholds_quad(df):
#     bursts = df.groupby(["storm_code", 'shear_quad']).apply(detect_bursts_iqr)
#     bursts.reset_index(drop=True, inplace=True)
#     bursts = bursts.groupby(["storm_code", 'shear_quad']).apply(detect_bursts_mad)
#     bursts.reset_index(drop=True, inplace=True)
#     bursts = bursts.groupby(["storm_code", 'shear_quad']).apply(detect_bursts_lognormal)
#     bursts.reset_index(drop=True, inplace=True)
#     # Reset index to keep data points in chronological order
#     bursts.sort_values(by=["storm_code",  "time_bin", 'shear_quad'], inplace=True)
#     bursts.reset_index(drop=True, inplace=True)
#     return bursts

# Function used to aggregate results dataframe
def create_tc_summary(processed):
    tc_summary = processed.groupby(["storm_code"]).agg(
        mad1_bursts=('burst_mad1', 'sum'),
        mad2_bursts=('burst_mad2', 'sum'),
        mad1_threshold=('mad1_threshold', 'max'),
        mad2_threshold=('mad2_threshold', 'max'),
        iqr1_bursts=('burst_iqr1', 'sum'),
        iqr2_bursts=('burst_iqr2', 'sum'),
        iqr1_threshold=('iqr1_threshold', 'max'),
        iqr2_threshold=('iqr2_threshold', 'max'),
        logn1_bursts=('burst_logn1', 'sum'),
        logn2_bursts=('burst_logn2', 'sum'),
        logn1_threshold=('logn1_threshold', 'max'),
        logn2_threshold=('logn2_threshold', 'max'),
        total_bins=('storm_code', 'count')
    )
    tc_summary.reset_index(drop=False, inplace=True)
    tc_summary.head(10)

    tc_summary["mad1_prop"] = round((tc_summary["mad1_bursts"]/tc_summary["total_bins"])*100, 2)
    tc_summary["mad2_prop"] = round((tc_summary["mad2_bursts"]/tc_summary["total_bins"])*100, 2)
    tc_summary["iqr1_prop"] = round((tc_summary["iqr1_bursts"]/tc_summary["total_bins"])*100, 2)
    tc_summary["iqr2_prop"] = round((tc_summary["iqr2_bursts"]/tc_summary["total_bins"])*100, 2)
    tc_summary["logn1_prop"] = round((tc_summary["logn1_bursts"]/tc_summary["total_bins"])*100, 2)
    tc_summary["logn2_prop"] = round((tc_summary["logn2_bursts"]/tc_summary["total_bins"])*100, 2)
    return tc_summary

# def create_tc_summary_quad(processed):
#     tc_summary = processed.groupby(["storm_code",'shear_quad']).agg(
#         mad1_bursts=('burst_mad1', 'sum'),
#         mad2_bursts=('burst_mad2', 'sum'),
#         mad1_threshold=('mad1_threshold', 'max'),
#         mad2_threshold=('mad2_threshold', 'max'),
#         iqr1_bursts=('burst_iqr1', 'sum'),
#         iqr2_bursts=('burst_iqr2', 'sum'),
#         iqr1_threshold=('iqr1_threshold', 'max'),
#         iqr2_threshold=('iqr2_threshold', 'max'),
#         logn1_bursts=('burst_logn1', 'sum'),
#         logn2_bursts=('burst_logn2', 'sum'),
#         logn1_threshold=('logn1_threshold', 'max'),
#         logn2_threshold=('logn2_threshold', 'max'),
#         total_bins=('storm_code', 'count')
#     )
#     tc_summary.reset_index(drop=False, inplace=True)
#     tc_summary.head(10)

#     tc_summary["mad1_prop"] = round((tc_summary["mad1_bursts"]/tc_summary["total_bins"])*100, 2)
#     tc_summary["mad2_prop"] = round((tc_summary["mad2_bursts"]/tc_summary["total_bins"])*100, 2)
#     tc_summary["iqr1_prop"] = round((tc_summary["iqr1_bursts"]/tc_summary["total_bins"])*100, 2)
#     tc_summary["iqr2_prop"] = round((tc_summary["iqr2_bursts"]/tc_summary["total_bins"])*100, 2)
#     tc_summary["logn1_prop"] = round((tc_summary["logn1_bursts"]/tc_summary["total_bins"])*100, 2)
#     tc_summary["logn2_prop"] = round((tc_summary["logn2_bursts"]/tc_summary["total_bins"])*100, 2)
#     return tc_summary

def add_bg_colors(ax, lightning_data, color_type):
    """
    Adds background shading based on either the 'Intensification_Category_3' column or 'Current_Category' column.

    Parameters:
    - ax: The matplotlib axis to plot on.
    - lightning_data: DataFrame with 'time_bin', 'Intensification_Category_3', and 'Current_Category'
    - color_type: toggle between coloring by intensification change category or current category, can only take i3, i5, c5 as values
    """
    # Define color mapping
    i3_colors = {
        "Intensifying": "#FFAABB",
        "Neutral": "#EEDD88",
        "Weakening": "#77AADD",
        "Unidentified":"white"
    }
    i5_colors = {
        "Rapidly Intensifying": "#EE8866",
        "Intensifying": "#FFAABB",
        "Neutral": "#EEDD88",
        "Weakening": "#77AADD",
        "Rapidly Weakening": "#99DDFF",
        "Unidentified":"white"
    }
    c5_colors = {
        "0":'white',
        "1":'#99DDFF',
        "2":'#77AADD',
        "3":'#EEDD88',
        "4":'#FFAABB',
        "5":'#EE8866'
    }

    # Define color_type toggle
    color_type_toggle = {
        "i3":["Intensification_Category_3", i3_colors],
        "i5":["Intensification_Category_5", i5_colors],
        "c5":["Current_Category", c5_colors]
    }
    # Exit if inputted color type is not valid
    if color_type not in color_type_toggle.keys():
        return(print(f"Not a valid background color type. Choose either: {', '.join(color_type_toggle.keys())}"))

    category_colors = color_type_toggle[color_type][1]
    column_name = color_type_toggle[color_type][0]
    for i in range(len(lightning_data) - 1):
        category = lightning_data[column_name].iloc[i]
        color = category_colors.get(category, "red")  # Default to red if not found - flag this as an error

        ax.axvspan(lightning_data['time_bin'].iloc[i],
                   lightning_data['time_bin'].iloc[i + 1],
                   color=color, alpha=0.3)

    # Create custom legend patches
    legend_patches = [mpatches.Patch(color=c, label=cat) for cat, c in category_colors.items()]
    return legend_patches  # Return legend handles


def plot_tc(cyclone_id, processed, storm_names, innercore_data, bg_type):
    cyclone_name = storm_names.filter(pl.col("storm_code") == cyclone_id)["storm_name"].item()
    df_cyclone = processed[processed['storm_code'] == cyclone_id]
    lightning_data = innercore_data.filter(pl.col("storm_code") == cyclone_id).to_pandas()

    plt.figure(figsize=(10, 5))

    # Create first y-axis for lightning
    fig, ax1 = plt.subplots(figsize=(14, 8))

    ax1.plot(lightning_data['time_bin'], lightning_data['lightning_count'], label='Lightning Count', color='gray')
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Lightning Count", color="gray")
    ax1.tick_params(axis='y', labelcolor="gray")

    # Create second y-axis for pressure
    ax2 = ax1.twinx()
    ax2.plot(lightning_data['time_bin'], lightning_data['pressure'], label='Pressure', color='#d16002')
    ax2.set_ylabel("Pressure", color="#d16002")
    ax2.tick_params(axis='y', labelcolor="#d16002")

    # Create third y-axis for wind knot
    ax3 = ax1.twinx()
    ax3.spines['right'].set_position(('outward', 50))  # Move the third axis outward for separation
    ax3.plot(lightning_data['time_bin'], lightning_data['knots'], label='Wind', color='blue')
    ax3.set_ylabel("Wind", color="#0603a8")
    ax3.tick_params(axis='y', labelcolor="#0603a8")

    # Call bg colors function
    legend_patches = add_bg_colors(ax1, lightning_data, bg_type)

    # Mark bursts detected by MAD
    ax1.scatter(df_cyclone['time_bin'][df_cyclone['burst_mad1']],
                df_cyclone['lightning_count'][df_cyclone['burst_mad1']],
                color='red', label='MAD Detected Burst -threshold1', s=50, marker='o', alpha=0.7)
    ax1.scatter(df_cyclone['time_bin'][df_cyclone['burst_mad2']],
                df_cyclone['lightning_count'][df_cyclone['burst_mad2']],
                color='yellow', label='MAD Detected Burst - threshold2', s=50, marker='o', alpha=0.7)

    # Mark bursts detected by IQR
    ax1.scatter(df_cyclone['time_bin'][df_cyclone['burst_iqr1']],
                df_cyclone['lightning_count'][df_cyclone['burst_iqr1']],
                color='blue', label='IQR Detected Burst - threshold1', s=50, marker='x', alpha=0.7)
    ax1.scatter(df_cyclone['time_bin'][df_cyclone['burst_iqr2']],
                df_cyclone['lightning_count'][df_cyclone['burst_iqr2']],
                color='orange', label='IQR Detected Burst - threshold2', s=50, marker='x', alpha=0.7)

    # Mark bursts detected by lognormal threshold
    ax1.scatter(df_cyclone['time_bin'][df_cyclone['burst_logn1']],
                df_cyclone['lightning_count'][df_cyclone['burst_logn1']],
                color='purple', label='Lognormal Detected Burst - 2 sigma', s=50, marker='^', alpha=0.7)
    ax1.scatter(df_cyclone['time_bin'][df_cyclone['burst_logn2']],
                df_cyclone['lightning_count'][df_cyclone['burst_logn2']],
                color='green', label='Lognormal Detected Burst - 3 sigma', s=50, marker='^', alpha=0.7)

    plt.xlabel('Time')
    plt.title(f'Lightning Burst Detection for {cyclone_name} ({cyclone_id})')
    ax1.legend(loc='upper left')
    ax2.legend(handles=legend_patches, loc='center left')
    plt.xticks(visible=False)
    plt.grid()
    plt.show()


def plot_tc_quadrants(cyclone_id, processed, storm_names, innercore_data, bg_type):
    cyclone_name = storm_names.filter(pl.col("storm_code") == cyclone_id)["storm_name"].item()
    df_cyclone = processed[processed['storm_code'] == cyclone_id]
    lightning_data = innercore_data.filter(pl.col("storm_code") == cyclone_id).to_pandas()

    quadrants = ["DL", "DR", "UL", "UR"]
    fig, axes = plt.subplots(2, 2, figsize=(14, 12), sharex=True, sharey=True)
    axes = axes.flatten()

    for i, quad in enumerate(quadrants):
        ax = axes[i]

        # Filter data for this quadrant
        df_quad = df_cyclone[df_cyclone["shear_quad"] == quad]
        lightning_quad = lightning_data[lightning_data["shear_quad"] == quad]

        # Plot lightning count
        ax.plot(lightning_quad['time_bin'], lightning_quad['lightning_count'], label='Lightning Count', color='gray')
        ax.set_title(f"{cyclone_name} ({cyclone_id}) - {quad}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Lightning Count", color="gray")
        ax.tick_params(axis='y', labelcolor="gray")

        # Add pressure data (second y-axis)
        ax2 = ax.twinx()
        ax2.plot(lightning_quad['time_bin'], lightning_quad['pressure'], label='Pressure', color='#d16002')
        ax2.set_ylabel("Pressure", color="#d16002")
        ax2.tick_params(axis='y', labelcolor="#d16002")

        # Add wind data (third y-axis)
        ax3 = ax.twinx()
        ax3.spines['right'].set_position(('outward', 50))
        ax3.plot(lightning_quad['time_bin'], lightning_quad['knots'], label='Wind', color='blue')
        ax3.set_ylabel("Wind", color="#0603a8")
        ax3.tick_params(axis='y', labelcolor="#0603a8")

        # Call background colors function
        add_bg_colors(ax, lightning_quad, bg_type)

        # Mark bursts using the overall storm data, not recalculated per quadrant
        burst_mask_mad1 = df_cyclone['burst_mad1'] & (df_cyclone['shear_quad'] == quad)
        burst_mask_mad2 = df_cyclone['burst_mad2'] & (df_cyclone['shear_quad'] == quad)
        burst_mask_iqr1 = df_cyclone['burst_iqr1'] & (df_cyclone['shear_quad'] == quad)
        burst_mask_iqr2 = df_cyclone['burst_iqr2'] & (df_cyclone['shear_quad'] == quad)
        burst_mask_logn1 = df_cyclone['burst_logn1'] & (df_cyclone['shear_quad'] == quad)
        burst_mask_logn2 = df_cyclone['burst_logn2'] & (df_cyclone['shear_quad'] == quad)

        ax.scatter(df_cyclone['time_bin'][burst_mask_mad1],
                   df_cyclone['lightning_count'][burst_mask_mad1],
                   color='red', label='MAD - threshold1', s=50, marker='o', alpha=0.7)
        ax.scatter(df_cyclone['time_bin'][burst_mask_mad2],
                   df_cyclone['lightning_count'][burst_mask_mad2],
                   color='yellow', label='MAD - threshold2', s=50, marker='o', alpha=0.7)

        ax.scatter(df_cyclone['time_bin'][burst_mask_iqr1],
                   df_cyclone['lightning_count'][burst_mask_iqr1],
                   color='blue', label='IQR - threshold1', s=50, marker='x', alpha=0.7)
        ax.scatter(df_cyclone['time_bin'][burst_mask_iqr2],
                   df_cyclone['lightning_count'][burst_mask_iqr2],
                   color='orange', label='IQR - threshold2', s=50, marker='x', alpha=0.7)

        ax.scatter(df_cyclone['time_bin'][burst_mask_logn1],
                   df_cyclone['lightning_count'][burst_mask_logn1],
                   color='purple', label='Lognormal - 2 sigma', s=50, marker='^', alpha=0.7)
        ax.scatter(df_cyclone['time_bin'][burst_mask_logn2],
                   df_cyclone['lightning_count'][burst_mask_logn2],
                   color='green', label='Lognormal - 3 sigma', s=50, marker='^', alpha=0.7)

        ax.grid()

    # Add a common legend for all plots
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center', ncol=7, fontsize=8)
    plt.tight_layout()
    plt.show()



def group_bins_category(dataset):
    # split bins into 0-2, 1-2, and 3-5 categories - return 3 datasets
    weak_cat0 = ["0", "1", "2"]
    weak_cat1 = ["1", "2"]
    strong_cat = ["3", "4", "5"]

    # separate the 2 category groupings
    weak0_lightning = dataset[dataset["Current_Category"].isin(weak_cat0)]
    print(f"{len(weak0_lightning)} non-zero lightning count timebins associated with category {min(weak_cat0)}-{max(weak_cat0)} wind speeds in EPAC basin.")

    weak1_lightning = dataset[dataset["Current_Category"].isin(weak_cat1)]
    print(f"{len(weak1_lightning)} non-zero lightning count timebins associated with category {min(weak_cat1)}-{max(weak_cat1)} wind speeds in EPAC basin.")

    strong_lightning = dataset[dataset["Current_Category"].isin(strong_cat)]
    print(f"{len(strong_lightning)} non-zero lightning count timebins associated with category {min(strong_cat)}-{max(strong_cat)} wind speeds in EPAC basin.")

    return weak0_lightning, weak1_lightning, strong_lightning


def plot_threshold_histogram(dataset, threshold_type, ax=None):
    if ax is None: # enable plotting multiple in a grid if ax passed in
        fig, ax = plt.subplots()
    threshold_names = {
        'mad1':['mad1_threshold','MAD1'],
        'mad2':['mad2_threshold','MAD2'],
        'iqr1':['iqr1_threshold','IQR1'],
        'iqr2':['iqr2_threshold','IQR2'],
        'logn1':['logn1_threshold','Lognormal 2 Sigma'],
        'logn2':['logn2_threshold','Lognormal 3 Sigma'],
    }
    if ax is None:
        fig, ax = plt.subplots()
    plot_data = dataset[threshold_names[threshold_type][0]]
    if plot_data is None or len(plot_data) == 0 or sum(plot_data.isnull()) == len(plot_data):  # Check if data is empty
        ax.text(0.5, 0.5, "No Data Available", fontsize=12, ha='center', va='center')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xticks([])  # Hide x-axis ticks
        ax.set_yticks([])  # Hide y-axis ticks
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.set_title(f"Histogram of {threshold_names[threshold_type][1]} Burst Threshold")
    else:
        ax.hist(plot_data, bins=20, edgecolor="black", align="left")
        ax.set_xlabel("Lightning Burst Threshold (Log10 Scale)")
        ax.set_ylabel("Frequency")
        ax.set_title(f"Histogram of {threshold_names[threshold_type][1]} Burst Threshold")


def plot_threshold_boxplot(dataset, category_group, ax=None):
    plt.figure(figsize=(10, 6))
    plt.boxplot([dataset['mad1_threshold'], dataset['mad2_threshold'], dataset['iqr1_threshold'],
                dataset['iqr2_threshold'], dataset['logn1_threshold'], dataset['logn2_threshold']]
                , labels=['MAD1', 'MAD2', 'IQR1', 'IQR2', 'LOGN1', 'LOGN2'],
                patch_artist=True, boxprops=dict(facecolor='lightblue'))

    plt.title(f'Threshold Value Comparison - {category_group}')
    plt.ylabel('Values')

    plt.show()


def create_burst_summary(dataset):
    threshold_names = {
        'mad1':['mad1_threshold','MAD1'],
        'mad2':['mad2_threshold','MAD2'],
        'iqr1':['iqr1_threshold','IQR1'],
        'iqr2':['iqr2_threshold','IQR2'],
        'logn1':['logn1_threshold','Lognormal 2 Sigma'],
        'logn2':['logn2_threshold','Lognormal 3 Sigma'],
    }
    threshold_keys = list(threshold_names.keys())
    burst_labels = [f'burst_{key}' for key, value in threshold_names.items()]
    # Generate burst summary
    burst_summary = {
        "Threshold": threshold_keys,
        "Burst Count": [dataset[b].sum() for b in burst_labels],
        "Timebin Count": [dataset["time_bin"].count() for i in range(len(burst_labels))],
        "Burst Percentage": [round(dataset[b].sum()/dataset["time_bin"].count()*100, 2) for b in burst_labels]
    }
    burst_summary = pd.DataFrame(burst_summary)
    return burst_summary


def create_basin_summary(dataset, category_group, basin):
    valid_categories = ["0-2", "1-2", "3-5", "all"]
    valid_basins = ["ATL", "EPAC", "WPAC", "IO", "SHEM", "CPAC"]
    threshold_names = {
        'mad1':['mad1_threshold','MAD1'],
        'mad2':['mad2_threshold','MAD2'],
        'iqr1':['iqr1_threshold','IQR1'],
        'iqr2':['iqr2_threshold','IQR2'],
        'logn1':['logn1_threshold','Lognormal 2 Sigma'],
        'logn2':['logn2_threshold','Lognormal 3 Sigma'],
    }
    threshold_keys = list(threshold_names.keys())
    threshold_cols = [threshold_names[key][0] for key in threshold_keys]

    # Check for valid input
    if category_group not in valid_categories:
        return(print(f"Not a valid category grouping. Choose either: {', '.join(valid_categories)}"))
    elif basin not in valid_basins:
        return(print(f"Not a valid basin. Choose either: {', '.join(valid_basins)}"))

    burst_summary = create_burst_summary(dataset)

    # Get mean and 2 standard deviations - threshold summary
    threshold_summary = {
        "Basin": [basin for i in range(len(threshold_keys))],
        "Category Group": [category_group for i in range(len(threshold_keys))],
        "Threshold": threshold_keys,
        "Mean": [dataset[col].mean() for col in threshold_cols],
        "Std Dev": [dataset[col].std() for col in threshold_cols],
        "Median": [dataset[col].median() for col in threshold_cols],
        "Min": [dataset[col].min() for col in threshold_cols],
        "Max": [dataset[col].max() for col in threshold_cols]
    }
    threshold_summary = pd.DataFrame(threshold_summary)

    # Join the two dataframes and return
    return pd.merge(threshold_summary, burst_summary, on="Threshold")


def calculate_basin_thresholds(dataset, category_group, basin, std_dev=None, threshold_type=None):
    if threshold_type is None:
        threshold_type = ''
    valid_categories = ["0-2", "1-2", "3-5", "all"]
    valid_basins = ["ATL", "EPAC", "WPAC", "IO", "SHEM", "CPAC"]
    threshold_names = {
        'mad1':['mad1_threshold','MAD1'],
        'mad2':['mad2_threshold','MAD2'],
        'iqr1':['iqr1_threshold','IQR1'],
        'iqr2':['iqr2_threshold','IQR2'],
        'logn1':['logn1_threshold','Lognormal 2 Sigma'],
        'logn2':['logn2_threshold','Lognormal 3 Sigma'],
    }
    threshold_keys = list(threshold_names.keys())
    threshold_cols = [threshold_names[key][0] for key in threshold_keys]

    # Check for valid input
    if category_group not in valid_categories:
        return(print(f"Not a valid category grouping. Choose either: {', '.join(valid_categories)}"))
    elif basin not in valid_basins:
        return(print(f"Not a valid basin. Choose either: {', '.join(valid_basins)}"))
    # Set defaults std dev value
    if std_dev is None:
        std_dev = 2
    # Create dictionary of thresholds
    calculated_thresholds = {
        "Basin": [basin for i in range(len(threshold_keys))],
        "Category Group": [category_group for i in range(len(threshold_keys))],
        "Threshold": threshold_keys,
        f"Basin-Category {threshold_type.capitalize()+' '}Threshold (Mean-Based) {std_dev} SD": [dataset[col].mean()+std_dev*dataset[col].std() for col in threshold_cols],
        f"Basin-Category {threshold_type.capitalize()+' '}Threshold (Median-Based) {std_dev} SD": [dataset[col].median()+std_dev*dataset[col].std() for col in threshold_cols]
    }

    return pd.DataFrame(calculated_thresholds)


def create_basin_threshold_dict(summary_data):
    basin_thresholds_mean = {}
    column_names = {}
    for col in summary_data.columns:
        if "(Mean-Based)" in col:
            column_names["mean"] = col
        elif "(Median-Based)" in col:
            column_names["median"] = col
    for i in range(len(summary_data)):
        basin_thresholds_mean[summary_data["Threshold"][i]] = summary_data[column_names["mean"]][i]
    basin_thresholds_median = {}
    for i in range(len(summary_data)):
        basin_thresholds_median[summary_data["Threshold"][i]] = summary_data[column_names["median"]][i]

    return basin_thresholds_mean, basin_thresholds_median


def detect_bursts_basin(group, thresholds):
    # Use thresholds passed in as dictionary
    for key, value in thresholds.items():
        threshold = value
        group[f'burst_{key}'] = group['log_lightning_count'] > threshold
        group[f'{key}_threshold'] = threshold

    return group



def apply_basin_thresholds(df, basin_thresholds):
    # drop bins with 0 lightning count
    clean_data = df[df['lightning_count'] != 0]

    bursts = clean_data.groupby(["storm_code"]).apply(detect_bursts_basin, thresholds = basin_thresholds)
    bursts.reset_index(drop=True, inplace=True)

    bursts.sort_values(by=["storm_code", "time_bin"], inplace=True)
    bursts.reset_index(drop=True, inplace=True)

    return bursts



def column_rename_helper(threshold_data, threshold_type=None):
    # Set default value for threshold_type to blank string
    if threshold_type is None:
        threshold_type = ''
    # Look for threshold columns to parse out SD
    for col in threshold_data.columns:
        if ")" in col:
            std_dev = col.split(")")[1]
    # Create dictionary to rename columns outputted from burst summary function
    column_names = {
        "mean": {"Burst Count": f"Basin-Category {threshold_type.capitalize()+' '}Threshold Bursts (Mean-Based){std_dev}",
                "Burst Percentage": f"Basin-Category {threshold_type.capitalize()+' '}Threshold Burst Percentage (Mean-Based){std_dev}"},
        "median":{"Burst Count": f"Basin-Category {threshold_type.capitalize()+' '}Threshold Bursts (Median-Based){std_dev}",
                "Burst Percentage": f"Basin-Category {threshold_type.capitalize()+' '}Threshold Burst Percentage (Median-Based){std_dev}"}
    }
    return column_names


def summarize_threshold_eval(summary_data, lightning_data, threshold_data, threshold_type=None):
    # Create threshold dictionaries to apply at basin level
    mean_thresholds, median_thresholds = create_basin_threshold_dict(threshold_data)

    # Apply basin thresholds at individual TC level for the mean and median threshold methods
    bursts_mean = apply_basin_thresholds(lightning_data, mean_thresholds)
    tc_summary_mean = create_tc_summary(bursts_mean)

    bursts_median = apply_basin_thresholds(lightning_data, median_thresholds)
    tc_summary_median = create_tc_summary(bursts_median)

    # Generate column names to prevent redundant columns in summary data
    column_names = column_rename_helper(threshold_data, threshold_type)

    # Create burst summary at basin level
    burst_summary_mean = create_burst_summary(bursts_mean)
    burst_summary_mean = burst_summary_mean.rename(columns=column_names["mean"])

    burst_summary_median = create_burst_summary(bursts_median)
    burst_summary_median = burst_summary_median.rename(columns=column_names["median"])

    # Add to the basin summary
    summary_data = pd.merge(summary_data, threshold_data, on=["Threshold", "Basin", "Category Group"]) # this should take care of duplicates?
    summary_data = pd.merge(summary_data, burst_summary_mean[["Threshold", column_names["mean"]["Burst Count"], column_names["mean"]["Burst Percentage"]]], on="Threshold")
    summary_data = pd.merge(summary_data, burst_summary_median[["Threshold", column_names["median"]["Burst Count"], column_names["median"]["Burst Percentage"]]], on="Threshold")

    return summary_data, bursts_mean, tc_summary_mean, bursts_median, tc_summary_median

def combine_mean_median_datasets(mean_data, median_data, std_dev, category_group):
    mean_data["std_dev"], mean_data["threshold_calc_type"], mean_data["category_group"] = std_dev, "mean", category_group
    median_data["std_dev"], median_data["threshold_calc_type"], median_data["category_group"] = std_dev, "median", category_group

    return pd.concat([mean_data, median_data], ignore_index=True)

def filter_effective_thresholds(burst_data):
    burst_columns = ['burst_iqr1', 'burst_iqr2', 'burst_mad1', 'burst_mad2', 'burst_logn1', 'burst_logn2']
    threshold_cols = ['mad1_threshold', 'mad2_threshold', 'iqr1_threshold', 'iqr2_threshold', 'logn1_threshold', 'logn2_threshold']
    # Filter data to only those with at least one "True" value in the burst columns, grouped by storm code
    # Do not include thresholds that don't flag a burst
    mask = burst_data.groupby("storm_code")[burst_columns].transform(lambda group: group.any(axis=0))

    # Filter rows to where at least one burst col has True value
    bursts_effective = burst_data[burst_data[burst_columns].any(axis=1)].copy()

    # Set threshold values to NaN where burst columns are False
    for burst_col, threshold_col in zip(burst_columns, threshold_cols):
        bursts_effective[threshold_col] = bursts_effective[threshold_col].where(bursts_effective[burst_col], np.nan)

    return bursts_effective

