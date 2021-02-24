#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 19:36:31 2021

@author: mika
"""

# BUTTON -  PySimpleGUI

import PySimpleGUI as sg

sg.theme('DarkTeal2')

layout = [[sg.T("")], 
          [sg.Text("Primary Button: "), sg.Button('Hello World', size=(20,4))],
          [sg.T("")],
          [sg.Button('Taas Poika Saunoo', size=(30,4)), sg.Button('Anopilla Kyydissa', size=(25,4))]] # Brackets add rows, kind of padding

window = sg.Window('Push my Buttons', layout, size=(550,300))

while True:
    
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Hello World':
        print("Hello World!")
    elif event == 'Taas Poika Saunoo':
        print('Se tuppaa joikaamaan!!')
    elif event == 'Anopilla Kyydissa':
        print('Eli hyvin menee!!')
