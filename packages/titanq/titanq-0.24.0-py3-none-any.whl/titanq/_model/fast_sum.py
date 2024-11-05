# Copyright (c) 2024, InfinityQ Technology, Inc.
from typing import Iterable
from .math_object import MathObject, Expression

def fast_sum(values: Iterable[MathObject]) -> Expression:
    """
    ℹ️ **This feature is experimental and may change.**

    Computes the sum of all elements provided.
    This function is an faster alternative to the traditional `sum()` operation for vector-based expressions.

    Parameters
    ----------
    values
        The `VectorExpression` or `VariableVector` whose elements are to be summed.

    Returns
    -------
    Expression
        An `Expression` representing the sum of the elements in `exprVector`.

    Raises
    ------
    ValueError
        If the provided input is not of type `VectorExpression` or `VariableVector`.

    Examples
    --------
    >>> from titanq import Model, Vtype
    >>> x = model.add_variable_vector('x', 1000, Vtype.BINARY)
    >>> y = model.add_variable_vector('y', 1000, Vtype.BINARY)
    >>> exprA = fastSum(x + (x * y) - 5 * y)
    >>> exprB = fastSum(x)
    """
    try:
        terms = []
        for v in values:
            terms.extend(v.terms())
        return Expression(terms)
    except AttributeError as ex:
        raise TypeError(f"Fast sum only work with MathObject, not {type(ex.obj).__name__}")
