# lilytk
Tkinter components that I wanted to make :3

## Installing
This can be installed like any other PyPi package `pip install lilytk`

## Capabilities

### Highlightable
Adds functions that let the widget be highlighted and unhighlighted with configurable highlight color, highlight width, blink duration, blink delay.

### Scrollable
Automatically sets up platform independent mouse scroll events on the widget.

## Components
Here are all the components I have implemented and a brief description

### ScrollableFrame
Adds scrolling capabilities for the base `tk.Frame` widget. The frame is wrapped in a canvas with some scrollbars and other implementations I found make it so you have to add the child components to a member variable of the ScrollableFrame class. This ScrollableFrame handles the component hierarchy shizzwazz, so you can have an ergonomic experience.

```python
# examples/scrollable_example_uwu.py
import tkinter as tk
from lilytk import ScrollableFrame

app = tk.Tk()
app.title('scrollable example uwu')
app.geometry('1000x1000')

# You can specify tk.VERITCAL, tk.HORIZONTAL, or tk.BOTH to 
# configure which ways this frame can scroll
scrollable_frame = ScrollableFrame(app, orient=tk.VERTICAL)
scrollable_frame.pack(expand=True, fill=tk.BOTH)

for i in range(0, 200):
  row = tk.Frame(scrollable_frame)
  row.pack(expand=True, fill=tk.X)

  # Text can be in a scrollable list already with ttk.Treeview 
  # and tk.Listbox
  label = tk.Label(row, text=str(i), anchor=tk.E)
  label.pack(side=tk.LEFT, expand=True, fill=tk.X)

  # However ttk.Treeview and tk.Listbox don't allow you to add 
  # tk.Entry widgets or anything that isn't a text string
  entry = tk.Entry(row)
  entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)

app.mainloop()
```

You can notice, we have our list of components but we are only showing up to 26 out of 200. We also have a scrollbar on the right side.
![Scrollable Example uwu 1](images/scrollable_example_uwu_1.png?raw=true "Scrollable Example uwu 1")

The scrollbar smoothly moves the ScrollableFrame's view and every `tk.Entry` component we added still allows text entry as expected.
![Scrollable Example uwu 2](images/scrollable_example_uwu_2.png?raw=true "Scrollable Example uwu 2")

