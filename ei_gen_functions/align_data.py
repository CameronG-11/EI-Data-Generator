import pandas as pd
import geopandas as gpd
import sys

'''
Aligns the data to match the order of the helper csv's align_to column.
Only really necessary if you combined 2 datasets in a fashion that shuffled the order of their unique_ids 
from their original shapefile, which may occur for example when grouping a larger and smaller dataset with QGIS. 
'''


def aligning(df, helper_df):

    unique_id_column_name = helper_df['key'][0]

    grouped_df = df
    original_df = helper_df['align_to']

    # print(f"Aligning based on align_to column in helper file")


    # Drops any blank lines. If for some reason you keep getting blank lines, delete the row in the Excel file
    grouped_df.dropna(how='all', inplace=True)
    original_df.dropna(how='all', inplace=True)


    if len(grouped_df) != len(original_df):
        print("Error, Unequal number of columns in files, please fix manually")
        print("grouped:", len(grouped_df))
        print("original:", len(original_df))
        sys.exit()


    try:
        aligned_df = grouped_df.set_index(unique_id_column_name).loc[original_df].reset_index()
    except KeyError as e:
        print(f"Error, Key Error {e} found, please fix manually")
        sys.exit()

    return aligned_df
