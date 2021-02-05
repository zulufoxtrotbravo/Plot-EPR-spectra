# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 15:45:57 2021

@author: pathf
"""
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
li = []# Empty list to store the dataframes from the for loop

path = r'C:\Users\pathf\Documents\25-1-2021_PEDOT-TEMPO\25-1-2021_EPR\g\g_baselined' # use your path
all_files = glob.glob(path + "/*.txt") # Read all files from the folder

for filename in all_files:      # Read files 1 at the time and append to li created previously
    df = pd.read_csv(filename, index_col=None, header=None, delimiter=' ')
    li.append(df)
EPR_data = pd.concat(li, axis=1, ignore_index=True)     # Concatenate the df:s to one df

EPR_data = EPR_data.drop(EPR_data.columns[2::2], axis=1) # Drop unnecessary field columns
EPR_data.plot(x=0)                                          # Plot data with 0th column as x

#%% Manipulate the dataframe to give integrals and plot them

EPR_data = EPR_data.set_index(0)        # set the 1st column (index=0) with field values to new index       
EPR_int = EPR_data.cumsum()             # Now the cumsum ignores the field values
# EPR_1stInt = EPR_data.loc[:,1:].cumsum()
EPR_int.plot()

EPR_int2 = EPR_int.cumsum()
EPR_int2.plot()

#%% Get the maximum value from the spectra and their field value

max_values = EPR_data.max(axis=0)
# max_values.plot(kind='scatter')
max_values2 = EPR_data.idxmax(axis=0)
plt.plot(max_values,'ro')


