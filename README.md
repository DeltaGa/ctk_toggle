# ctk_toggle: CustomTkinter Toggle Buttons and Groups

## Overview
`ctk_toggle` is a lightweight Python package for creating toggle buttons and groups using CustomTkinter.

## Features
- Create toggle buttons with customizable states.
- Group buttons for coordinated toggling.
- Easily manage toggle states programmatically.

## Installation
Install via pip:
```bash
pip install ctk_toggle
```
## Usage
Import modules:
```python
from ctk_toggle import CTkToggleButton, CTkToggleGroup
```
Check the [examples/](https://github.com/DeltaGa/ctk_toggle/tree/main/examples) directory for usage examples.

## Contributing
See [CONTRIBUTING.md](https://github.com/DeltaGa/ctk_toggle/blob/main/CONTRIBUTING.md).

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/DeltaGa/ctk_toggle/blob/main/LICENSE) file for details.

## Documentation
**CTkToggleGroup**
```python
class CTkToggleGroup:
    """
    A group for managing toggle buttons.
    """

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

    def add_button(self, button: CTkToggleButton):
        """
        Add a button to the group.

        Args:
            button (CTkToggleButton): The button to add.
        
        Raises:
            TypeError: If button is not an instance of CTkToggleButton.
        """

    def remove_button(self, button: CTkToggleButton):
        """
        Remove a button from the group.

        Args:
            button (CTkToggleButton): The button to remove.
        
        Raises:
            TypeError: If button is not an instance of CTkToggleButton.
        """

    def set_active_button(self, button: CTkToggleButton):
        """
        Activate a specific button.

        Args:
            button (CTkToggleButton): The button to activate.
        
        Raises:
            TypeError: If button is not an instance of CTkToggleButton.
        """

    def deactivate_all(self):
        """
        Deactivate all buttons in the group.
        """

    def get_active_button(self) -> Optional[CTkToggleButton]:
        """
        Get the currently active button, if any.

        Returns:
            Optional[CTkToggleButton]: The currently active button, or None if no button is active.
        """

    def _update_buttons(self):
        """
        Update all buttons when one is disabled.
        """

    def _configure_button(self, button: CTkToggleButton):
        """
        Configure a button for the group.

        Args:
            button (CTkToggleButton): The button to configure.
        
        Raises:
            TypeError: If button is not an instance of CTkToggleButton.
        """

    def _handle_button_toggle(self, button: CTkToggleButton):
        """
        Handle toggle logic for a button.

        Args:
            button (CTkToggleButton): The button that was toggled.
        
        Raises:
            TypeError: If button is not an instance of CTkToggleButton.
        """
```

**CTkToggleButton**
```python
class CTkToggleButton(ctk.CTkButton):
    """
    A CustomTkinter button with toggle functionality.
    """

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

    def toggle(self, event=None):
        """
        Handle button toggle behavior.

        Args:
            event: The event that triggered the toggle.
        
        Raises:
            RuntimeError: If the button is in an invalid state.
        """

    def set_toggle_state(self, state: bool):
        """
        Set the toggle state and update appearance.

        Args:
            state (bool): The new toggle state.
        
        Raises:
            ValueError: If state is not a boolean.
        """

    def get_toggle_state(self) -> bool:
        """
        Get the current toggle state.

        Returns:
            bool: The current toggle state.
        
        Raises:
            RuntimeError: If the button is in an invalid state.
        """

    def enable(self):
        """
        Enable the button.
        
        Raises:
            RuntimeError: If the button is already enabled.
        """

    def disable(self):
        """
        Disable the button.
        
        Raises:
            RuntimeError: If the button is already disabled.
        """

    def _update_fg_color(self):
        """
        Update the foreground color based on the toggle state.
        """
```

## Credits

### Author
- **Tchicdje Kouojip Joram Smith (DeltaGa)**  
  Creator and developer of the CTkToggleButton and CTkToggleGroup classes.  
  
  Email: dev.github.tkjoramsmith@outlook.com
  GitHub: [https://github.com/DeltaGa](https://github.com/DeltaGa)

### Acknowledgments
- **CustomTkinter**: The CustomTkinter library provided the foundation for building modern and customizable widgets in this project.  
  GitHub: [https://github.com/TomSchimansky/CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)

- **Open Source Community**: Inspiration and guidance from various open-source contributions and community members.

- **Python Community**: For creating an ever-evolving ecosystem that empowers developers worldwide.

### Contributions from Large Language Models

This project was developed with support and inspiration from state-of-the-art Large Language Models (LLMs), including but not limited to open/free-to-use models such as:

- OpenAI's GPT series.
- Open-source language models provided by communities like Hugging Face and EleutherAI.

These models were instrumental in providing guidance, code refactoring suggestions, and improving the overall quality of the project documentation. Special thanks to the developers, researchers, and communities who have contributed to the field of natural language processing and made these models publicly available for everyone.

The integration of such tools demonstrates how artificial intelligence can augment human creativity and productivity in software development and beyond.
