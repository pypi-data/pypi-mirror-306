'''
Copyright (C) 2024-2024 Lilith Cybi - All Rights Reserved.
You may use, distribute and modify this code under the
terms of the MIT license.

You should have received a copy of the MIT license with
this file. If not, please write to: lilith.cybi@syrency.com, 
or visit: https://github.com/jmeaster30/lilytk/LICENSE
'''

import tkinter as tk
from typing import Callable, Literal


Orientation = Literal['both', 'horizontal', 'vertical']
TkEventHandler = Callable[[tk.Event], None]