# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 15:30:08 2024

@author: Tchicdje Kouojip Joram Smith, DeltaGa
"""

import sys
import os
from pathlib import Path
import customtkinter as ctk
from typing import Optional

from ctk_toggle_button import CTkToggleButton

class ToggleGroup:
    def __init__(self, buttons: Optional[list] = None, disable_color="lightgrey"):
        self.buttons = buttons if buttons else []
        self.button_commands = [button.command for button in self.buttons]
        self.disable_color = disable_color
        for button in self.buttons:
            button.toggle_group = self
            button.configure(command=lambda b=button: self._toggle_button(b))

    def add_button(self, button: CTkToggleButton):
        button.toggle_group = self
        self.button_commands.append(button.command)
        button.configure(command=lambda b=button: self._toggle_button(b))
        self.buttons.append(button)

    def remove_button(self, button: CTkToggleButton):
        if button in self.buttons:
            button.configure(command=self.button_commands[self.buttons.index(button)])
            self.buttons.remove(button)
            self.button_commands.remove(button.command)
            button.toggle_group = None
            button.configure(command=None)

    def _toggle_button(self, button: CTkToggleButton):
        if button.get_toggle_state():
            self.deactivate_all()
        else:
            self.deactivate_all()
            button.set_toggle_state(True)
            self.button_commands[self.buttons.index(button)]()

    def get_active_button(self) -> Optional[CTkToggleButton]:
        for button in self.buttons:
            if button.get_toggle_state():
                return button
        return None

    def set_active_button(self, button: CTkToggleButton):
        self.deactivate_all()
        button.set_toggle_state(True)

    def deactivate_all(self):
        for button in self.buttons:
            button.set_toggle_state(False)

    def get_button_state(self, button: CTkToggleButton) -> bool:
        return button.get_toggle_state()

    def get_buttons(self) -> list:
        return self.buttons

    def _update_buttons(self):
        for button in self.buttons:
            if button._state == 'disabled':
                button.set_toggle_state(False)
                button.configure(fg_color=self.disable_color)