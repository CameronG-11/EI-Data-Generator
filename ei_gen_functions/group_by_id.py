import pandas as pd

'''
Groups each row which shares the same value in their key column. 
Requires a column with a unique ID that you wish to group all of your other values based off of.
Each row should have the same columns (aka no missing values).
'''

def grouping(df, helper_df):
    key_column = helper_df['key'][0]
    # Dropping NaN values, as there will be NaN values if the helper columns are not all of equal length.
    demographics = helper_df['demographics'].dropna().to_list()
    candidates = helper_df['candidates'].dropna().to_list()

    # print(f"Grouping by unique ID stored in column {key_column}")

    # Splitting the data into demographics (to be summed) and candidates (to be taken the same value of)

    # Including the key column to group by for both dataframes

    # Demographics

    # putting the unique_id column first just so it looks better
    demographics.insert(0, key_column)
    population_df = df[demographics]

    grouped_demographics_df = population_df.groupby(key_column, sort=False).sum(numeric_only=True)

    # Candidates

    # putting the unique_id column first just so it looks better
    candidates.insert(0, key_column)
    candidates_df = df[candidates]

    # all the same candidate values for each unique_id row, so can actually just drop duplicates
    grouped_candidates_df = candidates_df.drop_duplicates()

    # merging the individually grouped dataframes
    grouped_df = pd.merge(grouped_demographics_df, grouped_candidates_df, on=key_column)

    return grouped_df


