# EI_Helpers

A collection of Python programs to process data to be suitable for the Metric Geometry and Gerrymandering Group [PyEI](https://github.com/mggg/ecological-inference) Library as well as programs to convert that data into more easily visualizable data (see my [ei_viz](https://github.com/CameronG-11/ei_viz) repository for examples).

EI_Data_Generator.py runs the programs in the ei_gen_functions folder, which converts combined population and candidate data into data usable for PyEI's calculating functions. It takes command line arguments for input data as well as a helper data file, as well as options for skipping functions or stopping the functions early. 

For details, see the example_data folder for proper formatting of input data, and the code itself for brief explanations of each function.

The programs in the csv_functions folder take the produced EI data and extract data useful for visualizations. 
