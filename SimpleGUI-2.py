#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 20:50:04 2021

@author: mika
"""

# CHECK BOX - PySimpleGUI

import PySimpleGUI as sg

layout = [[sg.T("")],
          [sg.T("  "), sg.Button('Hello World',size=(20,4))],
          [sg.T("")],
          [sg.T("       "), sg.Checkbox('My Checkbox', default=False, key="-IN-")]]

window = sg.Window('Push My Buttons', layout, size=(300,200))

while True:
    event, values = window.read() # The keys in layout are stored in values
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    elif values["-IN-"] == True:        # look up checkbox' value with this call, is the box 1 or 0
        print("Hello World!")
    
window.close()