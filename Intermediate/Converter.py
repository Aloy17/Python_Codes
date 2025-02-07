import PySimpleGUI as sg
layout=[
    [sg.Text("Convert weight or distance!"), sg.Spin(["km","kg"],key="s1")],
    [sg.Text("Enter Below")],
    [sg.Input(key="i1")],
    [sg.Button("Convert",key="b1")],
    [sg.Text(enable_events=True,key="t2")]
]

window = sg.Window("Converter",layout)

while True:
    event , values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == "b1":
        unit = values["s1"]
        if unit == "km":
            num = float(values["i1"])
            answer = num * 1000
            window["t2"].update(f"{answer} metres")
        elif unit == "kg":
            num = float(values["i1"])
            answer = num * 1000
            window["t2"].update(f"{answer} grams")
window.close()
