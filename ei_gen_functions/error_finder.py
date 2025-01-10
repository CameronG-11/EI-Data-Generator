import sys
import pandas as pd

'''
Searches for errors in the data and prints out any found (as they require manual fixing).
Each row should have the same column length, and should have no Nulls.
'''


def finding(df, helper_df):

    set_first_row_length = True
    row_length = -1

    for index, row in df.iterrows():
        # all rows must be equal, so can just test against the first row's length with no need to reset it constantly
        if set_first_row_length:
            row_length = len(row)
            set_first_row_length = False

        # checking if the row is equal to all other rows
        if len(row) != row_length:
            # since these are aberrations with no real pattern, they are best handled manually
            # as opposed to a blanket fix which may not always be appropriate.
            print(f"Row {index} (which can found at A{int(index) + 2} in the excel file)"
                  f" is unequal to the other previous rows in length")
            sys.exit()

        for column, value in row.items():
            # check for missing values in the data, sometimes caused by QGIS's geometric functions

            if pd.isnull(value):
                # since these are aberrations with no real pattern, they are best handled manually
                # as opposed to a blanket fix which may not always be appropriate.
                print(f"Row {index} (which can found at A{int(index) + 2} in the excel file)"
                      f" is missing its value for {column}! Please fix this issue manually \nAborting Program")
                sys.exit()

    print("No Data Errors Found.")

    return df
