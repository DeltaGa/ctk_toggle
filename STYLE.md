# Python Style Guide — Complex GUI Libraries

Expert-level coding style conventions for Python GUI libraries built on tkinter or CustomTkinter. These rules apply to any project that couples a stateful parent widget with managed child objects.

---

## 1. Code Organization

### Module structure

```
src/
  your_package/
    __init__.py        # Public API only — re-exports, version, __all__
    parent_widget.py   # Canvas / container class
    child_object.py    # Managed interactive objects
    utils.py           # Pure helpers with no widget dependencies
```

- `__init__.py` must **never** contain logic. It exports symbols and declares `__version__`, `__all__`.
- One class per file unless the classes are tightly coupled and always imported together.
- Keep platform-specific concerns (DPI, OS bindings) isolated in clearly named sections.

### Import order

Follow PEP 8 with explicit grouping and one blank line between groups:

```python
# 1. Standard library
import sys
from pathlib import Path
from typing import Dict, List, Optional

# 2. Third-party
import customtkinter as ctk
from PIL import Image

# 3. Local / intra-package (always relative inside src/)
from .child_object import ChildObject
```

Inside `src/`, always use **relative imports** (`from . import ...`, `from .module import Class`). This guarantees the development source is used regardless of what is installed in the environment.

In standalone scripts (examples, tools), insert `src/` at `sys.path[0]` before any project import:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
```

---

## 2. Typing

- Use full type annotations on every public method signature. Return type is mandatory.
- Use `Optional[X]` / `X | None` (Python 3.10+) consistently; never leave ambiguity.
- Prefer concrete types (`Dict[int, Rect]`) over vague generics (`dict`).
- Use `TYPE_CHECKING` guard to avoid circular imports from type-only dependencies:

```python
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .parent_widget import ParentWidget
```

- Avoid `Any` except at true system boundaries (tkinter event data, external JSON blobs). Document every `# type: ignore` with a one-line reason.

---

## 3. Naming Conventions

| Thing | Convention | Example |
|---|---|---|
| Public method | `snake_case` | `get_topleft_pos()` |
| Private method | `_snake_case` | `_builtin_on_drag()` |
| Protected (override-intended) | `_snake_case` with docstring note | `_on_press()` |
| Instance attribute | `snake_case` | `self.canvas` |
| Private attribute | `_snake_case` | `self._attached_items` |
| Class constant | `UPPER_SNAKE` | `MAX_HISTORY = 50` |
| Boolean attributes | `is_`, `has_`, `enable_`, `_has_` prefix | `self._has_dispatch` |
| Callback attributes | `on_` prefix | `on_drag_callback` |

**Avoid abbreviations** unless they are universally understood in the domain (`dpi`, `px`, `mm`, `rect`, `idx`).

---

## 4. Class Design

### Separation of concerns

A widget class should own **exactly one responsibility**. If a class both renders and manages business logic, split them.

- Parent widget: layout, event routing, lifetime management of children, history.
- Child object: own state, own canvas items, own event handlers. Delegates upward only through well-defined hooks.

### `__init__` discipline

- List every instance attribute at the top of `__init__`, even if set to `None`. Readers and type-checkers depend on this.
- Unconditionally initialize attributes that guard optional features. Use sensible defaults instead of setting them only inside `if feature_enabled:` branches — this eliminates defensive `getattr` calls at runtime.
- Initialize expensive structures (dicts, sets) once; never inside event handlers.

```python
# Good
self._reverse_map: Dict[int, ChildObject] = {}
self._registered: set[int] = set()

# Bad — creates attribute only when feature is enabled, forces getattr elsewhere
if self.enable_feature:
    self._reverse_map = {}
```

### Properties vs. plain attributes

Use `@property` only when:
- A value must be computed or validated on access.
- You want to protect writes with a setter.

Do **not** use `@property` purely for style. Plain attributes are faster and clearer for simple stored state.

### Magic methods

Implement magic methods to express mathematical and containment semantics naturally — but only when the semantics are unambiguous and self-documenting. Document the return type and side-effect behavior clearly.

