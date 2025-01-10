erroneous_combined_data.xlsx is the combination of ga_gen_20_st_prec.shp (Georgia 2020 voting data) combined with ga_pl2020_p4_b (Georgia 2020 population and demographic data), both sourced from the Redistricting Data Hub (https://redistrictingdatahub.org/). The data was combined using QGIS(https://www.qgis.org/) and its Join Attributes by Location Data Management tool. 

combined_data.xlsx is the same data after having some errors fixed (found via the ei_gen_functions/error_finder.py program) which should be used for input into the EI_Data_Generator program. helper.xlsx is an example helper file for said data.

processed_data.xlsx is the result of combined_data.xlsx after being ran with EI_Data_Generator with the arguments [./example_data/combined_data.xlsx ./example_data/helper.xlsx -ofile=./example_data/processed_data.xlsx]. It is what would be input into PyEI in order to run ecological inference on the original Georgia 2020 voting data.
