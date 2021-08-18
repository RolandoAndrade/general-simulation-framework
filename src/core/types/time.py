from decimal import Decimal, getcontext

from core.config import FLOATING_POINT_DIGITS

Time = Decimal

getcontext().prec = FLOATING_POINT_DIGITS
