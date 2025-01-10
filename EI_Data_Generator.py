import sys
import argparse
import pandas as pd
from ei_gen_functions.error_finder import finding
from ei_gen_functions.group_by_id import grouping
from ei_gen_functions.align_data import aligning
from ei_gen_functions.column_editor import editing
from ei_gen_functions.data_smudger import smudging
from ei_gen_functions.to_EI_input import converting

parser = argparse.ArgumentParser()

parser.add_argument('data_file', type=str, help="path to target data file.")
parser.add_argument('helper_file', type=str, help="path to target helper file.")
parser.add_argument('-ofile','--output_file', type=str, help="path to output file. Will update file at each step.")

parser.add_argument('-start', '--start_at', type=str, help='Start the program from a specified step, '
                                                         'skipping all prior steps. Steps:'
                                                         '[error_finder, group_by_id, align_data, column_editor, '
                                                         'data_smudger, to_EI_input]')

parser.add_argument('-stop', '--stop_at', type=str, help='End the program early at a specified step via their file name. '
                                                        'Steps: [error_finder, group_by_id, align_data, column_editor,'
                                                         ' data_smudger, to_EI_input]')

parser.add_argument('-skip', '--skip_at', type=str, help='Skip the program at a specified step, '
                                                         'skipping all prior steps. Steps:'
                                                         '[error_finder, group_by_id, align_data, column_editor, '
                                                         'data_smudger, to_EI_input]')


args = parser.parse_args()

input_file = args.data_file
helper_file = args.helper_file
output_file = args.output_file

print(f"Reading from data file {input_file} and helper file {helper_file}\n")
df = pd.read_excel(input_file)
helper_df = pd.read_excel(helper_file)

# Of note, are in order
subroutines = {'error_finder':finding, 'group_by_id': grouping, 'align_data':aligning, 'column_editor':editing, 'data_smudger':smudging, 'to_EI_input':converting}


skip = args.start_at is not None

skip_steps =  args.skip_at
# print(skip_steps)

if skip and args.start_at not in subroutines:
    print(f'ERROR, -start (--start_at) was given an improper input, \"{args.start_at}\". '
          f'\nIt must be one of the following: {subroutines}'
          f'\nEnter -h for further help.')
    sys.exit()

if args.stop_at is not None and args.stop_at not in subroutines:
    print(f'ERROR, -stop (--stop_at) was given an improper input, \"{args.stop_at}\". '
          f'\nIt must be one of the following: {subroutines}'
          f'\nEnter -h for further help.')
    sys.exit()

for name, function in subroutines.items():

    if skip and args.start_at != name:
        print(f'Skipping {name} as to start at {args.start_at}')
    elif skip_steps is not None and name in skip_steps:
        print(f'Skipping step {name} as per -skip')
    else:
        print(f'{name} executes')
        df = function(df, helper_df)
        skip = False

    if args.stop_at == name:
        break


if output_file is not None:
    df.to_excel(output_file, index=False)
    print('\nNew excel file saved at', output_file)

print(df.head())



print("\nFinished")
