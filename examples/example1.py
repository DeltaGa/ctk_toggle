# -*- coding: utf-8 -*-
"""
example1: Simple Toggle Button

Author: Tchicdje Kouojip Joram Smith (DeltaGa)
Created: Wed Aug 7, 2024
"""

import customtkinter as ctk
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ctk_toggle.ctk_toggle_button import CTkToggleButton

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
    toggle_color="#68a6ff",
    command=on_toggle
)
toggle_button.pack(pady=50)

app.mainloop()