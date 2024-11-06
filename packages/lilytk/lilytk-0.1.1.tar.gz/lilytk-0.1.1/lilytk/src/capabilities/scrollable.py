'''
Copyright (C) 2024-2024 Lilith Cybi - All Rights Reserved.
You may use, distribute and modify this code under the
terms of the MIT license.

You should have received a copy of the MIT license with
this file. If not, please write to: lilith.cybi@syrency.com, 
or visit: https://github.com/jmeaster30/lilytk/LICENSE
'''

import platform
import tkinter as tk
from typing import Callable, Literal, Optional

from lilytk.src.typing import Orientation, TkEventHandler
from lilytk.src.utils import EMPTY_HANDLER


class MouseScrollEvent:
  def __init__(self, x: int, y: int, delta: float, what: Literal['units', 'pages']):
    self.x = x
    self.y = y
    self.delta = delta
    self.what = what


MouseScrollEventHandler = Callable[[MouseScrollEvent], None]


class Scrollable:
  '''
  Capability for responding to mouse scroll events
  '''

  def __init__(self, target: Optional[tk.BaseWidget] = None, bind_all: bool = True, bind_enter_leave: bool = True, orient: Orientation = tk.VERTICAL, scrolling_factor: float = 1.0):
    self.target = target if target is not None else self
    self.__mouse_scroll_vertical_binding_0: Optional[str] = None
    self.__mouse_scroll_vertical_binding_1: Optional[str] = None
    self.__mouse_scroll_horizontal_binding_0: Optional[str] = None
    self.__mouse_scroll_horizontal_binding_1: Optional[str] = None
    if bind_enter_leave:
      self.__bind_enter_leave_mouse_scroll(bind_all, orient, scrolling_factor, self.horizontal_scroll, self.vertical_scroll)
    else:
      self.__bind_scroll(bind_all, orient, scrolling_factor, self.horizontal_scroll, self.vertical_scroll)

  def horizontal_scroll(self, event: MouseScrollEvent):
    pass

  def vertical_scroll(self, event: MouseScrollEvent):
    pass

  '''
  Internal bind helpers
  '''

  def __bind_enter_leave_mouse_scroll(self, bind_all: bool = False, orient: Orientation = tk.VERTICAL, scrolling_factor: int = 120,
                                      xscrollcommand: MouseScrollEventHandler = EMPTY_HANDLER, 
                                      yscrollcommand: MouseScrollEventHandler = EMPTY_HANDLER):
    self.bind('<Enter>', lambda event: self.__bind_scroll(bind_all, orient, scrolling_factor, xscrollcommand, yscrollcommand), True)
    self.bind('<Leave>', lambda event: self.__unbind_scroll(), True)


  def __bind_scroll(self, bind_all: bool = False, orient: Orientation = tk.VERTICAL, scrolling_factor: int = 120,
                    xscrollcommand: MouseScrollEventHandler = EMPTY_HANDLER, 
                    yscrollcommand: MouseScrollEventHandler = EMPTY_HANDLER):
    if orient == tk.VERTICAL or orient == tk.BOTH:
      self.__bind_vertical_scroll(yscrollcommand, bind_all, scrolling_factor)
    if orient == tk.VERTICAL or orient == tk.BOTH:
      self.__bind_horizontal_scroll(xscrollcommand, bind_all, scrolling_factor)

  def __unbind_scroll(self):
    if self.__mouse_scroll_vertical_binding_0 is not None:
      if platform.system() == 'Linux':
        self.target.unbind("<Button-4>", self.__mouse_scroll_vertical_binding_0)
      else:
        self.target.unbind("<Mousewheel>", self.__mouse_scroll_vertical_binding_0)

    if self.__mouse_scroll_vertical_binding_1 is not None:
      self.target.unbind("<Button-5>", self.__mouse_scroll_vertical_binding_1)

    if self.__mouse_scroll_horizontal_binding_0 is not None:
      if platform.system() == 'Linux':
        self.target.unbind("<Shift-Button-4>", self.__mouse_scroll_horizontal_binding_0)
      else:
        self.target.unbind("<Shift-Mousewheel>", self.__mouse_scroll_horizontal_binding_0)
    
    if self.__mouse_scroll_horizontal_binding_1 is not None:
      self.target.unbind("<Shift-Button-5>", self.__mouse_scroll_horizontal_binding_1)

  def __bind_vertical_scroll(self, action: MouseScrollEventHandler = EMPTY_HANDLER, bind_all: bool = True, scrolling_factor: int = 120):
    match platform.system():
      case 'Windows':
        self.__mouse_scroll_vertical_binding_0 = self.__base_event_binding_helper(bind_all, "<Mousewheel>", lambda event: action(MouseScrollEvent(event.x, event.y, -1*(event.delta/120)*scrolling_factor, 'units')))

      case 'Darwin':
        self.__mouse_scroll_vertical_binding_0 = self.__base_event_binding_helper(bind_all, "<Mousewheel>", lambda event: action(MouseScrollEvent(event.x, event.y, event.delta * scrolling_factor, 'units')))
      case 'Linux':
        self.__mouse_scroll_vertical_binding_0 = self.__base_event_binding_helper(bind_all, "<Button-4>", lambda event: action(MouseScrollEvent(event.x, event.y, -scrolling_factor, 'units')))
        self.__mouse_scroll_vertical_binding_1 = self.__base_event_binding_helper(bind_all, "<Button-5>", lambda event: action(MouseScrollEvent(event.x, event.y, scrolling_factor, 'units')))
      case _:
        raise NotImplementedError(f"We don't know how to bind mouse scroll to '{platform.system()}'")
      
  def __bind_horizontal_scroll(self, action: MouseScrollEventHandler = EMPTY_HANDLER, bind_all: bool = True, scrolling_factor: int = 120):
    match platform.system():
      case 'Windows':
        self.__mouse_scroll_horizontal_binding_0 = self.__base_event_binding_helper(bind_all, "<Shift-Mousewheel>", lambda event: action(MouseScrollEvent(event.x, event.y, -1*(event.delta/scrolling_factor), 'units')))
      case 'Darwin':
        self.__mouse_scroll_horizontal_binding_0 = self.__base_event_binding_helper(bind_all, "<Shift-Mousewheel>", lambda event: action(MouseScrollEvent(event.x, event.y, event.delta, 'units')))
      case 'Linux':
        self.__mouse_scroll_horizontal_binding_0 = self.__base_event_binding_helper(bind_all, "<Shift-Button-4>", lambda event: action(MouseScrollEvent(event.x, event.y, 120 / scrolling_factor, 'units')))
        self.__mouse_scroll_horizontal_binding_1 = self.__base_event_binding_helper(bind_all, "<Shift-Button-5>", lambda event: action(MouseScrollEvent(event.x, event.y, -120 / scrolling_factor, 'units')))
      case _:
        raise NotImplementedError(f"We don't know how to bind mouse scroll to '{platform.system()}'")

  def __base_event_binding_helper(self, bind_all: bool, event_sequence: str, event_handler: TkEventHandler):
    if bind_all:
      return self.target.bind_all(event_sequence, event_handler, True)
    else:
      return self.target.bind(event_sequence, event_handler, True)
