'''
Copyright (C) 2024-2024 Lilith Cybi - All Rights Reserved.
You may use, distribute and modify this code under the
terms of the MIT license.

You should have received a copy of the MIT license with
this file. If not, please write to: lilith.cybi@syrency.com, 
or visit: https://github.com/jmeaster30/lilytk/LICENSE
'''

import tkinter as tk
from typing import Optional

class Highlightable:
  '''
  Capability for highlighting and unhighlighting widgets
  '''

  def __init__(self, target: Optional[tk.BaseWidget] = None, highlight_color: str = '#000', highlight_width: int = 0, blink_delay_ms: int = 0, blink_duration_ms: int = 0):
    self.target = target if target is not None else self
    self.highlight_color = highlight_color
    self.highlight_width = highlight_width
    self.blink_delay_ms = blink_delay_ms
    self.blink_duration_ms = blink_duration_ms

    self.is_blinking = False
    self.blink_on = False
    self.original_background: Optional[str] = None
    self.original_border_width: Optional[int] = None

  def highlight(self):
    self.__internal_highlight()
    self.is_blinking = True
    self.blink_on = True
    self.target.after(self.blink_delay_ms, self.__internal_do_blinking)
    self.target.after(self.blink_duration_ms, self.__internal_stop_blinking)

  def unhighlight(self):
    self.is_blinking = False
    self.blink_on = False
    self.__internal_unhighlight()

  '''
  Internal helpers :3
  '''

  def __internal_do_blinking(self):
    if not self.is_blinking:
      return

    if self.blink_on:
      # turn blink off
      self.blink_on = False
      self.__internal_unhighlight()
    else:
      # turn blink on
      self.blink_on = True
      self.__internal_highlight()

    self.target.after(self.blink_delay_ms, self.__internal_do_blinking)

  def __internal_stop_blinking(self):
    #self.blink_on = False
    self.is_blinking = False
    self.__internal_highlight()

  def __internal_highlight(self):
    if self.original_background is None:
      self.original_background = self.target.cget('background')
    if self.original_border_width is None:
      self.original_border_width = self.target.cget('borderwidth')
    self.target.configure(background=self.highlight_color, borderwidth=self.highlight_width)

  def __internal_unhighlight(self):
    background = '#000' if self.original_background is None else self.original_background
    border_width = 0 if self.original_border_width is None else self.original_border_width
    self.target.configure(background=background, borderwidth=border_width)
