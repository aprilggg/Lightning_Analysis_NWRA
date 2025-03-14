#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import polars as pl
import matplotlib.pyplot as plt
from scipy.stats import median_abs_deviation
import matplotlib.patches as mpatches
import gc
import os

### Functions
# Below are the functions used to evaluate 6 different lightning burst thresholds at the individual TC level.
# We compare each TC's lightning to itself to identify a burst using the IQR, MAD, and Lognormal methods.
# The thresholds defined by each of these functions act as a standard for a lightning burst for that TC.
# If the count in the bin is more than the threshold, we mark it as a lightning burst.
# Note that we use log-transformed lightning counts in this analysis.
# We do not include data associated with current wind speeds less than 40 knots in this threshold analysis.
# We also create functions to apply the thresholds and aggregate results, as well as functions used to plot individual TCs for analysis.


def detect_bursts_iqr(group):
    """
    Calculates Interquartile Range method log lightning burst thresholds at the
    individual TC level and applies to passed-in data.
    Marks a lightning burst if the log lightning count passes the defined threshold.
    IQR1 refers to 1*IQR higher than the third quartile, IQR2 refers to 1.5*IQR
    higher than the third quartile.

    Parameters:
    - group: set of data from the DataFrame passed in

    Returns:
    - group: data with 4 added columns: 'burst_iqr1', 'burst_iqr2',
    'iqr1_threshold', 'iqr2_threshold'
    """
    Q1 = group['log_lightning_count'].quantile(0.25)
    Q3 = group['log_lightning_count'].quantile(0.75)
    IQR = Q3 - Q1

    # Set burst threshold for each cyclone individually
    threshold1 = Q3 + 1 * IQR
    threshold2 = Q3 + 1.5* IQR

    # Mark bursts specific to the cyclone
    group['burst_iqr1'] = group['log_lightning_count'] > threshold1 # Returns boolean
    group['burst_iqr2'] = group['log_lightning_count'] > threshold2
    group['iqr1_threshold'] = threshold1
    group['iqr2_threshold'] = threshold2
    return group

def detect_bursts_mad(group):
    """
    Calculates Median Absolute Deviation method log lightning burst thresholds
    at the individual TC level and applies to passed-in data.
    Marks a lightning burst if the log lightning count passes the defined threshold.
    MAD1 refers to 4*MAD higher than the median log lightning count, MAD2 refers
    to 5*MAD higher than the median log lightning count.

    Parameters:
    - group: set of data from the DataFrame passed in

    Returns:
    - group: data with 4 added columns: 'burst_mad1', 'burst_mad2',
    'mad1_threshold', 'mad2_threshold'
    """
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

def detect_bursts_lognormal(group):
    """
    Calculates Log-normal Standard Deviation method log lightning burst thresholds
    at the individual TC level and applies to passed-in data.
    Marks a lightning burst if the log lightning count passes the defined threshold.
    LOGN1 refers to 2 standard deviations higher than the mean log lightning count,
    LOGN2 refers to 3 standard deviations higher than the mean log lightning count.

    Parameters:
    - group: set of data from the DataFrame passed in

    Returns:
    - group: data with 4 added columns: 'burst_logn1', 'burst_logn2',
    'logn1_threshold', 'logn2_threshold'
    """
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

def apply_individual_thresholds(df):
    """
    Applies the three lightning burst threshold calculation functions to the data
    at the individual TC level (comparing each storm's lightning with itself).

    Parameters:
    - df: DataFrame with binned log lightning counts

    Returns:
    - bursts: DataFrame with added columns denoting bursts (True/False) and
    threshold values for each storm, time bin, threshold method
    """
    # Apply IQR function
    bursts = df.groupby(["storm_code"]).apply(detect_bursts_iqr)
    bursts.reset_index(drop=True, inplace=True)
    # Apply MAD function
    bursts = bursts.groupby(["storm_code"]).apply(detect_bursts_mad)
    bursts.reset_index(drop=True, inplace=True)
    # Apply Lognormal function
    bursts = bursts.groupby(["storm_code"]).apply(detect_bursts_lognormal)
    bursts.reset_index(drop=True, inplace=True)
    # Reset index to keep data points in chronological order
    bursts.sort_values(by=["storm_code", "time_bin"], inplace=True)
    bursts.reset_index(drop=True, inplace=True)
    return bursts

