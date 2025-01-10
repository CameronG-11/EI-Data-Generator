import sys
import pandas as pd

'''
The final step, just checking for NULL values and converting demographics to ratios over total population.
'''

def converting(df, helper_df):

    total_name = helper_df['total_name'][0]
    key_column = helper_df['key'][0]

    final_values = []

    for index, row in df.iterrows():
        buffer = []
        total = row[total_name]
        for column, value in row.items():
            # Should not be the case as should already have fixed errors,
            #  but just in case this step was skipped (or an artifact occurred)
            if pd.isnull(value):
                # since these are aberrations with no real pattern, they are best handled manually
                # as opposed to a blanket fix which may not always be appropriate.
                print(f"Row {index} (which can found at A{int(index) + 2} in the excel file)"
                      f" is missing its value for {column}! Please fix this issue manually \nAborting Program")
                sys.exit()

            # keep unmodified totals and unique_ids
            if column == key_column or column == total_name:
                buffer.append(value)
            else:
                buffer.append(value/total)

        final_values.append(buffer)

    output_df = pd.DataFrame(final_values, columns=df.columns.to_list())

    return output_df
