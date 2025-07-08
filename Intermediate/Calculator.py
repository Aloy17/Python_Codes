import PySimpleGUI as sg
import random
def create_window(theme):
    sg.theme(theme)
    sg.set_options(font="Franklin 15", button_element_size=(6,3))

    layout = [
        [sg.Text("Output", key="-TEXT-",font="Franklin 25",justification="center",expand_x=True,pad=(10,20),right_click_menu=themes)],
        [sg.Button("Enter" ,key="-ENTER-",expand_x=True), sg.Button("CLR", key="-CLEAR-",expand_x=True)],
        [sg.Button(7, size=(6,3)), sg.Button(8, size=(6,3)), sg.Button(9, size=(6,3)), sg.Button("*", size=(6,3))],
        [sg.Button(4, size=(6,3)), sg.Button(5, size=(6,3)), sg.Button(6, size=(6,3)), sg.Button("/", size=(6,3))],
        [sg.Button(1, size=(6,3)), sg.Button(2, size=(6,3)), sg.Button(3, size=(6,3)), sg.Button("-", size=(6,3))],
        [sg.Button(0, expand_x=True), sg.Button(".", expand_x=True), sg.Button("+", size=(6,3))]
    ]

    return sg.Window("Calculator", layout)

themes = ["Menu",['Black', 'Black2', 'BlueMono', 'BluePurple', 'BrightColors','Random']]
window = create_window("Black")
current = []
operations = []

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event in themes[1]:
        window.close()
        window = create_window(event)
        window.read()

    if event in ["0","1","2","3","4","5","6","7","8","9","."]:
        current.append(event)
        num_string = ''.join(current)
        window["-TEXT-"].update(num_string)

    if event in ["+","*","-","/"]:
        operations.append(''.join(current))
        current = []
        operations.append(event)
        print(operations)
        window["-TEXT-"].update(" ")

    if event == "-ENTER-":
        operations.append(''.join(current))
        result = eval("".join(operations))
        window["-TEXT-"].update(result)
        operations = []

    if event == "-CLEAR-":
        operations = []
        current = []
        window["-TEXT-"].update(" ")


window.close()
