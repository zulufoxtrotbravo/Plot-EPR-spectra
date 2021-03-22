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
#%%

#%% Function for plotting with BGR subtracted data, BGR has to be the 1st spectrum in the folder
def plottaaja_BGR():
    global value    # Allow the function to change the gloval variable 'value'
    value = 1       # Set value = 1 to return BGR subtracted results to the variable explorer
    li = []# Empty list to store the dataframes from the for loop
    path = folder
    #path = r'C:\Users\pathf\Documents\25-1-2021_PEDOT-TEMPO\25-1-2021_EPR\g\g_baselined' # use your path
    all_files = glob.glob(path + "/*.txt") # Traverse through all files in the folder
    
    for filename in sorted(all_files):      # Read through files 1 at the time and append to li created previously
        df = pd.read_csv(filename, index_col=None, header=None, delimiter=' ')
        li.append(df)
    EPR_data = pd.concat(li, axis=1, ignore_index=True)     # Concatenate the df:s to one df
    
    layout3 = [[sg.Text("Choose whether the BGR spectrum is the 1st file in the selected folder \nor whether you want to select the BGR file manually.")],
        [sg.T("")],
        [sg.T("If the BGR spectrum is the 1st in the folder, click 'Ok'"), sg.T("     "),  sg.Button("Ok")],
        [sg.T("")],
        [sg.T("Otherwise use the 'Browse button to insert the BGR file")],
        [sg.T("Choose the BGR file"), sg.Input(), sg.FileBrowse(key="-IN2-")],
        [sg.T("                                           "), sg.Button("Submit")],
        [sg.T("")],
        [sg.T("                                           "), sg.Button("Cancel")]]
    window3 = sg.Window("Concerning background spectrum", layout3, size=(800,300))    
    
    while True:
        event, values = window3.read()
        if event == sg.WIN_CLOSED or event == "Cancel":
            break
        elif event == "Ok":
            bgr_spectrum = EPR_data.iloc[:,0:2]         # 1st and 2nd columns are made as a BGR spectrum
            bgr_spectrum = bgr_spectrum.set_index(0)    # set column 0 as new index
            bgr_spectrum.index.name = 'Field (mT)'      # Rename the index column
            bgr_spectrum.rename(columns = {1:'bgr'}, inplace=True) # Rename column
            bgr_spectrum = pd.DataFrame(bgr_spectrum.iloc[:,0].subtract(bgr_spectrum.iloc[:,0].mean())) # Mean Normalise also the bgr_spectrum, convert to df
            break
        elif event == "Submit":
            file_path = values["-IN2-"]
            bgr_spectrum = pd.read_csv(file_path, index_col=None, header=None, delimiter=' ')
            bgr_spectrum = bgr_spectrum.set_index(0)    # set column 0 as new index
            bgr_spectrum.index.name = 'Field (mT)'  # Rename the index column
            bgr_spectrum.rename(columns = {1:'bgr'}, inplace=True) # Rename column
            bgr_spectrum = pd.DataFrame(bgr_spectrum.iloc[:,0].subtract(bgr_spectrum.iloc[:,0].mean())) # Mean Normalise also the bgr_spectrum, convert to df
            break
    window3.close()
    
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
    
    
    # Get the EPR signal amplitude from BGR subtracted EPR data
    EPR_amplitude = []     
    for index in range(EPR_data_bgr.shape[1]): # Take range of the shape of EPR_data along columns
        max_amplitude = EPR_data_bgr.iloc[:,index].max()
        min_amplitude = EPR_data_bgr.iloc[:,index].min()
        EPR_amplitude.append(np.absolute(max_amplitude) + np.absolute(min_amplitude))
    EPR_amplitude = pd.DataFrame(EPR_amplitude)     # Convert to DataFrame
    EPR_amplitude.reset_index(inplace=True)     # Reset index to get an additional column for 'Experiment no.'
    EPR_amplitude.rename(columns={'index':'Experiment no.', 
                                  0:'EPR Signal Amplitude (A.U.)'}, inplace =True) # Rename columns
    EPR_amplitude['Experiment no.'] = EPR_amplitude['Experiment no.']+ 1

    # Take 1st and 2nd integrals
    EPR_int = EPR_data_bgr.cumsum()             # Cumsum ignores the field values, as they are indexes
    EPR_int2 = EPR_int.cumsum()
    
    max_values = pd.DataFrame(EPR_int2.max(axis=0)) # Create dataFrame for plotting scatter
    max_values.reset_index(inplace=True)            # reset index to plot scatter
    max_values.rename(columns={'index':'Experiment no.',
                               0:'DI EPR intensity (A.U.)'}, inplace=True) # rename columns
    max_values_field = pd.DataFrame(EPR_int2.idxmax(axis=0))  # Field values corresponding to max_values
    
    return bgr_spectrum, EPR_data, EPR_data_bgr, EPR_data_norm, EPR_int, EPR_int2, max_values, max_values_field, EPR_amplitude
