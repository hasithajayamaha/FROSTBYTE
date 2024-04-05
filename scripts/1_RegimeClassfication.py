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


if __name__ == "__main__":
    main()
