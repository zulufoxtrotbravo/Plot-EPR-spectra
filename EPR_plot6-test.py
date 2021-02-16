# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 21:09:49 2021

@author: pathf
"""
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt


li = []# Empty list to store the dataframes from the for loop
#path = r'/home/mika/Documents/python_plotting/25-1-2021_PEDOT-TEMPO/25-1-2021_EPR/g/g_baselined'
path = r'C:\Users\pathf\Documents\25-1-2021_PEDOT-TEMPO\25-1-2021_EPR\g\g_baselined' # use your path
all_files = glob.glob(path + "/*.txt") # Traverse through all files in the folder

for filename in sorted(all_files):      # Read through files 1 at the time and append to li created previously
    df = pd.read_csv(filename, index_col=None, header=None, delimiter=' ')
    li.append(df)
EPR_data = pd.concat(li, axis=1, ignore_index=True)     # Concatenate the df:s to one df

bgr_spectrum = EPR_data.iloc[:,0:2]     # 1st and 2nd columns are made as a BGR spectrum
bgr_spectrum = bgr_spectrum.set_index(0)    # set column 0 as new index
bgr_spectrum.index.name = 'Field (mT)'  # Rename the index column
bgr_spectrum.rename(columns = {1:'bgr'}, inplace=True) # Rename column 
EPR_data = EPR_data.drop(EPR_data.columns[0:2], axis = 1) # And then dropped from the EPR data
EPR_data = EPR_data.drop(EPR_data.columns[2::2], axis=1) # Drop unnecessary field columns also
EPR_data = EPR_data.to_numpy()          # Convert to numpy array to reset the column numbers
EPR_data = pd.DataFrame(EPR_data)       # and then back to df
EPR_data = EPR_data.set_index(0)        # set the 1st column (index=0) with field values to new index       
EPR_data.index.name = 'Field (mT)'

# Apply the mean subtraction here
EPR_data_norm = EPR_data.iloc[:,0]              # Take index and 1st datacolumn
EPR_data_norm = pd.DataFrame(EPR_data_norm).drop([1], axis=1) # Convert to df, then drop the data column

for index in range(EPR_data.shape[1]):
    mean_value = EPR_data.iloc[:,1].mean()
    normalised = EPR_data.iloc[:,1].subtract(mean_value)
    

EPR_data_bgr = EPR_data.iloc[:,0]               # Take index and 1st datacolumn
EPR_data_bgr = pd.DataFrame(EPR_data_bgr)       # Convert to dataframe
EPR_data_bgr = EPR_data_bgr.drop([1], axis=1)   # Then drop the data column for 'empty' df

for index in range(EPR_data.shape[1]): # Take range of the shape of EPR_data along columns
    result = EPR_data.iloc[:,index].subtract(bgr_spectrum.iloc[:,0]) # subtract BGR
    result = pd.DataFrame(result, columns=[index])  # Convert to df
    EPR_data_bgr[index+1] = result          # Add to df holding the results
    
EPR_int = EPR_data_bgr.cumsum()             # Cumsum ignores the field values, as they are indexes
EPR_int2 = EPR_int.cumsum()

max_values = pd.DataFrame(EPR_int2.max(axis=0)) # Create dataFrame for plotting scatter
max_values.reset_index(inplace=True)            # reset index to plot scatter
max_values.rename(columns={'index':'Experiment no.',
                           0:'DI EPR intensity (A.U.)'}, inplace=True) # rename columns
max_values_field = pd.DataFrame(EPR_data.idxmax(axis=0))  # Field values corresponding to max_values