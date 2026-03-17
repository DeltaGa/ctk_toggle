"""
CTkToggleGroup: A group for managing toggle buttons.

Author: Tchicdje Kouojip Joram Smith (DeltaGa)
Created: Wed Aug 7, 2024
"""

from typing import List, Optional

from .ctk_toggle_button import CTkToggleButton


class CTkToggleGroup:
    def __init__(
        self,
        buttons: Optional[List[CTkToggleButton]] = None,
        disable_color: str = "lightgrey",
        allow_deactivate: bool = False,
    ):
        """
        Initialize a CTkToggleGroup.

        Args:
            buttons (Optional[List[CTkToggleButton]]): List of buttons in the group.
            disable_color (str): Color for disabled buttons.
            allow_deactivate (bool): When True, clicking the currently-active button
                will deactivate it (leaving no button active).  When False (default),
                the group behaves like a radio-button set where exactly one button is
                always active once a selection has been made.

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
        self.allow_deactivate = allow_deactivate
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

        Wraps the button's existing command so that the group's toggle logic
        fires first, then the original callback (e.g. ``on_sidebar_refresh``) fires
        immediately after.  This preserves all downstream side-effects while giving
        the group full control over activation/deactivation state.

        Args:
            button (CTkToggleButton): The button to configure.

        Raises:
            TypeError: If button is not an instance of CTkToggleButton.
        """
        if not isinstance(button, CTkToggleButton):
            raise TypeError("button must be an instance of CTkToggleButton.")

        button.toggle_group = self
        original_cmd = button.cget("command")  # preserve caller-supplied callback

        def wrapped(b=button, orig=original_cmd):
            self._handle_button_toggle(b)
            if orig:
                orig()

        button.configure(command=wrapped)

    def _handle_button_toggle(self, button: CTkToggleButton):
        """
        Handle toggle logic for a button.

        When ``allow_deactivate`` is True, clicking an already-active button
        deactivates it (no button remains active).  When False, clicking an
        already-active button is a no-op (radio-button semantics).

        Args:
            button (CTkToggleButton): The button that was toggled.

        Raises:
            TypeError: If button is not an instance of CTkToggleButton.
        """
        if not isinstance(button, CTkToggleButton):
            raise TypeError("button must be an instance of CTkToggleButton.")

        if button.get_toggle_state():
            if self.allow_deactivate:
                button.set_toggle_state(False)
            # else: already active and deactivation not allowed — leave as-is.
        else:
            self.set_active_button(button)
