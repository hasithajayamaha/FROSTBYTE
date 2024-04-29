import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.wkt import loads as wkt_loads
import sys
from datetime import datetime, timedelta

def read_and_merge_data(read_csv, time_filter):
    read_csv_filter = read_csv.loc[read_csv['time'] == time_filter]
    read_csv_filter['geometry'] = read_csv_filter['geometry'].apply(wkt_loads)
    return gpd.GeoDataFrame(read_csv_filter, geometry='geometry')


def plot_data(df, column_plot, ax, pltsaveloc, time_filter):
    df.plot(column=column_plot, ax=ax, legend=True, markersize=10, cmap='coolwarm')
    plt.title(column_plot)
    plt.savefig(pltsaveloc + time_filter + '_' + column_plot + '.png')
    plt.close()


def plot_runoff(df, time_filter, pltsaveloc):
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    us = world[world['continent'] == 'North America']
    columns_to_plot = ['averageRoutedRunoff_mean', 'pptrate_mean', 'scalarSWE']
    for column_plot in columns_to_plot:
        fig, ax = plt.subplots(1, 1)
        us.plot(ax=ax, linewidth=0.8, color='lightgray', edgecolor='black')
        ax.set_aspect('equal')
        plot_data(df, column_plot, ax, pltsaveloc, time_filter)


# File paths
output = '/Users/hasithaj/PycharmProjects/FROSTBYTE/capstone_data/data/'
pltsaveloc = '/Users/hasithaj/PycharmProjects/FROSTBYTE/capstone_data/plot/'

read_csv = pd.read_csv(output + "animation_df.csv").reset_index()
gdf_catchment = pd.read_csv(output + "gdf_catchment_df.csv").reset_index()
merged_df = pd.merge(gdf_catchment, read_csv, left_on='hruId', right_on='hru', how='left')

cols_to_drop = ['Unnamed: 0_x', 'index_x', 'hruId', 'level_0', 'latitude',
                'longitude', 'index_y', 'Unnamed: 0_y', 'hru']
merged_df = merged_df.drop(columns=cols_to_drop)

# Here time_filter is the parameter you get from the shell script.
# Make sure to pass the full date as the parameter while calling this script.
# Example "python3 your_script_name.py 1998"
year = sys.argv[1]



# constructor of dates
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


# start and end dates for one year
start_date = datetime.strptime(year + '-01-01', '%Y-%m-%d')
end_date = datetime.strptime(year + '-12-31', '%Y-%m-%d')

for single_date in daterange(start_date, end_date):
    time_filter = single_date.strftime('%Y-%m-%d')
    print('Running for date: ', time_filter)
    gdf = read_and_merge_data(merged_df, time_filter)
    plot_runoff(gdf, time_filter, pltsaveloc)