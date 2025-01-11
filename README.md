# EI Data Generator

A collection of Python programs to process data to be suitable for the Metric Geometry and Gerrymandering Group [PyEI](https://github.com/mggg/ecological-inference)

## Overview 

EI_Data_Generator.py runs the programs in the ei_gen_functions folder, which converts combined population and candidate data into data usable for PyEI's calculating functions. It takes command line arguments for input data as well as a helper data file, as well as options for skipping functions or stopping the functions early. 


## Details

The example_data folder holds an example input data, helper, and output file, along with the command arguments to run it. Please refer to this example for proper formatting of data and helper input files.

EI_Data_Generator.py takes in a mandatory data and helper file, an optional output file, and options to skip certain functions. 
The full list of arguments is shown below: (and can also be viewed with -h)
```
data_file: Path to the target data file (required)

helper_file: Path to the target helper file (required)

-ofile, --output_file: Path to output file. Will update the file at each step. (If not included, output data will not be saved)

-start, --start_at: Start the program from a specified step, skipping all prior steps.

-stop, --stop_at: End the program early at a specified step.

-skip, --skip_at: Skip the function at a specified step.
```

Each step is shown below in order of operation, alongside a brief explanation:
```
error_finder: Searches for errors in the data and prints out any found, as they require manual fixing.

group_by_id: Groups each row that shares the same value in their key column. 

align_data: Aligns the data to match the order of the helper CSV's align_to column.
(Only required if the combined data does not match the ordering of the original data sets).

column_editor: Allows for column removing, renaming, or summation.
 
data_smudger: PyEI input requires no zero population precincts, so adds 1 to each demographic for each empty precinct.
Subtracts an equal number of votes from all candidates in cases where there are more votes than the total population.
Prints out the number of values smudged.
(This step is solely for errors in the original data)

to_EI_input: Checks for NULLs and converts demographics to ratios over the total population.
```

Example of command arguments:
```
python3 EI_Data_Generator.py ./22_GA_data/22_WW_Precleaned.xlsx ./22_GA_data/helper_WW.xlsx -ofile=./22_GA_data/outputfile_WW.xlsx -skip=align_to -start=group_by_id -stop=data_smudger
```
