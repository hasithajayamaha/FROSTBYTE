import logging
#%matplotlib notebook
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
from pprint import pprint
import sys
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)
import xarray as xr
from utilities import setup_logging, read_settings
from functions import regime_classification, polar_plot

def main():
    setup_logging()

    # Set up logging for this notebook
    logger = logging.getLogger()

    # Suppress misc. comments from being added to the log file
    logging.getLogger('matplotlib.font_manager').disabled = True
    logging.getLogger('matplotlib.pyplot').disabled = True
    pass
    logger.debug(f'Notebook: 1_RegimeClassification')

    settings = read_settings('../settings/config_test_case.yaml', log_settings=True)
    pprint(settings)

    # Set user-specified variables
    test_basin_id = settings['domain']  # Can override this with testbasin_id = <string of the testbasin id>, make sure that this id is in the input data files
    nival_start_doy_default = 60  # nival regime starting day of year, corresponds to the 1st of March
    nival_end_doy_default = 213  # nival regime ending day of year, corresponds to the 1st of August
    nival_regularity_threshold_default = 0.65  # nival regime minimum regularity threshold
    month_start_water_year_default, day_start_water_year_default = 10, 1  # water year start
    month_end_water_year_default, day_end_water_year_default = 9, 30  # water year end
    max_gap_days_default = 15  # max. number of days for gaps allowed in the daily streamflow data for the linear interpolation

    # Save the user-specified variables to the log file
    logger.debug(f'test basin ID: {test_basin_id}')
    logger.debug(f'nival regime start DOY: {nival_start_doy_default}')
    logger.debug(f'nival regime end DOY: {nival_end_doy_default}')
    logger.debug(f'regularity threshold: {nival_regularity_threshold_default}')
    logger.debug(f'water year start (month/day): {month_start_water_year_default}/{day_start_water_year_default}')
    logger.debug(f'water year end (month/day): {month_end_water_year_default}/{day_end_water_year_default}')
    logger.debug(f'linear interpolation maximum gap (days): {max_gap_days_default}')

    # Read the basin outlet's daily streamflow data as a DataArray
    Qobs_ds = xr.open_dataset(settings['streamflow_obs_path'])
    Qobs_testbasin_ds = Qobs_ds.where(Qobs_ds.Station_ID == test_basin_id, drop=True)
    Qobs_testbasin_ds = Qobs_testbasin_ds.set_index({"Station_ID": "Station_ID"})

    print(Qobs_testbasin_ds)# Plot a climatological hydrograph for the basin
    # Plot a climatological hydrograph for the basin
    fig = plt.figure()
    streamflow_data_da = Qobs_testbasin_ds.Flow
    doy_mean = streamflow_data_da.groupby("time.dayofyear").mean(skipna=True)
    plt.plot(np.arange(366), doy_mean.values, color='b')
    plt.ylabel('mean climatological streamflow [m3/s]')
    plt.xticks(np.arange(0, 360, 30),
               ['1st Jan', '1st Feb', '1st Mar', '1st Apr', '1st May', '1st Jun', '1st Jul', '1st Aug', '1st Sep',
                '1st Oct', '1st Nov', '1st Dec'], rotation=45)
    plt.tight_layout()


if __name__ == "__main__":
    main()