# Function used to aggregate results dataframe
def create_tc_summary(processed, rainband=None):
    """
    Aggregates the burst data at the TC level to get burst count per method and
    each method's threshold value for each TC.

    Parameters:
    - processed: DataFrame with burst columns indicating if a burst is detected
    for the 6 threshold methods
    - rainband: Boolean value denoting if the input data is for rainband lightning,
    if True then group the data by shear quadrant as well as storm code

    Returns:
    - tc_summary: DataFrame with burst count per method and each method's
    threshold value for each TC, as well as the proportion of non-zero lightning count
    time bins marked as a burst for each method
    """
    if rainband is not None:
        grouping = ["storm_code", "shear_quad"]
    else:
        grouping = ["storm_code"]
    tc_summary = processed.groupby(grouping).agg(
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

def add_bg_colors(ax, lightning_data, color_type):
    """
    Adds background shading based on either the 'Intensification_Category_3', 'Intensification_Category_5',
    or 'Current_Category' column.

    Parameters:
    - ax: The matplotlib axis to plot on.
    - lightning_data: DataFrame with 'time_bin', 'Intensification_Category_3', 'Intensification_Category_5', and 'Current_Category'
    - color_type: toggle between coloring by intensification change category or current category,
    can only take "i3", "i5", "c5" as values

    Returns:
    - legend_patches: matplotlib patch for use in plot legend
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


def plot_bursts(ax, df, quad=None):
    """
    Plots the burst markers for each of the 6 threshold types using the passed-in data.

    Parameters:
    - ax: The matplotlib axis to plot on.
    - df: The DataFrame with the burst data to plot markers with
    - quad: Optional parameter denoting the shear quadrant to plot, applies only to rainband data
    """
    # Set up column name, color, method, threshold type, and marker for each
    burst_columns = {
        'mad1': ['burst_mad1', 'red', 'MAD', '1', 'o'],
        'mad2': ['burst_mad2', 'yellow', 'MAD', '2', 'o'],
        'iqr1': ['burst_iqr1', 'blue', 'IQR','1', 'x'],
        'iqr2': ['burst_iqr2', 'orange', 'IQR','2', 'x'],
        'logn1': ['burst_logn1', 'purple', 'LOGN','1', '^'],
        'logn2': ['burst_logn2', 'green', 'LOGN','2', '^']
    }
    # If quad is passed in, create masks to filter for shear quad value
    if quad is not None:
        burst_masks = {
        "mad1": df['burst_mad1'] & (df['shear_quad'] == quad),
        "mad2": df['burst_mad2'] & (df['shear_quad'] == quad),
        "iqr1": df['burst_iqr1'] & (df['shear_quad'] == quad),
        "iqr2": df['burst_iqr2'] & (df['shear_quad'] == quad),
        "logn1": df['burst_logn1'] & (df['shear_quad'] == quad),
        "logn2": df['burst_logn2'] & (df['shear_quad'] == quad)
        }

    # Mark bursts detected by each method
    for key, (col, color, method, threshold, marker) in burst_columns.items():
        # If quad is passed in, use the shear quad mask
        if quad is not None:
            col_mask = burst_masks[key]
        # Otherwise use just the column name
        else:
            col_mask = df[col]
        ax.scatter(df['time_bin'][col_mask],
                    df['lightning_count'][col_mask],
                    color=color, label=f'{method}{threshold} Burst', s=50, marker=marker, alpha=0.7)

def plot_tc(storm_id, processed, storm_names, storm_data, bg_type, show=True, save_path=None):
    """
    Plots the lightning, wind, pressure, marked bursts, and color-coded background for an individual TC.
    Can optionally save the generated plot to .png file if a path is passed in.

    Parameters:
    - storm_id: Storm code in the basin_year_num format (e.g. "ATL_10_1")
    - processed: pandas DataFrame containing the bursts per time bin in True/False format
    - storm_names: polars DataFrame containing unique storm name and storm code
    - storm_data: polars DataFrame containing wind, pressure, lightning, current category, and intensification stage data
    - bg_type: Either "i3", "i5", or "c5", for use in choosing background color-coding type
    - show: Optional Boolean to toggle showing the plot
    - save_path: Optional path to save the generated plot to
    """
    plt.close('all') # Clean up any open plots for memory
    storm_name = storm_names.filter(pl.col("storm_code") == storm_id)["storm_name"][0] # Lookup storm name
    # Filter to just one storm
    df_cyclone = processed[processed['storm_code'] == storm_id]
    lightning_data = storm_data.filter(pl.col("storm_code") == storm_id).to_pandas()

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

    # Create third y-axis for wind speed
    ax3 = ax1.twinx()
    ax3.spines['right'].set_position(('outward', 50))  # Move the third axis outward for separation
    ax3.plot(lightning_data['time_bin'], lightning_data['knots'], label='Wind', color='blue')
    ax3.set_ylabel("Wind", color="#0603a8")
    ax3.tick_params(axis='y', labelcolor="#0603a8")

    # Call bg colors function
    legend_patches = add_bg_colors(ax1, lightning_data, bg_type)

    # Call bursts function
    plot_bursts(ax1, df_cyclone)

    # Add labels, title, legend
    plt.xlabel('Time')
    plt.title(f'Lightning Burst Detection for {storm_name} ({storm_id})', fontsize=14)
    ax1.legend(loc='upper left', fontsize=12) # Burst marker legend
    ax2.legend(handles=legend_patches, loc='center left', fontsize=12) # Background color legend
    plt.xticks(visible=False)
    plt.grid()

    # Save the figure if save_path is provided
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    # Show only if explicitly requested
    if show:
        plt.show()
    # Ensure figure is closed after use
    plt.close(fig)  # Close the specific figure
    plt.close('all')  # Close any remaining figures
    gc.collect()  # Force garbage collection to free memory


def plot_tc_quadrants(storm_id, processed, storm_names, storm_data, bg_type, show=True, save_path=None):
    """
    Plots the lightning, wind, pressure, marked bursts, and color-coded background by shear quadrant for an individual TC.
    Only applicable for rainband data. Generates a 2x2 plot with all 4 quadrants.
    Can optionally save the generated plot to .png file if a path is passed in.

    Parameters:
    - storm_id: Storm code in the basin_year_num format (e.g. "ATL_10_1")
    - processed: pandas DataFrame containing the bursts per time bin in True/False format
    - storm_names: polars DataFrame containing unique storm name and storm code
    - storm_data: polars DataFrame containing wind, pressure, lightning, current category, and intensification stage data
    - bg_type: Either "i3", "i5", or "c5", for use in choosing background color-coding type
    - show: Optional Boolean to toggle showing the plot
    - save_path: Optional path to save the generated plot to
    """
    plt.close('all') # Clean up any open plots for memory
    storm_name = storm_names.filter(pl.col("storm_code") == storm_id)["storm_name"][0] # Lookup storm name
    # Filter data to one storm
    df_cyclone = processed[processed['storm_code'] == storm_id]
    lightning_data = storm_data.filter(pl.col("storm_code") == storm_id).to_pandas()
    # Define the shear quadrants to plot - display the quadrants in the same order as shear quad graphic
    quadrants = ["UL", "DL", "UR", "DR"]
    fig, axes = plt.subplots(2, 2, figsize=(14, 12), sharey=True, sharex=False)
    axes = axes.flatten()

    # Create empty lists to store legend handles and labels
    all_handles = []
    all_labels = []
    # Create a set to track labels we've added already (to prevent duplicates)
    added_labels = set()

    # Create a plot for each quadrant
    for i, quad in enumerate(quadrants):
        ax = axes[i]

        # Filter data for this quadrant
        df_quad = df_cyclone[df_cyclone["shear_quad"] == quad]
        lightning_quad = lightning_data[lightning_data["shear_quad"] == quad]

        # Plot lightning count
        ax.plot(lightning_quad['time_bin'], lightning_quad['lightning_count'], label='Lightning Count', color='gray')
        ax.set_title(f"{storm_name} ({storm_id}) - {quad}")
        ax.set_xlabel("Time")
        ax.set_ylabel("Lightning Count", color="gray")
        ax.tick_params(axis='y', labelcolor="gray")
        ax.xaxis.set_tick_params(rotation=45)

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
        legend_patches = add_bg_colors(ax, lightning_quad, bg_type)

        # Mark bursts using the overall storm data, not recalculated per quadrant
        plot_bursts(ax, df_cyclone, quad)

        ax.grid()

        # Capture the handles and labels for the current axis
        handles, labels = ax.get_legend_handles_labels()

        # Filter out duplicate labels
        for handle, label in zip(handles, labels):
            if label not in added_labels:
                all_handles.append(handle)
                all_labels.append(label)
                added_labels.add(label)

        # Add the legend patches from background color function
        for patch in legend_patches:
            label = patch.get_label()
            if label not in added_labels:  # Avoid duplicates
                all_handles.append(patch)
                all_labels.append(label)
                added_labels.add(label)


    # Add a common legend for all plots
    fig.legend(all_handles, all_labels, loc='upper center', ncol=7, fontsize=12, bbox_to_anchor=(0.5, 1.05))
    plt.tight_layout()
    # Save the figure if save_path is provided
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    # Show only if explicitly requested
    if show:
        plt.show()
    # Ensure figure is closed after use
    plt.close(fig)  # Close the specific figure
    plt.close('all')  # Close any remaining figures
    gc.collect()  # Force garbage collection to free memory

def export_visualizations(output_dir, tc_list, bursts, storm_names, lightning_data, bg_types, lightning_type, print_toggle=False):
    """
    Generates lightning, wind, pressure, burst plots for the passed-in data and saves to an output directory.
    Calls the plot_tc, plot_tc_quadrants, plot_bursts, and add_bg_colors functions.

    Parameters:
    - output_dir: Path to directory to put visualizations
    - tc_list: DataFrame of storm codes and storm names to generate visualizations for
    - bursts: DataFrame of lightning time bins with burst evaluation (True/False for each threshold type)
    - storm_names: DataFrame of unique storm names and storm codes, used to lookup storm name
    - lightning_data: DataFrame containing all lightning to plot (including those not in threshold analysis)
    - bg_types: List of background color-coding types to generate plots for (valid values: "i3", "i5", "c5")
    - lightning_type: Specify lightning type to control plot type and output file name (valid values: "innercore", "rainband", "shear")
    - print_toggle: Optional Boolean controlling individual file print statements, default to False
    """
    # Define valid values for lighting_type parameter
    lightning_type_list = ["innercore", "rainband", "shear"]
    if lightning_type not in lightning_type_list:
        return(print(f"Not a valid lightning data type. Choose either: {', '.join(lightning_type_list)}"))
    elif lightning_type == "shear":
        lightning_type = "rainband_shear"
    # Check if output directory exists, if not create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Keep count of files saved
    file_count = 0
    # Loop through each row in the TC list
    for storm_code, storm_name in tc_list.iter_rows():
        if print_toggle:
            print(f"Exporting graphs for {storm_name} ({storm_code})")
        # Loop through each background color-coding type
        for bg_type in bg_types:
            # Create save path
            save_path = f"{output_dir}{storm_code}_{storm_name}_{lightning_type}_{bg_type}.png"
            # If shear, plot the 2x2 shear quadrant plot
            if lightning_type == "rainband_shear":
                plot_tc_quadrants(storm_code, bursts, storm_names, lightning_data, bg_type, show=False, save_path=save_path)
            # If not, plot the singular plot
            else:
                plot_tc(storm_code, bursts, storm_names, lightning_data, bg_type, show=False, save_path=save_path)
            file_count += 1
    print(f"{file_count} files saved.")


### The below functions are used for basin-level threshold analysis ###

def group_bins_category(dataset):
    """
    Splits the input dataset into 3 category groupings: 0-2, 1-2, and 3-5.

    Parameters:
    - dataset: DataFrame of lightning count time bins with identified bursts (True/False) to split into category groupings.

    Returns:
    - weak0_lightning: DataFrame of data associated with category 0-2 wind speeds
    - weak1_lightning: DataFrame of data associated with category 1-2 wind speeds
    - strong_lightning: DataFrame of data associated with category 3-5 wind speeds
    """
    # Define the category groupings
    weak_cat0 = ["0", "1", "2"]
    weak_cat1 = ["1", "2"]
    strong_cat = ["3", "4", "5"]

    # Separate the 3 category groupings
    weak0_lightning = dataset[dataset["Current_Category"].isin(weak_cat0)]
    print(f"{len(weak0_lightning)} non-zero lightning count timebins associated with category {min(weak_cat0)}-{max(weak_cat0)} wind speeds.")

    weak1_lightning = dataset[dataset["Current_Category"].isin(weak_cat1)]
    print(f"{len(weak1_lightning)} non-zero lightning count timebins associated with category {min(weak_cat1)}-{max(weak_cat1)} wind speeds.")

    strong_lightning = dataset[dataset["Current_Category"].isin(strong_cat)]
    print(f"{len(strong_lightning)} non-zero lightning count timebins associated with category {min(strong_cat)}-{max(strong_cat)} wind speeds.")

    return weak0_lightning, weak1_lightning, strong_lightning

def plot_threshold_histogram(dataset, threshold_type, ax=None):
    """
    Plots histogram of thresholds for a group of TCs.

    Parameters:
    - dataset: DataFrame of lightning count time bins with threshold values (not aggregated to TC level)
    - threshold_type: Specify which threshold type to plot (e.g. "mad1")
    - ax: Optional parameter used to enable plotting multiple graphs in a grid
    """
    # Create dictionary of threshold names and column names to lookup
    threshold_names = {
        'mad1':['mad1_threshold','MAD1'],
        'mad2':['mad2_threshold','MAD2'],
        'iqr1':['iqr1_threshold','IQR1'],
        'iqr2':['iqr2_threshold','IQR2'],
        'logn1':['logn1_threshold','Lognormal 2 Sigma'],
        'logn2':['logn2_threshold','Lognormal 3 Sigma'],
    }
    if ax is None:
        fig, ax = plt.subplots() # Enable plotting multiple in a grid if ax passed in
    # Filter the data to the specified threshold type
    plot_data = dataset[threshold_names[threshold_type][0]]
    # Check if data is empty - if so, show "No Data Available"
    if plot_data is None or len(plot_data) == 0 or sum(plot_data.isnull()) == len(plot_data):
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
    # If there is data, plot the histogram
    else:
        ax.hist(plot_data, bins=20, edgecolor="black", align="left")
        ax.set_xlabel("Lightning Burst Threshold (Log10 Scale)")
        ax.set_ylabel("Frequency")
        ax.set_title(f"Histogram of {threshold_names[threshold_type][1]} Burst Threshold")

def plot_threshold_boxplot(dataset, category_group):
    """
    Plots boxplot of thresholds for a group of TCs.

    Parameters:
    - dataset: DataFrame of lightning count time bins with threshold values (not aggregated to TC level)
    - category_group: Specify what category grouping this plot is for (valid values: "all", "0-2", "1-2", "3-5")
    """
    category_group_list = ["all", "0-2", "1-2", "3-5"]
    if category_group not in category_group_list:
        return(print(f"Not a valid category group. Choose either: {', '.join(category_group_list)}"))
    plt.figure(figsize=(10, 6))
    plt.boxplot([dataset['mad1_threshold'], dataset['mad2_threshold'], dataset['iqr1_threshold'],
                dataset['iqr2_threshold'], dataset['logn1_threshold'], dataset['logn2_threshold']]
                , labels=['MAD1', 'MAD2', 'IQR1', 'IQR2', 'LOGN1', 'LOGN2'],
                patch_artist=True, boxprops=dict(facecolor='lightblue'))

    plt.title(f'Threshold Value Comparison - {category_group}')
    plt.ylabel('Values')

    plt.show()

def create_burst_summary(dataset):
    """
    Create DataFrame of aggregated burst count, time bin count, and burst percentage for a group of TCs.

    Parameters:
    - dataset: DataFrame of lightning count time bins with threshold values (not aggregated to TC level)

    Returns:
    - burst_summary: DataFrame with burst count, time bin count, and burst percentage for each threshold type.
    """
    # Define threshold names, column names
    threshold_names = {
        'mad1':['mad1_threshold','MAD1'],
        'mad2':['mad2_threshold','MAD2'],
        'iqr1':['iqr1_threshold','IQR1'],
        'iqr2':['iqr2_threshold','IQR2'],
        'logn1':['logn1_threshold','Lognormal 2 Sigma'],
        'logn2':['logn2_threshold','Lognormal 3 Sigma'],
    }
    threshold_keys = list(threshold_names.keys())
    # Create list of burst column names (that match the input dataset column names)
    burst_labels = [f'burst_{key}' for key, value in threshold_names.items()]
    # Generate burst summary
    burst_summary = {
        "Threshold": threshold_keys,
        "Burst Count": [dataset[b].sum() for b in burst_labels], # Sum of bursts per burst type
        "Timebin Count": [dataset["time_bin"].count() for i in range(len(burst_labels))], # Count of time bins per burst type
        "Burst Percentage": [round(dataset[b].sum()/dataset["time_bin"].count()*100, 2) for b in burst_labels]
    }
    # Convert dictionary to DataFrame
    burst_summary = pd.DataFrame(burst_summary)
    return burst_summary


def create_basin_summary(dataset, category_group, basin):
    """
    Create DataFrame of aggregated burst count, time bin count, burst percentage,
    min/max/avg/median threshold values for a group of TCs.
    Calls the create_burst_summary() function.

    Parameters:
    - dataset: DataFrame of lightning count time bins with threshold values (not aggregated to TC level)
    - category_group: Specify which category grouping the input data is for (valid values: "0-2", "1-2", "3-5", "all")
    - basin: Basin to generate summary for (valid values: "ATL", "EPAC", "WPAC", "IO", "SHEM", "CPAC")

    Returns:
    - DataFrame with burst count, time bin count, burst percentage, mean, standard deviation,
    median, minimum, and maximum threshold values for each threshold type for the specified basin/category group.
    """
    # Define valid input values
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

    # Call burst summary function to create burst summary
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
    """
    Create DataFrame of calculated basin-level thresholds for the specified basin, category group.

    Parameters:
    - dataset: DataFrame of lightning count time bins with threshold values (not aggregated to TC level)
    - category_group: Specify which category grouping the input data is for (valid values: "0-2", "1-2", "3-5", "all")
    - basin: Basin to generate summary for (valid values: "ATL", "EPAC", "WPAC", "IO", "SHEM", "CPAC")
    - std_dev: Optional parameter to specify how many standard deviations away from the mean/median to set the threshold value to,
                default value is 2
    - threshold_type: Optional parameter to specify if the threshold is based off "effective" thresholds

    Returns:
    - DataFrame with basin, category group, mean-based calculated threshold, median-based calculated threshold
    """
    # Define valid values
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

    # Set threshold_type to blank if not passed-in
    if threshold_type is None:
        threshold_type = ''
    # Set default std dev value
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

def create_basin_threshold_dict(threshold_data):
    """
    Create dictionary of basin-level thresholds for use in applying basin thresholds to invidividual TCs.
    Used in summarize_threshold_eval() function.

    Parameters:
    - threshold_data: DataFrame of basin-level thresholds

    Returns:
    - basin_thresholds_mean: Dictionary of mean-based threshold values
    - basin_thresholds_median: Dictionary of median-based threshold values
    """
    # Get column names from threshold data
    column_names = {}
    for col in threshold_data.columns:
        if "(Mean-Based)" in col:
            column_names["mean"] = col
        elif "(Median-Based)" in col:
            column_names["median"] = col
    # Separate out mean-based threshold values
    basin_thresholds_mean = {}
    for i in range(len(threshold_data)):
        basin_thresholds_mean[threshold_data["Threshold"][i]] = threshold_data[column_names["mean"]][i]
    # Separate out median-based threshold values
    basin_thresholds_median = {}
    for i in range(len(threshold_data)):
        basin_thresholds_median[threshold_data["Threshold"][i]] = threshold_data[column_names["median"]][i]

    return basin_thresholds_mean, basin_thresholds_median

def detect_bursts_basin(group, thresholds):
    """
    Evaluate basin-level thresholds on DataFrame group.
    Used in apply_basin_thresholds() function.

    Parameters:
    - group: Data to apply thresholds to
    - thresholds: Dictionary of threshold values to evaluate

    Returns:
    - group: Data with added Boolean burst column and threshold value column
    """
    # Use thresholds passed in as dictionary
    for key, value in thresholds.items():
        threshold = value
        group[f'burst_{key}'] = group['log_lightning_count'] > threshold
        group[f'{key}_threshold'] = threshold

    return group

def apply_basin_thresholds(df, basin_thresholds):
    """
    Apply basin-level thresholds on DataFrame group.
    Calls apply_basin_thresholds() function, used in summarize_threshold_eval() function.

    Parameters:
    - df: DataFrame to apply thresholds to
    - basin_thresholds: Dictionary of threshold values to evaluate

    Returns:
    - bursts: DataFrame with added Boolean burst columns and threshold value columns
    """
    # drop bins with 0 lightning count
    clean_data = df[df['lightning_count'] != 0]

    bursts = clean_data.groupby(["storm_code"]).apply(detect_bursts_basin, thresholds = basin_thresholds)
    bursts.reset_index(drop=True, inplace=True)

    bursts.sort_values(by=["storm_code", "time_bin"], inplace=True)
    bursts.reset_index(drop=True, inplace=True)

    return bursts

def column_rename_helper(threshold_data, threshold_type=None):
    """
    Helper function to rename columns in DataFrame. Used to prevent duplicate column names.
    Called by summarize_threshold_eval() function.

    Parameters:
    - threshold_data: DataFrame of calculated threshold values
    - threshold_type: Optional parameter to specify if thresholds are calculated using "effective" burst threshold values

    Returns:
    - column_names: Dictionary to use in renaming DataFrame columns.
    """
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
    """
    Apply basin-level thresholds to lightning bin data and add aggregated summary to summary data.
    Calls create_basin_threshold_dict(), apply_basin_thresholds(), create_tc_summary(), column_rename_helper(), create_burst_summary()

    Parameters:
    - summary_data: DataFrame of aggregated threshold-related statistics for the basin
    - lightning_data: DataFrame with time bins to evaluate the basin-thresholds with
    - threshold_data: DataFrame of calculated threshold values
    - threshold_type: Optional parameter to specify if thresholds are calculated using "effective" burst threshold values

    Returns:
    - summary_data: summary_data DataFrame with added columns for applied threshold (burst count, percentage, threshold value)
    - bursts_mean: DataFrame at time bin level with Boolean indicators for detected bursts for mean-based thresholds
    - tc_summary_mean: DataFrame aggregated to TC level with burst counts, time bin counts, percentages for mean-based thresholds
    - bursts_median: DataFrame at time bin level with Boolean indicators for detected bursts for median-based thresholds
    - tc_summary_median: DataFrame aggregated to TC level with burst counts, time bin counts, percentages for median-based thresholds
    """
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
    summary_data = pd.merge(summary_data, threshold_data, on=["Threshold", "Basin", "Category Group"]) # this should take care of duplicates
    summary_data = pd.merge(summary_data, burst_summary_mean[["Threshold", column_names["mean"]["Burst Count"], column_names["mean"]["Burst Percentage"]]], on="Threshold")
    summary_data = pd.merge(summary_data, burst_summary_median[["Threshold", column_names["median"]["Burst Count"], column_names["median"]["Burst Percentage"]]], on="Threshold")

    return summary_data, bursts_mean, tc_summary_mean, bursts_median, tc_summary_median

def combine_mean_median_datasets(mean_data, median_data, std_dev, category_group):
    """
    Concatenate mean and median datasets to one DataFrame. Can be used for both time bin and aggregated TC level data.

    Parameters:
    - mean_data: DataFrame of mean-based threshold evaluated data
    - median_data: DataFrame of median-based threshold evaluated data
    - std_dev: Number of standard deviations used in the threshold calculation (e.g. 2, 1.5)
    - category_group: Specify which category grouping the input data is for (valid values: "0-2", "1-2", "3-5", "all")

    Returns:
    - Concatenated DataFrame of the two input datasets + 3 columns identifying standard deviations, calculation type (mean/median), and category group
    """
    # Check for valid input
    valid_categories = ["0-2", "1-2", "3-5", "all"]
    if category_group not in valid_categories:
        return(print(f"Not a valid category grouping. Choose either: {', '.join(valid_categories)}"))
    # Add std dev, calculation type, category group to mean/median DataFrames
    mean_data["std_dev"], mean_data["threshold_calc_type"], mean_data["category_group"] = std_dev, "mean", category_group
    median_data["std_dev"], median_data["threshold_calc_type"], median_data["category_group"] = std_dev, "median", category_group
    # Concat and return
    return pd.concat([mean_data, median_data], ignore_index=True)

def filter_effective_thresholds(burst_data):
    """
    Filter for "effective" thresholds - thresholds that have at least 1 detected burst (1+ True value).
    Set threshold values to NaN if burst column is False (not a burst) to prevent inclusion in subsequent calculations.

    Parameters:
    - burst_data: DataFrame of time bin level data with burst evaluation Boolean values to filter

    Returns:
    - bursts_effective: DataFrame of only effective bursts and threshold values
    """
    # Define column names
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