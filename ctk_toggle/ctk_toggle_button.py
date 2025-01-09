# -*- coding: utf-8 -*-
"""
CTkToggleButton: A CustomTkinter button with toggle functionality.

Author: Tchicdje Kouojip Joram Smith (DeltaGa)
Created: Wed Aug 7, 2024
"""

import customtkinter as ctk
from typing import Optional, Any


class CTkToggleButton(ctk.CTkButton):
    def __init__(
        self,
        master=None,
        toggle_color: str = "#c1e2c5",
        disable_color: str = "lightgrey",
        toggle_group: Optional[Any] = None,
        **kwargs,
    ):
        """
        Initialize a CTkToggleButton with toggle functionality.

        Args:
            master: Parent widget.
            toggle_color (str): Color when toggled.
            disable_color (str): Color when disabled.
            toggle_group (Optional[CTkToggleGroup]): Group to coordinate toggling.
            **kwargs: Additional keyword arguments for CTkButton.
        
        Raises:
            ValueError: If toggle_color or disable_color is not a string.
            TypeError: If toggle_group is not an instance of CTkToggleGroup or None.
        """
        from .ctk_toggle_group import CTkToggleGroup
        
        if not isinstance(toggle_color, str):
            raise ValueError("toggle_color must be a string.")
        if not isinstance(disable_color, str):
            raise ValueError("disable_color must be a string.")
        if toggle_group is not None and not isinstance(toggle_group, CTkToggleGroup):
            raise TypeError("toggle_group must be an instance of CTkToggleGroup or None.")
        
        super().__init__(master, **kwargs)
        self.toggle_state = False
        self.toggle_color = toggle_color
        self.disable_color = disable_color
        self.default_fg_color = self.cget("fg_color")
        self.toggle_group = toggle_group
        self._state = "normal"
        self.bind("<Button-1>", self.toggle)

    def toggle(self, event=None):
        """
        Handle button toggle behavior.

        Args:
            event: The event that triggered the toggle.
        
        Raises:
            RuntimeError: If the button is in an invalid state.
        """
        if self._state == "normal":
            if self.toggle_group:
                self.toggle_group.set_active_button(self)
            else:
                self.toggle_state = not self.toggle_state
                self._update_fg_color()
        else:
            raise RuntimeError("Cannot toggle button when it is disabled.")

    def set_toggle_state(self, state: bool):
        """
        Set the toggle state and update appearance.

        Args:
            state (bool): The new toggle state.
        
        Raises:
            ValueError: If state is not a boolean.
        """
        if not isinstance(state, bool):
            raise ValueError("state must be a boolean.")
        
        self.toggle_state = state
        self._update_fg_color()

    def get_toggle_state(self) -> bool:
        """
        Get the current toggle state.

        Returns:
            bool: The current toggle state.
        
        Raises:
            RuntimeError: If the button is in an invalid state.
        """
        if self._state != "normal":
            raise RuntimeError("Cannot get toggle state when button is disabled.")
        
        return self.toggle_state

    def enable(self):
        """
        Enable the button.
        
        Raises:
            RuntimeError: If the button is already enabled.
        """
        if self._state == "normal":
            raise RuntimeError("Button is already enabled.")
        
        self._state = "normal"
        if not self.toggle_state:
            self.configure(fg_color=self.default_fg_color)

    def disable(self):
        """
        Disable the button.
        
        Raises:
            RuntimeError: If the button is already disabled.
        """
        if self._state == "disabled":
            raise RuntimeError("Button is already disabled.")
        
        self._state = "disabled"
        self.set_toggle_state(False)
        self.configure(fg_color=self.disable_color)
        if self.toggle_group:
            self.toggle_group._update_buttons()

    def _update_fg_color(self):
        """
        Update the foreground color based on the toggle state.
        """
        new_color = self.toggle_color if self.toggle_state else self.default_fg_color
        self.configure(fg_color=new_color)

