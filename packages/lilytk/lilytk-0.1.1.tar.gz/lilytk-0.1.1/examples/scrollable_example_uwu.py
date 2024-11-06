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