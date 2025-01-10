import pandas as pd

'''
Allows for column removing, renaming, or summation.
Uses the helper csv's remove, rename_from, rename_to, sum_from, and sum_to columns (all of which are self explanatory).
'''

def editing(df, helper_df):

    # Can either remove, rename, or sum columns using this program
    # Summing replaces all sum_from columns with their sum_to columns

    # Renaming

    rename_from = helper_df['rename_from'].dropna().tolist()
    rename_to = helper_df['rename_to'].dropna().tolist()
    rename_mappings = dict(zip(rename_from, rename_to))

    # print(f'Renaming the columns: {rename_from}\nTo columns {rename_to}')

    df = df.rename(columns=rename_mappings)


    # Summing
    sum_from = helper_df['sum_from'].dropna().tolist()
    sum_to = helper_df['sum_to'].dropna().tolist()
    sum_mappings = zip(sum_from, sum_to)

    # print(f'Summing from columns: {sum_from}\nTo columns {sum_to}')

    # Set each sum_to column equal to it plus it all its sum_froms.
    for from_name, to_name  in sum_mappings:

        # Creating a new column if the to_name column is not already in the df
        if to_name not in df.columns:
            df[to_name] = df[from_name]

        # Else update column values to sum to additional sum_froms
        else:
            df[to_name] = df[to_name] + df[from_name]


    # Removing

    columns_to_remove = helper_df['remove'].dropna().tolist()
    # returns a list of all the column names
    column_names = df.columns.tolist()
    # Adding all the sum_from columns to be removed (as they are replaced by their sum_to columns)
    columns_to_remove = columns_to_remove + sum_from

    # print(f'Removing columns: {columns_to_remove}')

    for column in columns_to_remove:
        column_names.remove(column)

    # reset df to be only equal to its non_removed columns
    df = df[column_names]

    return df