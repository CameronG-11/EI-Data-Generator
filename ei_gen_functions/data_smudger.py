import sys
import pandas as pd

'''
PyEI input requires no zero population precincts, so this program replaces them with 1 demographic each
precincts who all did not vote (aka voted for Abstain).
Some datasets will have an more votes in a precinct than total people, likely due to changes in between when
the population was counted and where people lived when the election was. 
This data is just smudged so the over-votes are removed equally from both candidates.
'''



def smudging(df, helper_df):


    total_name = helper_df['total_name'][0]
    key_column = helper_df['key'][0]
    demographic_names = helper_df['new_demographics'].dropna().to_list()
    candidate_names = helper_df['new_candidates'].dropna().to_list()
    abstain_name = helper_df['abstain_name'][0]

    new_columns = [key_column] + [total_name] + demographic_names + candidate_names + [abstain_name]

    zero_smudged_ids = []
    over_pop_ids = [] # # if sum of sub-demographic groups is more than total
    under_pop_ids = [] # # if sum of sub-demographic groups is less than total
    votes_smudged_ids = []
    votes_smudged_counts = 0
    pop_smudged_counts = 0
    broken_count = 0
    added_count = 0

    final_values = []

    for index, row in df.iterrows():

        # re-creation of each row
        buffer = []
        i = 0
        while i < len(new_columns):
            buffer.append(None)
            i = i + 1

        zero_smudged_flag = False
        candidate_sum = 0
        pop_sum = 0 #
        for column, value in row.items():
            # Zero fixing, replace all 0 Total precincts with 1 demographic each
            # precinct who all did not vote (aka voted for Abstain).
            if column == total_name:
                buffer[new_columns.index(total_name)] = value
                if value == 0:
                    # setting each demographic to 1
                    for name in demographic_names:
                        buffer[new_columns.index(name)] = 1

                    # setting total to the # of demographics, as imputed 1 in each demographic.
                    buffer[new_columns.index(total_name)] = len(demographic_names)
                    pop_sum = len(demographic_names)
                    zero_smudged_flag = True

            if column in demographic_names:
                if not zero_smudged_flag:
                    pop_sum = pop_sum + value
                    buffer[new_columns.index(str(column))] = value

            if column in candidate_names:
                candidate_sum = candidate_sum + value
                buffer[new_columns.index(str(column))] = value

            if column == key_column:
                buffer[new_columns.index(str(column))] = value

        # Over-voting fix, subtract from both all candidates equally until fixed
        if candidate_sum > buffer[new_columns.index(total_name)]:
            while candidate_sum > buffer[new_columns.index(total_name)]:
                for candidate in candidate_names:
                    if buffer[new_columns.index(candidate)] > 0:
                        buffer[new_columns.index(candidate)] = buffer[new_columns.index(candidate)] - 1
                        candidate_sum = candidate_sum - 1
                        votes_smudged_counts = votes_smudged_counts + 1
            votes_smudged_ids.append(row[key_column])

        # Over-populated fix, subtract from both all demographics equally until fixed
        if pop_sum > buffer[new_columns.index(total_name)]:
            while pop_sum > buffer[new_columns.index(total_name)]:
                for demographic in demographic_names:
                    if buffer[new_columns.index(demographic)] > 0:
                        buffer[new_columns.index(demographic)] = buffer[new_columns.index(demographic)] - 1
                        pop_sum = pop_sum - 1
                        pop_smudged_counts = pop_smudged_counts + 1
            over_pop_ids.append(row[key_column])

        # Under-populated fix, adding from both all demographics equally until fixed
        # Could add an 'unknown' demographic similar to Abstain, but this would be odd to visualize.
        if pop_sum < buffer[new_columns.index(total_name)]:
            while pop_sum < buffer[new_columns.index(total_name)]:
                for demographic in demographic_names:
                    buffer[new_columns.index(demographic)] = buffer[new_columns.index(demographic)] + 1
                    pop_sum = pop_sum + 1
                    added_count = added_count + 1
                    if pop_sum == buffer[new_columns.index(total_name)]:
                        broken_count = broken_count + 1
                        break
            under_pop_ids.append(row[key_column])

        # adding votes for the Abstain candidate, which represents the people who did not vote
        buffer[new_columns.index(abstain_name)] = buffer[new_columns.index(total_name)] - candidate_sum

        # zero_smudged_ids.append(row[key_column])
        if zero_smudged_flag:
            zero_smudged_ids.append(buffer[new_columns.index(key_column)])

        if None in buffer:
            print("Error, a None is in buffer as not all columns are accounted for or original data has a None")
            sys.exit()
        final_values.append(buffer)


    print(f"\nThere were {len(zero_smudged_ids)} zero population precincts that were smudged, "
          f"totaling {len(zero_smudged_ids) * len(demographic_names)} more equally distributed votes for {abstain_name}")
    print(zero_smudged_ids)
    print(f"There were {len(votes_smudged_ids)} over-voted districts "
          f"whose votes were smudged, totaling {votes_smudged_counts} equally* removed votes.")
    print(f"There were {len(over_pop_ids)} over-populated districts "
          f"whose votes were smudged, totaling {pop_smudged_counts} equally* removed people.")
    print(f"There were {len(under_pop_ids)} under-populated districts of which {broken_count} districts were un-evenly added to,"
          f" totaling {added_count} added people.")
    print(votes_smudged_ids)
    print("*equally removed unless one of the demographics/candidates would become negative, in which case the "
          "remainder is removed from the non-zero candidates/demographics")

    output_df = pd.DataFrame(final_values, columns=new_columns)

    return output_df
