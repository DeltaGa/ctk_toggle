# -*- coding: utf-8 -*-
"""
example3: Dynamically Adding and Removing Buttons in a Group

Author: Tchicdje Kouojip Joram Smith (DeltaGa)
Created: Wed Aug 7, 2024
"""

import customtkinter as ctk
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ctk_toggle.ctk_toggle_button import CTkToggleButton
from ctk_toggle.ctk_toggle_group import CTkToggleGroup

# Create the application window
app = ctk.CTk()
app.geometry("500x400")

# Create a toggle group
group = CTkToggleGroup()

# Add a button dynamically
def add_button():
    new_button = CTkToggleButton(
        master=app,
        text=f"Button {len(group.buttons) + 1}",
        toggle_color="#af52de",
        command=lambda: print(f"{new_button.cget('text')} is active!")
    )
    group.add_button(new_button)
    new_button.pack(pady=5)

# Remove the last button dynamically
def remove_button():
    if group.get_buttons():
        last_button = group.buttons[-1]
        last_button.destroy()
        group.remove_button(last_button)

# Add control buttons to manage dynamic changes
add_button_button = ctk.CTkButton(app, text="Add Button", command=add_button)
remove_button_button = ctk.CTkButton(app, text="Remove Button", command=remove_button)

add_button_button.pack(pady=20)
remove_button_button.pack(pady=10)

app.mainloop()
