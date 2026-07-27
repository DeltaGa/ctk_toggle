"""
CTkToggleButton: A CustomTkinter button with toggle functionality.

Author: Tchicdje Kouojip Joram Smith (DeltaGa)
Created: Wed Aug 7, 2024
"""

from typing import Any, Optional

import customtkinter as ctk


class CTkToggleButton(ctk.CTkButton):
    def __init__(
        self,
        master=None,
        toggle_color: str = "#c1e2c5",
        disable_color: str = "lightgrey",
        toggle_group: Optional[Any] = None,
        skip_runtime_errors: bool = True,
        **kwargs,
    ):
        """
        Initialize a CTkToggleButton with toggle functionality.

        Args:
            master: Parent widget.
            toggle_color (str): Color when toggled.
            disable_color (str): Color when disabled.
            toggle_group (Optional[CTkToggleGroup]): Group to coordinate toggling.
            skip_runtime_errors (bool): If True, suppress RuntimeErrors raised by state
                guard checks in toggle(), get_toggle_state(), enable(), and disable().
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
        self.skip_runtime_errors = skip_runtime_errors
        self.bind("<Button-1>", self.toggle)

    def toggle(self, event=None):
        """
        Handle button toggle behavior.

        When the button belongs to a ``CTkToggleGroup``, all state management
        is delegated to the group's command wrapper (fired on ``<ButtonRelease-1>``).
        This binding (``<Button-1>``) must therefore do nothing in that case -
        acting here would unconditionally activate the button and prevent the
        group from implementing deactivate-on-reclick logic.

        Args:
            event: The event that triggered the toggle.

        Raises:
            RuntimeError: If the button is in an invalid state.
        """
        if self._state == "normal":
            if not self.toggle_group:
                # Standalone button: flip state directly.
                self.toggle_state = not self.toggle_state
                self._update_fg_color()
            # In-group: let the group's command wrapper handle everything.
        else:
            if not self.skip_runtime_errors:
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
        if self._state != "normal" and not self.skip_runtime_errors:
            raise RuntimeError("Cannot get toggle state when button is disabled.")

        return self.toggle_state

    def enable(self):
        """
        Enable the button.

        Raises:
            RuntimeError: If the button is already enabled.
        """
        if self._state == "normal":
            if not self.skip_runtime_errors:
                raise RuntimeError("Button is already enabled.")
            return

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
            if not self.skip_runtime_errors:
                raise RuntimeError("Button is already disabled.")
            return

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
