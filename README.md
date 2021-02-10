# Plot-EPR-spectra
Automates the plotting of EPR spectra, including normalisation and subtracting background spectrum. 

Version 3 plots any raw data read from a folder as 1st derivative, 1st and 2nd integrals. It also reads the maximum values of the 2nd integrals and plots those vs. the file number. Field values of the max 2nd integral are also saved for quick inspection

Version 4 then subtracts the BGR spectrum (assumed to be 1st in the folder) from the raw spectra and plots the result, takes again 1st and 2nd integrals and plots those also. Cumsums are determined and the maximum of 2nd integral is plotted, with corresponding field values also stored to variable explorer.

Version 5 adds a GUI to the vaesion 4
