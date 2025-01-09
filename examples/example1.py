# -*- coding: utf-8 -*-
"""
example1: Simple Toggle Button

Author: Tchicdje Kouojip Joram Smith (DeltaGa)
Created: Wed Aug 7, 2024
"""

import customtkinter as ctk
from ctk_toggle_button import CTkToggleButton

# Create a simple application window
app = ctk.CTk()
app.geometry("400x200")

# Define a callback function
def on_toggle():
    print("Button toggled!")

# Add a toggle button to the window
toggle_button = CTkToggleButton(
    master=app,
    text="Toggle Me",
    toggle_color="#58a6ff",
    command=on_toggle
)
toggle_button.pack(pady=50)

app.mainloop()