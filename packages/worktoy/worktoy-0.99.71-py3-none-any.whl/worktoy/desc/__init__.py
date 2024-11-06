"""The 'worktoy.desc' implements the descriptor protocol with lazy
instantiation. """
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from ._core_descriptor import CoreDescriptor
from ._abstract_descriptor import AbstractDescriptor
from ._bag import Bag
from ._zero_this import THIS
from ._zero_type import TYPE
from ._zero_box import BOX
from ._zero_attr import ATTR
from ._field import Field
from ._zero_filter import ZeroFilter
from ._attri_box import AttriBox
