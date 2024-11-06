"""TYPE is a Zeroton serving as placeholder for the yet to be created
class owning the AttriBox instance."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

try:
  from typing import Callable
except ImportError:
  Callable = object

from worktoy.meta import Zeroton


class TYPE(Zeroton):
  """TYPE is a Zeroton serving as placeholder for the yet to be created
  class owning the AttriBox instance."""

  __TYPE_ZEROTON__ = True

  __call_me_maybe__ = None

  def __matmul__(self, callMeMaybe: Callable) -> None:
    self.__call_me_maybe__ = callMeMaybe

  def __call__(self, owner: type, *args, **kwargs) -> None:
    self.__call_me_maybe__(owner, *args, **kwargs)
