#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 20:20:28 2021

@author: mika
"""

#%% Imports
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import tkinter
from tkinter import Tk, Label, constants, ttk, Entry, Button, INSERT, END, Message, messagebox, Toplevel
#%% 

#%% code body
li = []# Empty list to store the dataframes from the for loop
path = r'/home/mika/Documents/python_plotting/25-1-2021_PEDOT-TEMPO/25-1-2021_EPR/g/g_baselined'
#path = r'C:\Users\pathf\Documents\25-1-2021_PEDOT-TEMPO\25-1-2021_EPR\g\g_baselined' # use your path
all_files = glob.glob(path + "/*.txt") # Traverse through all files in the folder

for filename in sorted(all_files):      # Read through files 1 at the time and append to li created previously
    df = pd.read_csv(filename, index_col=None, header=None, delimiter=' ')
    li.append(df)
EPR_data = pd.concat(li, axis=1, ignore_index=True)     # Concatenate the df:s to one df

bgr_spectrum = EPR_data.iloc[:,0:2]     # 1st and 2nd columns are made as a BGR spectrum
bgr_spectrum = bgr_spectrum.set_index(0)    # set column 0 as new index
bgr_spectrum.index.name = 'Field (mT)'  # Rename the index column
bgr_spectrum.rename(columns = {1:'bgr'}, inplace=True) # Rename column
bgr_spectrum = pd.DataFrame(bgr_spectrum.iloc[:,0].subtract(bgr_spectrum.iloc[:,0].mean())) # Mean Normalise also the bgr_spectrum, convert to df
EPR_data = EPR_data.drop(EPR_data.columns[0:2], axis = 1) # And then dropped from the EPR data
EPR_data = EPR_data.drop(EPR_data.columns[2::2], axis=1) # Drop unnecessary field columns also
EPR_data = pd.DataFrame(EPR_data.to_numpy())          # Convert to numpy array to reset the column numbers, and then back to df      
EPR_data = EPR_data.set_index(0)        # set the 1st column (index=0) with field values to new index       
EPR_data.index.name = 'Field (mT)'

# Mean normalise the data here
EPR_data_norm = EPR_data.iloc[:,0]              # Take index and 1st datacolumn
EPR_data_norm = pd.DataFrame(EPR_data_norm).drop([1], axis=1) # Convert to df, then drop the data column
for index in range(EPR_data.shape[1]):   # Take range of the shape of EPR_data along columns
    mean_value = EPR_data.iloc[:,index].mean()
    normalised = EPR_data.iloc[:,index].subtract(mean_value)
    EPR_data_norm[index+1] = normalised

# Subtract BGR here
EPR_data_bgr = EPR_data.iloc[:,0]               # Take index and 1st datacolumn
EPR_data_bgr = pd.DataFrame(EPR_data_bgr)       # Convert to dataframe
EPR_data_bgr = EPR_data_bgr.drop([1], axis=1)   # Then drop the data column for 'empty' df

for index in range(EPR_data.shape[1]): # Take range of the shape of EPR_data along columns
    result = EPR_data_norm.iloc[:,index].subtract(bgr_spectrum.iloc[:,0]) # subtract BGR
    result = pd.DataFrame(result, columns=[index])  # Convert to df
    EPR_data_bgr[index+1] = result          # Add to df holding the results
    
EPR_int = EPR_data_bgr.cumsum()             # Cumsum ignores the field values, as they are indexes
EPR_int2 = EPR_int.cumsum()

max_values = pd.DataFrame(EPR_int2.max(axis=0)) # Create dataFrame for plotting scatter
max_values.reset_index(inplace=True)            # reset index to plot scatter
max_values.rename(columns={'index':'Experiment no.',
                           0:'DI EPR intensity (A.U.)'}, inplace=True) # rename columns
max_values_field = pd.DataFrame(EPR_int2.idxmax(axis=0))  # Field values corresponding to max_values
#%%


#%% Ask if linewidths are required


def get_linewidth():
    answer = Toplevel()
    answer = messagebox.askquestion('Yks juttu:','Haluatko tietää signaalin leveyden? Tätä pitää kysyä että tämä kysymysboksi olisi isompi.')
    if answer == 'yes':
        global line_widths
        line_widths = []
        if 'EPR_data_bgr' in globals(): # If BGR subtraction was selected, run this loop
            for index in range(EPR_data_bgr.shape[1]):  # Take range of the shape of EPR_data along columns
                max_value = EPR_data_bgr.iloc[:,index].idxmax()
                min_value = EPR_data_bgr.iloc[:,index].idxmin()
                line_width = min_value-max_value
                line_widths.append(line_width)
        else:                           # If plotting of RAW was selected, run this loop
            for index in range(EPR_data_norm.shape[1]): # Take range of the shape of EPR_data along columns
                max_value = EPR_data_norm.iloc[:,index].idxmax()
                min_value = EPR_data_norm.iloc[:,index].idxmin()
                line_width = min_value-max_value
                line_widths.append(line_width)
        return line_widths
    else:
        root.destroy
    # line_widths = get_linewidth() # Need to intend so the function is not called    

root = Tk()
root.geometry("600x400+700+500")
root.title('Python Guides')
root.config(bg='#345')
button1 = Button(root,text="Concerning EPR linewidths",command=get_linewidth).pack(pady=80)
button2 = Button(root,text='Close WIndow', command=root.destroy).pack(pady=80)
root.mainloop()

if 'line_widths' in globals():    
    line_widths = pd.DataFrame(line_widths, columns=['Line widths (mT) FWHH'])
else:
    pass

del button1, button2, filename, index, li, path, all_files, result, normalised, mean_value, root, df
