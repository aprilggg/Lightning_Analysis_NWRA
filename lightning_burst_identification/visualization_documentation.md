# Lightning Burst Threshold Visualizations
Visualizations in this directory can also be found [here](https://drive.google.com/drive/folders/1iIZx4ThnT8KyQc6pDPAemjYb0Ma_OFd_?usp=drive_link).

### Directory Overview
This directory contains the following visualizations for each TC:*

| Lightning Visualization Type   | Background Color-Coding Type  | File Name Pattern |
| -------- | ------- | ------- |
| Inner Core | Current Category (5 categories) | innercore_c5.png |
| Inner Core | Intensification Stages (3 categories) | innercore_i3.png |
| Rainband | Current Category (5 categories) | rainband_c5.png |
| Rainband | Intensification Stages (3 categories) | rainband_i3.png |
| Rainband Shear (2x2) | Current Category (5 categories) | rainband_shear_c5.png |
| Rainband Shear (2x2) | Intensification Stages (3 categories) | rainband_shear_i3.png |

*note that not all TCs have shear data available, and as such will not have been included in rainband analysis

The current category background color-coding type includes categories 0-5, while the intensification stages color-coding type includes the simplified intensification stage bins (Weakening, Neutral, Intensifying). The visualizations in this directory are created in [lightning_threshold_innercore.ipynb](lightning_threshold_innercore.ipynb) and [lightning_threshold_rainband.ipynb](lightning_threshold_rainband.ipynb), which use the functions in [lightning_threshold_functions.py](lightning_threshold_functions.py) to graph each TC. Note that the source code also includes a 5 intensification stage color-coding option that we did not generate and include in this directory.