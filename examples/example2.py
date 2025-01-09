# -*- coding: utf-8 -*-
"""
example2: Managing Multiple Toggles with a Group

Author: Tchicdje Kouojip Joram Smith (DeltaGa)
Created: Wed Aug 7, 2024
"""

import customtkinter as ctk
from ctk_toggle_button import CTkToggleButton
from ctk_toggle_group import CTkToggleGroup

# Create the application window
app = ctk.CTk()
app.geometry("400x300")

# Define callback functions
def button_one_action():
    print("Button One is active!")

def button_two_action():
    print("Button Two is active!")

def button_three_action():
    print("Button Three is active!")

# Create toggle buttons
button_one = CTkToggleButton(app, text="Button 1", toggle_color="#34c759", command=button_one_action)
button_two = CTkToggleButton(app, text="Button 2", toggle_color="#ff9500", command=button_two_action)
button_three = CTkToggleButton(app, text="Button 3", toggle_color="#ff3b30", command=button_three_action)

# Create a toggle group
group = CTkToggleGroup([button_one, button_two, button_three])

# Layout the buttons
button_one.pack(pady=10)
button_two.pack(pady=10)
button_three.pack(pady=10)

app.mainloop()