# Plot-EPR-spectra
Automates the plotting of EPR spectra, including normalisation and subtracting background spectrum. 

Version 3 plots any raw data read from a folder as 1st derivative, 1st and 2nd integrals. It also reads the maximum values of the 2nd integrals and plots those vs. the file number. Field values of the max 2nd integral are also saved for quick inspection

Version 4 then subtracts the BGR spectrum (assumed to be 1st in the folder) from the raw spectra and plots the result, takes again 1st and 2nd integrals and plots those also. Cumsums are determined and the maximum of 2nd integral is plotted, with corresponding field values also stored to variable explorer.

Version 5 adds a GUI to the version 4. A window opens up informing the user that it is time to plot EPR. First click initiates the script, but the pop-up needs to close for the results to be plotted, so I introduced a second button that prompts the user to click it to see the results.

Version 6 has a mean subtraction for all of the spectra, which handels the uneaven baselines that the Mangnettech spectrometer occasionally gives. The mean baselining is applied after plotting the raw data.