#%%

#%% Function for plotting without BGR subtracted RAW data. Relies on very good quality spectra without BGR or baselining problems
def plottaaja_RAW():
    global value    # Allow the function to change the gloval variable 'value'
    value = 0       # Set value = 1 to return BGR subtracted results to the variable explorer
    li = []# Empty list to store the dataframes from the for loop
    path = folder
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
    
    # Get the EPR signal amplitude from BGR subtracted EPR data
    EPR_amplitude = []     
    for index in range(EPR_data_norm.shape[1]): # Take range of the shape of EPR_data along columns
        max_amplitude = EPR_data_norm.iloc[:,index].max()
        min_amplitude = EPR_data_norm.iloc[:,index].min()
        EPR_amplitude.append(np.absolute(max_amplitude) + np.absolute(min_amplitude))
    EPR_amplitude = pd.DataFrame(EPR_amplitude)     # Convert to DataFrame
    EPR_amplitude.reset_index(inplace=True)     # Reset index to get an additional column for 'Experiment no.'
    EPR_amplitude.rename(columns={'index':'Experiment no.', 
                                  0:'EPR Signal Amplitude (A.U.)'}, inplace =True) # Rename columns
    EPR_amplitude['Experiment no.'] = EPR_amplitude['Experiment no.']+ 1
    
    EPR_int = EPR_data_norm.cumsum()             # Cumsum ignores the field values, as they are indexes
    EPR_int2 = EPR_int.cumsum()
    
    max_values = pd.DataFrame(EPR_int2.max(axis=0)) # Create dataFrame for plotting scatter
    max_values.reset_index(inplace=True)            # reset index to plot scatter
    max_values.rename(columns={'index':'Experiment no.',
                               0:'DI EPR intensity (A.U.)'}, inplace=True) # rename columns
    max_values_field = pd.DataFrame(EPR_int2.idxmax(axis=0))  # Field values corresponding to max_values
    
    return EPR_data, EPR_data_norm, EPR_int, EPR_int2, max_values, max_values_field, EPR_amplitude
#%%

#%% Ask whether the BGR shoulf be subtracted, or the RAW data plotted

layout2 = [[sg.Text("Do you want to subtract the backqround spectrum from your data?")],
           [sg.T("")],
           [sg.T("                   "), sg.Button("Yes"), sg.Button("No"), sg.Button("Cancel")]]
window2 = sg.Window("Concerning background spectgrum (and Hobbits)", layout2, size=(600,200))

while True:
    event, values = window2.read()
    if event == sg.WIN_CLOSED or event == "Cancel":
        break
    elif event == "Yes":
        #window2.close()           
        plottaaja_BGR()
        break
    elif event == "No":
        plottaaja_RAW()
        break
window2.close()

