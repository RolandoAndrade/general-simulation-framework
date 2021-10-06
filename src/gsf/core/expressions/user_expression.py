"""User Expression module
=============================
Contains the definition of user defined expressions.
It has the class UserExpression that evaluates an expression defined in an string.

Example:
    Creating an expression::

        true_value = UserExpression("1==1").evaluate()
        false_expression = UserExpression("1==2").evaluate()
        true_value = 3 == UserExpression("1+2").evaluate()

.. warning::
    Currently the use of an object with this class is unsafe.
    Is very dangerous if you accept strings to evaluate from untrusted input because
    it can execute malicious code.

"""

from typing import Any

from gsf.core.expressions import Expression


class UserExpression(Expression):
    value: Any
    """Value of the expression."""

    def __init__(self, expression_value: Any):
        self.value = expression_value

    def evaluate(self):
        return self.value

    def __str__(self):
        return str(self.evaluate())
