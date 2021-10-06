"""Time module
===============================
This module contains the definitions of types and aliases used in the framework.
"""

from decimal import Decimal, getcontext

from gsf.core.config import FLOATING_POINT_DIGITS

Time = Decimal
"""Definition of the Time alias"""

getcontext().prec = FLOATING_POINT_DIGITS
"""Sets the floating point precision."""
