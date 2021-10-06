"""Config module
===============================
This module sets up some global variables of the framework.
"""


from decimal import getcontext

FLOATING_POINT_DIGITS = 10
"""Floating point precision"""

getcontext().prec = 10
"""Set the floating point precision"""
