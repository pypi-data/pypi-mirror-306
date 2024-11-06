'''
Copyright (C) 2024-2024 Lilith Cybi - All Rights Reserved.
You may use, distribute and modify this code under the
terms of the MIT license.

You should have received a copy of the MIT license with
this file. If not, please write to: lilith.cybi@syrency.com, 
or visit: https://github.com/jmeaster30/lilytk/LICENSE
'''

from typing import Any, Callable


EMPTY_HANDLER = lambda event: None

def debug_handler(handler: Callable[..., None]) -> Callable[..., None]:
  def internal(*args, **kwargs):
    print(f'ARGS: {args}')
    print(f'KWARGS: {kwargs}')
    handler(*args, *kwargs)
  return internal