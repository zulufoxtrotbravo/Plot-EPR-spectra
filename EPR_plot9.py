#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 21:23:08 2021

@author: mika
"""

import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import PySimpleGUI as sg

value = ()   # This value determines if RAW or BGR data is returned to the Variable Explorer

#%% Initial folder selection
layout = [[sg.Text("Choose a folder that \ncontains the EPR datafiles: "), sg.Input(), 
           sg.FolderBrowse(key="-IN-")], [sg.T("")], [sg.Button("Submit"), sg.Button('Cancel')],
          [sg.T("")], [sg.T("Press 'Submit' after selecting the correct folder")]]

window = sg.Window('My File Browser', layout, size=(800,200))

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Cancel":
        break
    elif event == "Submit":
        folder = values["-IN-"]
        break
window.close()

#%% Function for plotting with BGR subtracted data, BGR has to be the 1st spectrum in the folder
def plottaaja_BGR():
    global value    # Allow the function to change the gloval variable 'value'
    value = 1       # Set value = 1 to return BGR subtracted results to the variable explorer
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
    
    return bgr_spectrum, EPR_data, EPR_data_bgr, EPR_data_norm, EPR_int, EPR_int2, max_values, max_values_field
#%%

#%% Function for plotting without BGR subtracted RAW data. Relies on very good quality spectra without BGR or baselining problems
def plottaaja_RAW():
    global value    # Allow the function to change the gloval variable 'value'
    value = 0       # Set value = 1 to return BGR subtracted results to the variable explorer
    li = []# Empty list to store the dataframes from the for loop
    path = r'/home/mika/Documents/python_plotting/25-1-2021_PEDOT-TEMPO/25-1-2021_EPR/g/g'
    # path = r'C:\Users\pathf\Documents\25-1-2021_PEDOT-TEMPO\25-1-2021_EPR\g\g' # use your path
    all_files = glob.glob(path + "/*.txt") # Traverse through all files in the folder
    
    for filename in sorted(all_files):      # Read through files 1 at the time and append to li created previously
        df = pd.read_csv(filename, index_col=None, header=None, delimiter=' ')
        li.append(df)
    EPR_data = pd.concat(li, axis=1, ignore_index=True)     # Concatenate the df:s to one df
    
    EPR_data = EPR_data.drop(EPR_data.columns[2::2], axis=1) # Drop unnecessary field columns also
    EPR_data = EPR_data.to_numpy()          # Convert to numpy array to reset the column numbers
    EPR_data = pd.DataFrame(EPR_data)       # and then back to df
    EPR_data = EPR_data.set_index(0)        # set the 1st column (index=0) with field values to new index       
    EPR_data.index.name = 'Field (mT)'   
    
    # Apply the mean subtraction here
    EPR_data_norm = EPR_data.iloc[:,0]              # Take index and 1st datacolumn
    EPR_data_norm = pd.DataFrame(EPR_data_norm).drop([1], axis=1) # Convert to df, then drop the data column
    for index in range(EPR_data.shape[1]):   # Take range of the shape of EPR_data along columns
        mean_value = EPR_data.iloc[:,index].mean()
        normalised = EPR_data.iloc[:,index].subtract(mean_value)
        EPR_data_norm[index+1] = normalised
    
    EPR_int = EPR_data.cumsum()             # Cumsum ignores the field values, as they are indexes
    EPR_int2 = EPR_int.cumsum()
    
    max_values = pd.DataFrame(EPR_int2.max(axis=0)) # Create dataFrame for plotting scatter
    max_values.reset_index(inplace=True)            # reset index to plot scatter
    max_values.rename(columns={'index':'Experiment no.',
                               0:'DI EPR intensity (A.U.)'}, inplace=True) # rename columns
    max_values_field = pd.DataFrame(EPR_int2.idxmax(axis=0))  # Field values corresponding to max_values
    
    return EPR_data, EPR_data_norm, EPR_int, EPR_int2, max_values, max_values_field 
#%%

#%% Ask whether the BGR shoulf be subtracted, or the RAW data plotted

layout2 = [[sg.Text("Do you want to subtract the backqround spectrum from your data?")],
           [sg.Button("Yes"), sg.Button("No")]]
window2 = sg.Window("Concerning background spectgrum (1/3)", layout2, size=(800,300))

layout3 = [[sg.Text("Choose whether the BGR spectrum is the 1st file in the selected folder \n or whether you want to select the BGR file manually.")],
           [sg.T("")],
           [sg.Radio("BGR spectrum is the 1st spectrum", "radio1", default=True)],
           [sg.Radio("Manually Choose the BGR spectrum", "radio1", default=False, key="-IN2")]]
window3 = sg.Window("Concerning background spectrum (2/3", laypout3, size=(800,400))

layout4 = [[sg.T("Select the BGR file:")], sg.Input(), sg.FileBrowse(key="-IN3-")], [sg.Button("Submit")]]
window4 = sg.Window("Concerning backgroud spectrum (3/3)", layout4, size=(800,500))

while True:
    event, values = window2.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == "Yes":
        event, values = window3.read()
        if event == sg.WIN_CLOSED:
            break
        
        elif values["-IN2-"] == True:
            event, values = windows4.read()
            if event == sg.WIN_CLOSED:
                break
            elif event == True:
                plottaaja_BGR()
            elif values["-IN3-"] == True:
                
        
        
        plottaaja_BGR()
    elif event == "No":
        plottaaja_RAW()
    else:
        break
window.close()

#%% Unpack the variables returned by the selected function, plot the unpacked dataframes to visualise results
if value==1:
    bgr_spectrum, EPR_data, EPR_data_bgr,  EPR_data_norm, EPR_int, EPR_int2, max_values, max_values_field = plottaaja_BGR()
    
    fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(10,12))
    fig.subplots_adjust(wspace=0.3, hspace=0.3)
    #fig.tight_layout(h_pad=1) # Can set height padding between the subplots

    EPR_data.plot(ax=axes[0,0], title='Raw Spectra', fontsize=8).legend(loc='upper center', bbox_to_anchor=(0.9, 1.10))
    axes[0,0].ticklabel_format(useMathText=True, useOffset=False, style='scientific',scilimits=(0,0))
    
    bgr_spectrum.plot(ax=axes[0,1], title='Mean normalised BGR spectrum')                    # Plot the BGR spectrum
    EPR_data_norm.plot(ax=axes[0,1], title='Mean normalised EPR spectra', fontsize=8).legend(loc='upper center',bbox_to_anchor=(0.8, 1.00),ncol=2)
    axes[0,1].ticklabel_format(useMathText=True, useOffset=False, style='scientific',scilimits=(0,0))
    axes[0,1].set(ylabel='Mean Norm. EPR spectra')
    
    EPR_data_bgr.plot(ax=axes[1,0], title='Mean norm. & BGR subtract', fontsize=8).legend(loc='upper center',bbox_to_anchor=(0.8, 1.00),ncol=2)
    axes[1,0].ticklabel_format(useMathText=True, useOffset=False, style='scientific',scilimits=(0,0))
    
    EPR_int.plot(ax=axes[1,1],title='1st Integrals', fontsize=8).legend(loc='upper center',bbox_to_anchor=(0.8, 1.05),ncol=2)
    axes[1,1].ticklabel_format(useMathText=True, useOffset=False, style='scientific',scilimits=(0,0))
    
    EPR_int2.plot(ax=axes[2,0],title='2nd Integrals', fontsize=8).legend(loc='upper center',bbox_to_anchor=(0.25, 1.00),ncol=2)
    max_values.plot(ax=axes[2,1],x='Experiment no.',y='DI EPR intensity (A.U.)',kind='scatter')
elif value == 0:
    EPR_data, EPR_data_norm, EPR_int, EPR_int2, max_values, max_values_field = plottaaja_RAW()
    EPR_data.plot(title='Raw EPR spectra')              # Plot data, Field is index, so no need to specify x
    EPR_data_norm.plot(title='Mean normalised EPR spectra')
    EPR_int.plot(title='1st integral')
    EPR_int2.plot(title='2nd integral')     # if you already have a DataFrame instance, then df.plot() offers cleaner syntax than pyplot.plot().
    #plt.plot(EPR_int2)
    #plt.title('2nd Integral for Experiment no.')
    #plt.xlabel('Field (mT)')
    #plt.ylabel('2nd Integral')
    max_values.plot(x='Experiment no.',y='DI EPR intensity (A.U.)',kind='scatter')
else:
    pass
#%% 
