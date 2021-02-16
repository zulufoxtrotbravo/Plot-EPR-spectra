#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 14 12:44:59 2021

@author: mika
"""

#%% Imports
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
import tkinter
from tkinter import Tk, Label, constants, ttk, Entry, Button, INSERT, END, Message
value = 0

#%% ANALYSE BGR SUBTRACTED

def plottaaja_BGR():
    global value
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
    EPR_data = EPR_data.drop(EPR_data.columns[0:2], axis = 1) # And then dropped from the EPR data
    EPR_data = EPR_data.drop(EPR_data.columns[2::2], axis=1) # Drop unnecessary field columns also
    EPR_data = EPR_data.to_numpy()          # Convert to numpy array to reset the column numbers
    EPR_data = pd.DataFrame(EPR_data)       # and then back to df
    EPR_data = EPR_data.set_index(0)        # set the 1st column (index=0) with field values to new index       
    EPR_data.index.name = 'Field (mT)'
    
    bgr_spectrum.plot()                     # Plot the BGR spectrum
    
    EPR_data_bgr = EPR_data.iloc[:,0]               # Take index and 1st datacolumn
    EPR_data_bgr = pd.DataFrame(EPR_data_bgr)       # Convert to dataframe
    EPR_data_bgr = EPR_data_bgr.drop([1], axis=1)   # Then drop the data column for 'empty' df
    
    for index in range(EPR_data.shape[1]): # Take range of the shape of EPR_data along columns
        result = EPR_data.iloc[:,index].subtract(bgr_spectrum.iloc[:,0]) # subtract BGR
        result = pd.DataFrame(result, columns=[index])  # Convert to df
        EPR_data_bgr[index+1] = result          # Add to df holding the results
        
    EPR_data_bgr.plot(title='BGR subtracted Spectra', fontsize=12)
    EPR_int = EPR_data_bgr.cumsum()             # Cumsum ignores the field values, as they are indexes
    EPR_int.plot(title='1st Integrals', fontsize=12)
    EPR_int2 = EPR_int.cumsum()
    EPR_int2.plot(title='2nd Integrals', fontsize=12)
    
    max_values = pd.DataFrame(EPR_int2.max(axis=0)) # Create dataFrame for plotting scatter
    max_values.reset_index(inplace=True)            # reset index to plot scatter
    max_values.rename(columns={'index':'Experiment no.',0:'DI EPR intensity (A.U.)'},inplace=True) # Rename columns
    max_values_field = pd.DataFrame(EPR_data.idxmax(axis=0))  # Field values corresponding to max_values
    max_values.plot(x='Experiment no.',y='DI EPR intensity (A.U.)',kind='scatter')
    value = 1
    
    return bgr_spectrum, EPR_data, EPR_data_bgr,  EPR_int, EPR_int2, max_values, max_values_field
# desc_BGR = plottaaja_BGR()  # Pack all return values to a single tuple - could then use iterable unpacking
# bgr, data, data_bgr, int1, int2, maxv, maxv_field, value = desc_BGR
# bgr_spectrum, EPR_data, EPR_data_bgr,  EPR_int, EPR_int2, max_values, max_values_field, value = plottaaja_BGR()
 
#%% ANALYSE RAW

def plottaaja_RAW():
    li = []# Empty list to store the dataframes from the for loop
    path = r'/home/mika/Documents/python_plotting/25-1-2021_PEDOT-TEMPO/25-1-2021_EPR/g/g_baselined'
    #path = r'C:\Users\pathf\Documents\25-1-2021_PEDOT-TEMPO\25-1-2021_EPR\g\g_baselined' # use your path
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
    
    plt.plot(EPR_data)
    plt.title('EPR spectra for Experiment no.XOXO')
    plt.xlabel('Field (mT)')
    plt.ylabel('Signal intensity (A.U.)')
    plt.show()
    
    EPR_int = EPR_data.cumsum()             # Cumsum ignores the field values, as they are indexes
    plt.plot(EPR_int)
    plt.title('1st Integral for Experiment no.')
    plt.xlabel('Field (mT)')
    plt.show()
    
    EPR_int2 = EPR_int.cumsum()
    plt.plot(EPR_int2)
    plt.title('2nd Integral for Experiment no.')
    plt.xlabel('Field (mT)')
    plt.show()
   
    max_values = pd.DataFrame(EPR_int2.max(axis=0)) # Create dataFrame for plotting scatter
    max_values.reset_index(inplace=True)            # reset index to plot scatter
    max_values.rename(columns={'index':'Experiment no.',0:'DI EPR intensity (A.U.)'}, inplace=True) # rename column
    max_values_field = pd.DataFrame(EPR_int2.idxmax(axis=0))  # Field values corresponding to max_values
    max_values.plot(x='Experiment no.',y='DI EPR intensity (A.U.)',kind='scatter')
    
    return EPR_data, EPR_int, EPR_int2, max_values, max_values_field
# desc_RAW = plottaaja_RAW()  # Pack all of the return values to a single tuple
# EPR_data, EPR_int, EPR_int2, max_values, max_values_field = plottaaja_RAW()

#%%
root = Tk()
# Give the user an instructions message
my_text = Label(root, text='Plottaa EPR dataa.')
my_text2 = Label(root, text=' Klikkaa "1. Analysoi BGR" jos haluat miinustaa blankon spectran tai \n"2. Analysoi raakadata" jos haluat nähdä tulokset sellaisenaan \nKlikkaa sen jälkeen "Näytä tulokset".')
my_text.pack()
my_text2.pack()
my_text.config(font=('times', 14, 'bold'))
my_text2.config(font=('times', 12, 'bold'))
# Create a button that will print the contents of the entry
button_BGR = Button(root, text='1. Analysoi BGR', command=plottaaja_BGR)
button_BGR.pack()
button_RAW = Button(root, text='2. Analysoi raakadata', command=plottaaja_RAW)
button_RAW.pack()
button2 = Button(root, text='Näytä tulokset', command=root.destroy)
button2.pack()
my_text3 = Label(root, text='Huom, jos haluat vähentää blankon spectrumin, on sen oltava kansion ensimmäinen tiedosto!!')
my_text3.pack()
my_text3.config(font=('times', 12, 'italic'))
root.geometry("900x250+150+150")
root.mainloop()
del button2, button_BGR, button_RAW, my_text, my_text2, my_text3, root

#%%
if value==1:
    bgr_spectrum, EPR_data, EPR_data_bgr,  EPR_int, EPR_int2, max_values, max_values_field = plottaaja_BGR()
else:
    EPR_data, EPR_int, EPR_int2,  max_values, max_values_field = plottaaja_RAW()
    
    
    