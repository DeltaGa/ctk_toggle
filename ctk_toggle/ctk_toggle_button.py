# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 09:58:40 2024

@author: Tchicdje Kouojip Joram Smith, DeltaGa
"""

import customtkinter as ctk
from PIL import Image as PILImage
from typing import Optional

class CTkToggleButton(ctk.CTkButton):
    def __init__(self, master=None, toggle_color="#c1e2c5", disable_color="lightgrey", toggle_group=None, **kwargs):
        super().__init__(master, **kwargs)
        self.toggle_state = False
        self.toggle_color = toggle_color
        self.disable_color = disable_color
        self.default_fg_color = self.cget("fg_color")
        self.toggle_group = toggle_group
        self._state = 'normal'
        self.bind("<Button-1>", self.toggle)
        self.command = kwargs['command']

    def toggle(self, event=None):
        if self._state == 'normal':
            if self.toggle_group:
                self.toggle_group.set_active_button(self)
            else:
                self.toggle_state = not self.toggle_state
                new_color = self.toggle_color if self.toggle_state else self.default_fg_color
                self.configure(fg_color=new_color)

    def set_toggle_state(self, state: bool):
        self.toggle_state = state
        if self._state == 'normal':
            new_color = self.toggle_color if self.toggle_state else self.default_fg_color
            self.configure(fg_color=new_color)

    def get_toggle_state(self) -> bool:
        return self.toggle_state

    def enable(self):
        self._state = 'normal'
        if not self.toggle_state:
            self.configure(fg_color=self.default_fg_color)

    def disable(self):
        self._state = 'disabled'
        self.set_toggle_state(False)
        self.configure(fg_color=self.disable_color)
        if self.toggle_group:
            self.toggle_group._update_buttons()