'''
Copyright (C) 2024-2024 Lilith Cybi - All Rights Reserved.
You may use, distribute and modify this code under the
terms of the MIT license.

You should have received a copy of the MIT license with
this file. If not, please write to: lilith.cybi@syrency.com, 
or visit: https://github.com/jmeaster30/lilytk/LICENSE
'''

import tkinter as tk
from tkinter import ttk
from typing import Optional

from lilytk.src.capabilities.scrollable import Scrollable, MouseScrollEvent
from lilytk.src.typing import Orientation


class ScrollableFrame(tk.Frame, Scrollable):
  def __init__(self, root: Optional[tk.Misc], orient: Orientation = tk.VERTICAL, *args, **kwargs):
    self.full_container = tk.Frame(root, *args, *kwargs)
    self.canvas = tk.Canvas(self.full_container)

    self.full_container.rowconfigure(0, weight=1)
    self.full_container.columnconfigure(0, weight=1)
    
    self.canvas.grid(row=0, column=0, sticky=tk.NSEW)

    match orient:
      case tk.HORIZONTAL:
        self.y_scrollbar = None
        self.x_scrollbar = ttk.Scrollbar(self.full_container, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.x_scrollbar.grid(row=1, column=0, sticky=tk.EW)
        self.canvas.configure(xscrollcommand=self.x_scrollbar.set)
      case tk.VERTICAL:
        self.x_scrollbar = None
        self.y_scrollbar = ttk.Scrollbar(self.full_container, orient=tk.VERTICAL, command=self.canvas.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.canvas.configure(yscrollcommand=self.y_scrollbar.set)
      case tk.BOTH:
        self.x_scrollbar = ttk.Scrollbar(self.full_container, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.x_scrollbar.grid(row=1, column=0, sticky=tk.EW)
        self.y_scrollbar = ttk.Scrollbar(self.full_container, orient=tk.VERTICAL, command=self.canvas.yview)
        self.y_scrollbar.grid(row=0, column=1, sticky=tk.NS)
        self.canvas.configure(xscrollcommand=self.x_scrollbar.set, yscrollcommand=self.y_scrollbar.set)
      case _:
        raise ValueError(f"Bad value '{orient}' for orient argument of ScrollableFrame")

    # Frame has to be initialized first
    tk.Frame.__init__(self, self.canvas)
    Scrollable.__init__(self, target=self.full_container, orient=orient)

    # set up function overrides for geometry managers
    geometry_manager_method_list = [func for func in dir(self.__class__) if callable(getattr(self, func)) and (func.startswith("pack") or func.startswith("grid") or func.startswith("place"))]
    for method in geometry_manager_method_list:
      setattr(self, f'internal_{method}', getattr(super(tk.Frame, self), method))
      setattr(self, method, getattr(self.full_container, method))

    self.internal_pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
    self.inner_frame_id = self.canvas.create_window((0,0), window=self, anchor=tk.NW)

    def _configure_interior(event):
      self.canvas.config(scrollregion=self.canvas.bbox("all"))
      if self.winfo_reqwidth() != self.canvas.winfo_width():
        self.canvas.config(width=self.winfo_reqwidth())
    self.bind('<Configure>', _configure_interior)

    def _configure_canvas(event):
      if self.winfo_reqwidth() != self.canvas.winfo_width():
        self.canvas.itemconfigure(self.inner_frame_id, width=self.canvas.winfo_width())
    self.canvas.bind('<Configure>', _configure_canvas)

  def vertical_scroll(self, event: MouseScrollEvent):
    self.canvas.yview_scroll(int(event.delta), event.what)

  def horizontal_scroll(self, event: MouseScrollEvent):
    self.canvas.xview_scroll(int(event.delta), event.what)

  def show(self, widget: tk.Widget):
    if widget in self.children.values():
      self.canvas.yview_moveto(widget.winfo_y() / self.winfo_height())
