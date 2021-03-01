# Plot-EPR-spectra
Automates the plotting of EPR spectra, including normalisation and subtracting background spectrum. 

Version 3 plots any raw data read from a folder as 1st derivative, 1st and 2nd integrals. It also reads the maximum values of the 2nd integrals and plots those vs. the file number. Field values of the max 2nd integral are also saved for quick inspection

Version 4 then subtracts the BGR spectrum (assumed to be 1st in the folder) from the raw spectra and plots the result, takes again 1st and 2nd integrals and plots those also. Cumsums are determined and the maximum of 2nd integral is plotted, with corresponding field values also stored to variable explorer.

Version 5 adds a GUI to the version 4. A window opens up informing the user that it is time to plot EPR. First click initiates the script, but the pop-up needs to close for the results to be plotted, so I introduced a second button that prompts the user to click it to see the results.

Version 6 has a mean subtraction for all of the spectra, which handels the uneaven baselines that the Mangnettech spectrometer occasionally gives. The mean baselining is applied after plotting the raw data. This version is good in situations where manual baselining wans't done with Magnettech's software. Seems to quite robust for plotting manually baselined spectra also.

Version 7 uses a Messgebox functionality to ask if the user wants to get the EPR linewidths. Message box does not allow defining the position on the screen, so I used 'Toplevel' functionality to get it to the centre of the screen.

Version 8 plots the spectra as subplots to one figure, as I did with Matlab initially. I implemented this only in case the BGR subtracted data is required. I also did some formatting of the subplots etc., for example all of the y-axes are in scientific notation to save space on the page. 2nd plot has y-axis label also manually added
https://holypython.com/gui-with-python-checkboxes-and-radio-buttons-pysimplegui-part-ii/ is the website for the GUI

Version 9 tries to achieve version 8 but with PySimpleGUI. The imprrovement is that the file path is not hardcoded to the script, but can be selected with a FolderBrowse method of PySimpleGUI. Also the BGR spectrum can be selectred with a FileBrowse method if BGR spectrum is not the 1st spectrum in the folder. The BGR question dialog opens 2 times, and clicking for the 2nd time initiates the plottaaja_BGR function. I have no idea why this is, probably something to do with the functions return values??
--- TGo improve on this I think I should put the BGR selection window outside of the plottaaja_BGR function ---
