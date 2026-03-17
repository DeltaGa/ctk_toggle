# Optimization Guide — Object-Oriented Parent-Child GUI Systems

Performance principles for Python GUI libraries where a parent widget manages a collection of interactive child objects that receive events at display refresh rate (~60 Hz).

---

## 1. Know Your Hot Path

The **hot path** is any code that executes on every user interaction during a drag or resize — typically 60 times per second. Every microsecond wasted there is perceptible.

Identify the hot path by asking:
- Is this method called on every mouse-move event?
- Is this method called inside a loop over all managed objects?
- Is this method called by a tkinter binding that fires continuously?

If yes to any: treat it as hot-path. Everything else is cold.

**Profile before optimizing.** Use `cProfile` or `py-spy` to confirm where time is actually spent before making changes. Premature optimization is the root of maintenance debt.

```python
import cProfile
cProfile.run("root.mainloop()", sort="cumulative")
```

---

## 2. Attribute Access on the Hot Path

Python attribute lookup follows the MRO chain on every access. On a 60 Hz loop, redundant lookups accumulate.

### Cache repeated attribute access in local variables

```python
# Slow — three global lookups per call
def on_drag(self, event):
    self.canvas.move(self.rect, event.x - self.canvas.last_x, ...)
    self.canvas.move(self.resize_handle, ...)

# Fast — one lookup, local binding
def on_drag(self, event):
    canvas = self.canvas
    canvas.move(self.rect, event.x - canvas.last_x, ...)
    canvas.move(self.resize_handle, ...)
```

### Replace `hasattr` / `getattr` with cached booleans

`hasattr` and `getattr` are expensive on the hot path. Pre-compute capability flags once in `__init__`:

```python
# In __init__ (cold path — runs once)
self._has_dispatch: bool = hasattr(canvas, "_dispatch_rect")
self._has_move_attached: bool = hasattr(canvas, "move_attached_items")

# In on_drag (hot path — runs at 60 Hz)
if self._has_move_attached:
    canvas.move_attached_items(self, dx, dy)
```

This pattern is especially valuable when checking for optional parent capabilities — capabilities that may or may not exist depending on how the parent was configured.

---

## 3. Data Structure Choice for O(1) Lookups

### Membership testing: use `set`, not `list`

```python
# O(n) — scans all items
if rect in my_list:

# O(1) — hash lookup
if id(rect) in my_set:
```

### Reverse maps eliminate scanning

Maintain a reverse dict alongside the forward dict:

```python
self.objects: Dict[int, ChildObject] = {}       # item_id → object
self._rect_to_id: Dict[int, int] = {}           # id(object) → item_id
self._registered: set[int] = set()              # id(object) presence check
```

When you need `item_id` given an object, use `self._rect_to_id.get(id(obj))` — O(1) instead of scanning `self.objects.values()`.

**Keep reverse maps in sync.** Every insertion or deletion must update all related structures atomically.

---

## 4. The Python–C Boundary Cost (tkinter)

Every call to a tkinter method (`canvas.coords()`, `canvas.move()`, `canvas.itemconfig()`) crosses the Python–C boundary. This cost is fixed per call, regardless of payload size.

**Minimize round-trips:**
- Batch reads: collect all coordinates in one pass before beginning writes.
- Avoid calling `canvas.coords(item)` inside a tight loop when you already know the coordinates from a previous step.
- Use `canvas.move(item, dx, dy)` instead of `canvas.coords(item, x1, y1, x2, y2)` when only translating — `move` is implemented as a single C call while `coords` requires computing and passing four new values.

---

## 5. The Mutable Hash Key Pitfall

**Never use an object with a coordinate-based `__hash__` as a dict key when its coordinates will change during iteration.**

Python dicts store items by hash at insertion time. If the hash changes after insertion (because the underlying data changed), lookups will silently fail with `KeyError` even though the object is in the dict:

```python
# BROKEN — rect.__hash__ is coordinate-based
cache = {r: r.canvas.coords(r.rect) for r in rectangles}
for rect in rectangles:
    rc = cache[rect]           # KeyError after set_topleft_pos changes hash
    rect.set_topleft_pos(...)  # mutates hash
```

**Fix: use `id(obj)` as the key.** `id()` is the memory address — it never changes for a live object:

