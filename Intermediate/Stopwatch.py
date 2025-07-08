import PySimpleGUI as sg
import time

layout = [[sg.Text(now.tm_hour)]]

window = sg.Window("Time",layout)

while True:
    event,values = window.read()

    if event == sg.WIN_CLOSED:
        break

window.close()
