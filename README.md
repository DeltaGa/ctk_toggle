<img src="https://raw.githubusercontent.com/DeltaGa/ctk_toggle/main/assets/thumbnail.jpg" alt="ctk_toggle thumbnail">

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.1.0+-green.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# CTk Toggle v1.0.4

## Toggle Buttons and Toggle Groups for CustomTkinter

**Version:** 1.0.4  
**Release Date:** July 27, 2026  
**Python:** 3.7+  
**CustomTkinter:** 5.1.0+

---

## Table of Contents

- [Overview](#overview)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Changelog](#changelog)
- [Credits](#credits)

---

## Overview

`ctk_toggle` adds toggle buttons and toggle groups to CustomTkinter. A `CTkToggleButton` extends the standard button with a persistent on/off state and a distinct toggled color. A `CTkToggleGroup` coordinates a set of buttons so that activating one deactivates the others, giving radio-style selection without leaving the CustomTkinter look and feel.

### Key Capabilities

- **Stateful toggle button** - A `CTkButton` subclass with a persistent boolean state and a toggled color
- **Coordinated groups** - Single-active selection across a set of buttons
- **Programmatic control** - Read and set state, enable and disable, and query the active button in code
- **Validated inputs** - Constructor and setter arguments are type- and value-checked, raising `TypeError` or `ValueError`
- **Drop-in styling** - Accepts the full `CTkButton` keyword set through `**kwargs`

---

## System Requirements

- **Python:** 3.7 or later
- **CustomTkinter:** 5.1.0 or later

---

## Installation

```bash
pip install ctk_toggle
```

---

## Usage

```python
import customtkinter as ctk
from ctk_toggle import CTkToggleButton, CTkToggleGroup

root = ctk.CTk()

group = CTkToggleGroup()
for label in ("Day", "Week", "Month"):
    button = CTkToggleButton(root, text=label, toggle_group=group)
    button.pack(padx=10, pady=5)

root.mainloop()
```

Activating any button in the group deactivates the others. Without a group, each button toggles independently.

---

## API Reference

### CTkToggleButton

A `customtkinter.CTkButton` subclass with toggle behavior.

**Constructor:** `CTkToggleButton(master=None, toggle_color="#c1e2c5", disable_color="lightgrey", toggle_group=None, **kwargs)`

| Method | Description |
|--------|-------------|
| `toggle(event=None)` | Flip the toggle state and update appearance |
| `set_toggle_state(state: bool)` | Set the state explicitly and refresh the color |
| `get_toggle_state() -> bool` | Return the current toggle state |
| `enable()` | Enable the button |
| `disable()` | Disable the button |

### CTkToggleGroup

Coordinates single-active selection across a set of buttons.

**Constructor:** `CTkToggleGroup(buttons=None, disable_color="lightgrey")`

| Method | Description |
|--------|-------------|
| `add_button(button)` | Add a button to the group |
| `remove_button(button)` | Remove a button from the group |
| `set_active_button(button)` | Activate one button and deactivate the rest |
| `deactivate_all()` | Deactivate every button in the group |
| `get_active_button() -> Optional[CTkToggleButton]` | Return the active button, or `None` |

Invalid arguments raise `TypeError` for wrong types and `ValueError` for invalid values.

---

## Examples

Runnable examples are in the [`examples/`](examples/) directory:

- `example1.py`
- `example2.py`
- `example3.py`

---

## Troubleshooting

### TypeError when constructing a group

**Cause:** `buttons` is not a list of `CTkToggleButton` instances  
**Solution:** Pass a list of `CTkToggleButton` objects, or omit the argument and add buttons with `add_button`.

### ValueError on a color argument

**Cause:** `toggle_color` or `disable_color` is not a string  
**Solution:** Provide colors as strings, for example `"#c1e2c5"` or `"lightgrey"`.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Code follows the conventions in [STYLE.md](STYLE.md) and [OPTIMIZATION.md](OPTIMIZATION.md).

---

## Changelog

### Version 1.0.4 (July 27, 2026)

- Toggle button and toggle group widgets for CustomTkinter.
- Group-coordinated single-active selection.
- Programmatic state control with validated constructor and setter arguments.

---

## Credits

### Author

**Tchicdje Kouojip Joram Smith (DeltaGa)**  
Email: dev.github.tkjoramsmith@outlook.com  
GitHub: [https://github.com/DeltaGa](https://github.com/DeltaGa)

### Acknowledgments

- [**CustomTkinter**](https://github.com/TomSchimansky/CustomTkinter): The widget foundation this package builds on.

---

## License

Released under the MIT License. See [LICENSE](LICENSE) for details.

---

© 2026 DeltaGa. All rights reserved.