- `__hash__` and `__eq__` must be **consistent and immutable**. If an object's hash must reflect coordinates, either freeze the object after creation, or — better — **do not use the object as a dict key** when its coordinates are mutable. Use `id(obj)` as a dict key instead.
- If `__eq__` is defined, `__hash__` must also be defined (or explicitly set to `None` to make the object unhashable).

---

## 5. Event-Driven Patterns

### Callback registration

Prefer explicit registration over monkey-patching or subclassing for user-supplied callbacks:

```python
canvas.on_select_callback = my_handler   # stored reference
```

Guard all user callbacks against exceptions — a buggy callback must not crash the widget:

```python
if self.on_drag_callback:
    try:
        self.on_drag_callback(self)
    except Exception:
        pass  # or log; never propagate into tkinter's event loop
```

### Binding hygiene

- Use `canvas.tag_bind(item_id, "<Event>", handler)` rather than `canvas.bind(...)` for item-level events.
- Store the result of `canvas.bind(...)` if you need to unbind later. Do not rely on implicit rebinding to replace old bindings.
- Never bind the same event multiple times on the same widget/item without first unbinding.

### State flags

Use narrow-scoped boolean flags for transient state (`_dragging`, `_resizing`, `_restoring_state`). Set them to `False` immediately after the operation completes — never leave flags set between event cycles.

---

## 6. Error Handling

- Validate inputs at **public API boundaries only**. Trust internal methods.
- Raise `ValueError` for invalid argument values, `TypeError` for wrong types. Never raise `Exception` directly.
- Use guard clauses (early `return` or `raise`) to eliminate nesting:

```python
# Good
def set_size(self, size: List[float]) -> None:
    if len(size) != 2:
        raise ValueError("size must be [width, height]")
    ...

# Bad
def set_size(self, size):
    if len(size) == 2:
        ...
        if size[0] > 0:
            ...
```

- Never catch broad exceptions silently in library code. If you suppress an exception (e.g. for tkinter widget-already-destroyed scenarios), add a comment explaining why.

---

## 7. Documentation

Use Google-style docstrings for all public classes and methods:

```python
def align(cls, rectangles: List["Rect"], mode: str = "top") -> None:
    """Align a list of rectangles along a common axis.

    Args:
        rectangles: The objects to align. Must be on the same canvas.
        mode: Alignment mode. One of ``"top"``, ``"bottom"``, ``"middle"``,
            ``"start"``, ``"end"``, ``"center"``.

    Raises:
        ValueError: If fewer than 2 rectangles are provided or mode is unknown.
    """
```

- First line is a one-sentence imperative summary.
- `Args:` and `Returns:` are required for non-trivial signatures.
- `Raises:` documents every exception the caller might need to handle.
- Private methods need only a brief inline comment if the logic is non-obvious.

---

## 8. Code Formatting

- Line length: **100 characters** (matches `black` + `ruff` config).
- Use `black` for formatting and `ruff` for linting. Do not argue with the formatter.
- Trailing commas in multi-line function signatures and collections — they make diffs cleaner.
- Use f-strings for all string interpolation. Avoid `%` and `.format()`.
- Never use mutable default arguments (`def f(lst=[])`). Use `None` and assign inside the body.

---

## 9. Testing

- Tests live in `tests/`. The `conftest.py` must insert `src/` at `sys.path[0]` so tests always run against the local source, never against an installed package.
- Name tests `test_<behavior>`, not `test_<implementation_detail>`.
- Fixtures should be function-scoped for GUI widget tests — shared state between tests causes false positives.
- Test public behavior, not private implementation. Refactoring internals must not break tests.
- For GUI tests that require a display, use `pytest.skip` gracefully when Tkinter is not available.

---

## 10. Version and Changelog

- Version follows `MAJOR.MINOR.PATCH` (SemVer). Breaking API changes bump `MAJOR`.
- Every released version gets a `CHANGELOG.md` entry grouped as: **Added**, **Changed**, **Fixed**, **Performance**, **Breaking**.
- Version string lives in `__init__.py` and `pyproject.toml`. Keep them in sync.