```python
# CORRECT
cache = {id(r): r.canvas.coords(r.rect) for r in rectangles}
for rect in rectangles:
    rc = cache[id(rect)]       # always stable
    rect.set_topleft_pos(...)
```

This applies to sets as well: never put a mutable-hash object in a set if its hash can change while it's a member.

The general rule: `__hash__` must return a stable value for the lifetime of the object, or the object must be declared unhashable (`__hash__ = None`).

---

## 6. Reconciliation vs. Destroy-and-Rebuild

When restoring state (undo/redo, reload), prefer **in-place reconciliation** over destroying all objects and rebuilding from scratch.

Destroy-and-rebuild:
- Invalidates every external reference to child objects.
- Forces all caller code to re-fetch references after every state change.
- Triggers unnecessary canvas item creation/destruction overhead.

Reconciliation (React-style diffing):
1. Update items that exist in both old and new state — in-place mutations preserve Python object identity.
2. Delete items present in current state but absent from the target state.
3. Create items present in the target state but absent from current state.

```python
current_ids = set(self.objects.keys())
target_ids = set(state.keys())

for item_id in current_ids & target_ids:
    self._update_in_place(self.objects[item_id], state[item_id])

for item_id in current_ids - target_ids:
    self._delete(item_id)

for item_id in target_ids - current_ids:
    self._create_from_state(item_id, state[item_id])
```

This is the same pattern used by game-engine entity managers and virtual DOM renderers — it is the correct pattern for any system where object identity matters to external holders.

---

## 7. Coordinate Arithmetic Optimization

Division is slower than multiplication. When you repeatedly divide by the same value (e.g. a zoom scale factor), pre-compute the inverse and multiply:

```python
# In a setup or property setter (cold)
self._zoom_inv = 1.0 / self.zoom_scale

# In coordinate conversion (hot path)
logical_x = canvas_x * self._zoom_inv   # multiply — faster than divide
```

For identity transforms (zoom == 1.0, no pan offset), add an early-return guard:

```python
def canvas_to_logical(self, x: float, y: float) -> tuple[float, float]:
    if self._offset_x == 0.0 and self._offset_y == 0.0 and self._zoom_inv == 1.0:
        return x, y
    return (x - self._offset_x) * self._zoom_inv, (y - self._offset_y) * self._zoom_inv
```

---

## 8. Lazy vs. Eager Initialization

| Pattern | When to use |
|---|---|
| Eager (in `__init__`) | Structures always needed; cheap to create; eliminates `getattr` guards |
| Lazy (on first use) | Structures rarely needed; expensive to create (e.g. image thumbnails) |

**Default to eager** for anything that guards a hot-path conditional. The tiny startup cost is paid once; the eliminated `getattr` overhead is paid every frame.

```python
# Eager — no runtime guards needed
self._thumbnail_cache: Dict[str, Image] = {}

# Lazy — only compute on first access
@property
def thumbnail(self) -> Image:
    if self._thumbnail is None:
        self._thumbnail = self._compute_thumbnail()
    return self._thumbnail
```

---

## 9. Selection Area Optimization

When hit-testing a rectangular selection region against a large set of objects, use the underlying engine's spatial query instead of looping in Python:

```python
# Slow — O(n) Python loop
selected = [r for r in all_rects if overlaps(r, selection_bbox)]

# Fast — O(log n) or hardware-accelerated via tkinter's spatial index
enclosed_ids = set(canvas.find_enclosed(x1, y1, x2, y2))
```

Convert the result to a `set` immediately if you need repeated membership tests.

---

## 10. Memory Layout and Object Count

- Minimize the number of canvas items per logical object. Each canvas item has overhead in tkinter's internal C structures.
- Delete canvas items explicitly when a logical object is deleted (`canvas.delete(item_id)`). Tkinter does not garbage-collect canvas items when the Python object goes out of scope.
- Use `canvas.delete("all")` only on full resets — never inside per-frame or per-object loops.

---

## 11. Profiling Checklist

Before declaring an optimization complete:

- [ ] Measured baseline FPS or latency with `cProfile` or `time.perf_counter`.
- [ ] Confirmed the optimization targets code that is actually on the measured hot path.
- [ ] Re-measured after the change to confirm improvement.
- [ ] No regression in correctness (all tests pass).
- [ ] No increase in code complexity that outweighs the gain.

**Do not optimize until you have measured. Do not stop optimizing until you have re-measured.**
