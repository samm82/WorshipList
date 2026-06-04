## @file   GUI_Helpers.py
#  @brief  Implements smaller GUI elements used in GUI.py and Helpers.py.
#  @author Samuel Crawford
#  @date   6/4/2026

import PySimpleGUI as sg


## @brief         Defines a warning popup that provides the option to ignore.
#  @param[in] s   The warning string to be printed in dialogue box.
#  @param[in] all A Boolean representing if an "Ignore All" button should be created.
#  @return        The name of the button pressed.
def popupWarn(s: str, all: bool = True):
    buttons = ["Go Back", "Ignore"]
    if all:
        buttons.append("Ignore All")

    dialogue = [[sg.Text(s)], buttonRow(buttons, True)]

    window = sg.Window("WorshipList").Layout(dialogue)
    return window.Read()[0]


## @brief       Defines a text input popup.
#  @param[in] s The prompt string to be printed in dialogue box.
#  @return      The name of the button pressed and the text entered.
def popupText(s):
    dialogue = [
        [sg.Text(s)],
        [sg.InputText("")],
        buttonRow(["OK", "Cancel"], True)
    ]

    window = sg.Window("WorshipList").Layout(dialogue)
    button, values = window.Read()
    return button, values[0]


## @brief       Defines an error popup that signifies incorrect input.
#  @param[in] s The error string to be printed in dialogue box.
def popupError(s: str):
    sg.Popup(s, title="Error")


## @brief           Creates a row of buttons.
#  @param[in] names A list of names for buttons and a Boolean for if they should close on press.
#  @param[in] close A Boolean representing if the window should be closed on a button press.
#  @return          A list of buttons.
def buttonRow(names: list[str], close: bool = False):
    return [sg.CloseButton(n) if close else sg.Button(n) for n in names]