#%% Unpack the variables returned by the selected function, plot the unpacked dataframes to visualise results
if value==1:
    bgr_spectrum, EPR_data, EPR_data_bgr,  EPR_data_norm, EPR_int, EPR_int2, max_values, max_values_field, EPR_amplitude = plottaaja_BGR()
    
    fig, ax1 = plt.subplots(nrows=3, ncols=2, figsize=(10,12))
    fig.subplots_adjust(wspace=0.3, hspace=0.3)
    #fig.tight_layout(h_pad=1) # Can set height padding between the subplots

    EPR_data.plot(ax=ax1[0,0], title='Raw Spectra', fontsize=8).legend(loc='upper center', bbox_to_anchor=(0.9, 1.10))
    ax1[0,0].ticklabel_format(useMathText=True, useOffset=False, style='scientific',scilimits=(0,0))
    
    bgr_spectrum.plot(ax=ax1[0,1], title='Mean normalised BGR spectrum')                    # Plot the BGR spectrum
    EPR_data_norm.plot(ax=ax1[0,1], title='Mean normalised EPR spectra', fontsize=8).legend(loc='upper center',bbox_to_anchor=(0.8, 1.00),ncol=2)
    ax1[0,1].ticklabel_format(useMathText=True, useOffset=False, style='scientific',scilimits=(0,0))
    ax1[0,1].set(ylabel='Mean Norm. EPR spectra')
    
    EPR_data_bgr.plot(ax=ax1[1,0], title='Mean norm. & BGR subtract', fontsize=8).legend(loc='upper center',bbox_to_anchor=(0.8, 1.00),ncol=2)
    ax1[1,0].ticklabel_format(useMathText=True, useOffset=False, style='scientific',scilimits=(0,0))
    
    EPR_int.plot(ax=ax1[1,1],title='1st Integrals', fontsize=8).legend(loc='upper center',bbox_to_anchor=(0.8, 1.05),ncol=2)
    ax1[1,1].ticklabel_format(axis='y', useMathText=False, useOffset=False, style='scientific',scilimits=(0,0))
    
    EPR_int2.plot(ax=ax1[2,0],title='2nd Integrals', fontsize=8).legend(loc='upper center',bbox_to_anchor=(0.25, 1.00),ncol=2)
    
    max_values.plot(ax=ax1[2,1],x='Experiment no.',y='DI EPR intensity (A.U.)',s=50, kind='scatter') # s=100 sets the marker size
    
    ax2 = ax1[2,1].twinx() # Need to create an instance of a specific subplot for which the 2nd y-axis is needed
    ax2.tick_params(labelcolor='red')           # Coloring of the numbers of Y2-axis
    ax2.set_ylabel('Y2-axis', color='red')      # Coloring of the label of Y2-axis
    EPR_amplitude.plot(ax=ax2, title='DI and SA vs experiment no.', x='Experiment no.',   # and then used it here
                       y='EPR Signal Amplitude (A.U.)',color='red', kind='scatter')
    ax2.ticklabel_format(useMathText=True, useOffset=False, style='scientific',scilimits=(0,0))
    
elif value == 0:
    EPR_data, EPR_data_norm, EPR_int, EPR_int2, max_values, max_values_field, EPR_amplitude = plottaaja_RAW()
    
    fig, ax1 = plt.subplots(nrows=3, ncols=2, figsize=(10,12))
    fig.subplots_adjust(wspace=0.3, hspace=0.3)
    #fig.tight_layout(h_pad=1) # Can set height padding between the subplots
    
    EPR_data.plot(ax=ax1[0,0], title='Raw Spectra', fontsize=8).legend(loc='upper center', bbox_to_anchor=(0.9, 1.10))
    ax1[0,0].ticklabel_format(useMathText=True, useOffset=False, style='scientific',scilimits=(0,0))
    
    EPR_data_norm.plot(ax=ax1[0,1], title='Mean normalised EPR spectra', fontsize=8).legend(loc='upper center',bbox_to_anchor=(0.8, 1.00),ncol=2)
    ax1[0,1].ticklabel_format(useMathText=True, useOffset=False, style='scientific',scilimits=(0,0))
    ax1[0,1].set(ylabel='Mean Norm. EPR spectra')
    
    EPR_int.plot(ax=ax1[1,0],title='1st Integrals', fontsize=8).legend(loc='upper center',bbox_to_anchor=(0.8, 1.05),ncol=2)
    ax1[1,0].ticklabel_format(useMathText=True, useOffset=False, style='scientific',scilimits=(0,0))
    
    EPR_int2.plot(ax=ax1[1,1],title='2nd Integrals', fontsize=8).legend(loc='upper center',bbox_to_anchor=(0.25, 1.00),ncol=2)
    
    max_values.plot(ax=ax1[2,0],x='Experiment no.',y='DI EPR intensity (A.U.)',kind='scatter')
    
    ax2 = ax1[2,0].twinx() # Need to create an instance of a specific subplot for which the 2nd y-axis is needed
    ax2.tick_params(labelcolor='red')           # Coloring of the numbers of Y2-axis
    ax2.set_ylabel('Y2-axis', color='red')      # Coloring of the label of Y2-axis
    EPR_amplitude.plot(ax=ax2, title='DI and SA vs experiment no.', x='Experiment no.',   # and then used it here
                       y='EPR Signal Amplitude (A.U.)',color='red', kind='scatter')
    ax2.ticklabel_format(useMathText=True, useOffset=False, style='scientific',scilimits=(0,0))
    
else:
    pass
#%% Delete unnecessary variables from the workspace
del ax1, ax2, event, fig, layout, layout2, value, values
