# -*- coding: utf-8 -*-
"""
CTkToggleGroup: A group for managing toggle buttons.

Author: Tchicdje Kouojip Joram Smith (DeltaGa)
Created: Wed Aug 7, 2024
"""

from typing import List, Optional
from .ctk_toggle_button import CTkToggleButton


class CTkToggleGroup:
    def __init__(self, buttons: Optional[List[CTkToggleButton]] = None, disable_color: str = "lightgrey"):
        """
        Initialize a CTkToggleGroup.

        Args:
            buttons (Optional[List[CTkToggleButton]]): List of buttons in the group.
            disable_color (str): Color for disabled buttons.
        
        Raises:
            TypeError: If buttons is not a list of CTkToggleButton instances or None.
            ValueError: If disable_color is not a string.
        """
        if buttons is not None and not all(isinstance(button, CTkToggleButton) for button in buttons):
            raise TypeError("buttons must be a list of CTkToggleButton instances or None.")
        if not isinstance(disable_color, str):
            raise ValueError("disable_color must be a string.")

        self.buttons = buttons or []
        self.disable_color = disable_color
        for button in self.buttons:
            self._configure_button(button)

    def add_button(self, button: CTkToggleButton):
        """
        Add a button to the group.

        Args:
            button (CTkToggleButton): The button to add.
        
        Raises:
            TypeError: If button is not an instance of CTkToggleButton.
        """
        if not isinstance(button, CTkToggleButton):
            raise TypeError("button must be an instance of CTkToggleButton.")
        
        self._configure_button(button)
        self.buttons.append(button)

    def remove_button(self, button: CTkToggleButton):
        """
        Remove a button from the group.

        Args:
            button (CTkToggleButton): The button to remove.
        
        Raises:
            TypeError: If button is not an instance of CTkToggleButton.
        """
        if not isinstance(button, CTkToggleButton):
            raise TypeError("button must be an instance of CTkToggleButton.")
        
        if button in self.buttons:
            button.configure(command=None)
            self.buttons.remove(button)

    def set_active_button(self, button: CTkToggleButton):
        """
        Activate a specific button.

        Args:
            button (CTkToggleButton): The button to activate.
        
        Raises:
            TypeError: If button is not an instance of CTkToggleButton.
        """
        if not isinstance(button, CTkToggleButton):
            raise TypeError("button must be an instance of CTkToggleButton.")
        
        self.deactivate_all()
        button.set_toggle_state(True)

    def deactivate_all(self):
        """
        Deactivate all buttons in the group.
        """
        for button in self.buttons:
            button.set_toggle_state(False)

    def get_active_button(self) -> Optional[CTkToggleButton]:
        """
        Get the currently active button, if any.

        Returns:
            Optional[CTkToggleButton]: The currently active button, or None if no button is active.
        """
        return next((button for button in self.buttons if button.get_toggle_state()), None)

    def _update_buttons(self):
        """
        Update all buttons when one is disabled.
        """
        for button in self.buttons:
            if button._state == "disabled":
                button.set_toggle_state(False)
                button.configure(fg_color=self.disable_color)

    def _configure_button(self, button: CTkToggleButton):
        """
        Configure a button for the group.

        Args:
            button (CTkToggleButton): The button to configure.
        
        Raises:
            TypeError: If button is not an instance of CTkToggleButton.
        """
        if not isinstance(button, CTkToggleButton):
            raise TypeError("button must be an instance of CTkToggleButton.")
        
        button.toggle_group = self
        button.configure(command=lambda b=button: self._handle_button_toggle(b))

    def _handle_button_toggle(self, button: CTkToggleButton):
        """
        Handle toggle logic for a button.

        Args:
            button (CTkToggleButton): The button that was toggled.
        
        Raises:
            TypeError: If button is not an instance of CTkToggleButton.
        """
        if not isinstance(button, CTkToggleButton):
            raise TypeError("button must be an instance of CTkToggleButton.")
        
        if not button.get_toggle_state():
            self.set_active_button(button)

