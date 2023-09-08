# BraTS-Reg registration challenge using Elastix

* The challenge: https://www.med.upenn.edu/cbica/brats-reg-challenge/
* ITKElastix: https://github.com/InsightSoftwareConsortium/ITKElastix

## File explanation

1. ``brats-reg-analysis.py``: Runs the registration for each subject and saves the results. Make sure to speficy the correct filepaths in ``fileconfig.py`` first.
2. ``calculate-point-distance.py``: Transforms the landmarks based on the previous registration, and calculates the median point distance (metric specified by the challenge) before and after registration per subject.
3. ``landmark-reader``: Contains a napari plugin that loads and visualizes the landmarks to aid visual inspection. To use, run ``pip install elastix-napari`` and then ``pip install -e .`` inside the landmark-reader directory.

