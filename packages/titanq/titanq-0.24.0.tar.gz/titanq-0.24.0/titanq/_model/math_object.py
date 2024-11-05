# Copyright (c) 2024, InfinityQ Technology, Inc.

from abc import ABC, abstractmethod
from collections import defaultdict
import enum
from typing import Dict, List, Optional, Tuple
import warnings

import numpy as np
import numpy.typing as npt

class Vtype(str, enum.Enum):
    """
    All variable types currently supported by the solver.

    ℹ️ **NOTE:** Bipolar variables are not directly supported,
    but :class:`tools.BipolarToBinary` can be used as an alternative.
    """

    BINARY = 'binary'
    INTEGER = 'integer'
    CONTINUOUS = 'continuous'

    def __str__(self) -> str:
        return str(self.value)

    def _api_str(self) -> str:
        """
        Convert the `Vtype` enum to its corresponding API string representation.

        This method returns a shorthand character used by the API to identify 
        the variable type. The mapping is as follows:

        - 'b' for BINARY
        - 'c' for CONTINUOUS
        - 'i' for INTEGER

        Returns
        -------
        A string representing the variable type in the API.
        """
        if self == Vtype.BINARY:
            return 'b'
        elif self == Vtype.CONTINUOUS:
            return 'c'
        else: # Vtype.Integer
            return 'i'


class ConstraintType(str, enum.Enum):
    """
    All constraint types currently supported in expression.
    """
    EQUAL = '=='
    GREATER_EQUAL = '>='
    GREATER = '>'
    LESSER_EQUAL = '<='
    LESSER = '<'

    def __str__(self) -> str:
        return str(self.value)


class MathObject(ABC):
    @abstractmethod
    def terms(self) -> List['Term']:
        """
        Returns
        -------
        A copy of all the terms of this math object
        """

    @abstractmethod
    def __add__(self, other):
        return NotImplemented

    @abstractmethod
    def __mul__(self, other):
        return NotImplemented

    @abstractmethod
    def __sub__(self, other):
        return NotImplemented

    @abstractmethod
    def _populate_weights(self, weights: npt.NDArray):
        """
        Populate the given weight matrix with the appropriate values contained in this MathObject.

        Parameters
        ----------
        weights
            A numpy array representing the weights to be populated.
        """

    @abstractmethod
    def _populate_bias(self, bias: npt.NDArray):
        """
        Populate the given bias matrix with the appropriate values contained in this MathObject.

        Parameters
        ----------
        bias
            A numpy array representing the bias values to be populated.
        """

    def generate_weights(self, variable_list: List['Variable']) -> Optional[npt.NDArray[np.float32]]:
        """
        Generate a 2D square weight matrix.

        Parameters
        ----------
        variable_list
            A list of variables for which the weights will be generated.

        Returns
        -------
        A weight matrix of type `np.float32`, or `None` if all weights are zero.
        """
        weights = np.zeros((len(variable_list), len(variable_list)), dtype=np.float32)
        self._populate_weights(weights)
        return weights if np.any(weights) else None

    def generate_bias(self, variable_list: List['Variable']) -> npt.NDArray[np.float32]:
        """
        Generate a 1D bias vector.

        Parameters
        ----------
        variable_list
            A list of variables for which the bias will be generated.

        Returns
        -------
        A bias vector of type `np.float32`.
        """
        bias = np.zeros(len(variable_list), dtype=np.float32)
        self._populate_bias(bias)
        return bias

    def __eq__(self, other):
        return Equation(self, ConstraintType.EQUAL, other)

    def __lt__(self, other):
        warnings.warn(
            "TitanQ does not support strictly less than constraints (<). Your less than constraint has been parsed "
            "as a less than or equal to (<=). If this was not intended please reformulate the expression appropriately."
        )
        return self.__le__(other)

    def __le__(self, other):
        return Equation(self, ConstraintType.LESSER_EQUAL, other)

    def __gt__(self, other):
        warnings.warn(
            "TitanQ does not support strictly greater than constraints (>). Your greater than constraint has been parsed "
            "as a greater than or equal to (>=). If this was not intended please reformulate the expression appropriately."
        )
        return self.__ge__(other)

    def __ge__(self, other):
        return Equation(self, ConstraintType.GREATER_EQUAL, other)

    def __sub__(self, other):
        return self + (-1 * other)

    def __rsub__(self, other):
        return (-1 * self) + other

    def __radd__(self, other):
        return self.__add__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, other):
        if isinstance(other, int):
            res = self
            for _ in range(other-1):
                res = res * self
            return res
        return NotImplemented

    def __repr__(self) -> str:
        return self.__str__()


class Variable(MathObject):
    """
    Variable is the smallest object in the problem formulation.

    Each variable can have different types such as binary, integer, or continuous.
    The solver will determine the optimal values for the variables based on the
    constraints and the objective function.
    """
    def __init__(self, parent: str, index: int, problem_index: int) -> None:
        super().__init__()
        self._parent_name = parent
        self._variable_index = index
        self._problem_index = problem_index

    @abstractmethod
    def vtype(self) -> Vtype:
        """
        Returns
        -------
        Type of the variable.
        """

    @abstractmethod
    def variable_bounds(self) -> npt.NDArray[np.float32]:
        """
        Returns
        -------
        The variable bounds associated to this variable
        """

    def problem_index(self) -> int:
        """
        Returns
        -------
        The index of this variable for the whole problem
        """
        return self._problem_index

    def parent_name(self) -> str:
        """
        Returns
        -------
        The name of the parent variable vector
        """
        return self._parent_name

    def terms(self) -> List['Term']:
        return [Term(1, [self])]

    def __str__(self) -> str:
        return f"{self._parent_name}[{self._variable_index}]"

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Expression(self.terms() + [Term(other)])
        elif isinstance(other, Variable):
            return Expression(self.terms() + other.terms())
        else:
            return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Term(other, [self])
        elif isinstance(other, Variable):
            return Term(1, [self, other])
        else:
            return NotImplemented

    def _populate_weights(self, weights: npt.NDArray):
        pass

    def _populate_bias(self, bias: npt.NDArray):
        bias[self.problem_index()] = 1


class BinaryVariable(Variable):
    def vtype(self) -> Vtype: return Vtype.BINARY
    def variable_bounds(self) -> npt.NDArray[np.float32]: return np.array([0,1], dtype=np.float32)

class IntegerVariable(Variable):
    def __init__(self, parent: str, index: int, problem_index: int, bounds: Tuple[int, int]) -> None:
        super().__init__(parent, index, problem_index)
        self._bounds = bounds

    def vtype(self) -> Vtype:
        return Vtype.INTEGER

    def variable_bounds(self) -> npt.NDArray[np.float32]:
        return self._bounds

class ContinuousVariable(Variable):
    def __init__(self, parent: str, index: int, problem_index: int, bounds: Tuple[int, int]) -> None:
        super().__init__(parent, index, problem_index)
        self._bounds = bounds

    def vtype(self) -> Vtype:
        return Vtype.CONTINUOUS

    def variable_bounds(self) -> npt.NDArray[np.float32]:
        return self._bounds


class Term(MathObject):
    """
    Term is a composition of a coef and a list of variables.

    Notes
    -----
    Currently, Titanq Does not support higher than 2 degree.

    Examples
    --------
    In the following equation:  `7xz + 4xy - 3z + 12` we have 3 terms of different degree:
    -   `7xz` (degree 2)
    -   `4xy` (degree 2)
    -   `3z`  (degree 1)
    -   `12`  (degree 0)
    """
    def __init__(self, coef: float, variables: List[Variable] = []) -> None:
        super().__init__()
        if len(variables)>2:
            raise ValueError("Titanq does not support terms with a degree greater than 2.")

        self._variables = variables
        self._coef = coef

    def terms(self) -> List['Term']:
        return [Term(self._coef, self._variables.copy())]

    def degree(self) -> int:
        """
        Returns
        -------
        The degree of this term
        """
        return len(self._variables)

    def coef(self) -> int:
        """
        Returns
        -------
        The numerical coefficient of this term
        """
        return self._coef

    def variables(self) -> List[Variable]:
        """
        Returns
        -------
        List of variable of this term
        """
        return self._variables

    def __str__(self) -> str:
        if len(self._variables) == 0:
            return str(self._coef)

        s = ''
        if self._coef == -1:
            s += '-'
        elif self._coef != 1:
            s += str(self._coef) + ' '
        s += '*'.join([str(v) for v in self._variables])
        return s

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Expression([self, Term(other)])
        elif isinstance(other, Variable):
            return Expression([self, Term(1, [other])])
        elif isinstance(other, Term):
            return Expression([self, other])
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Term(self._coef * other, self._variables)
        elif isinstance(other, Variable):
            return Term(self._coef, self._variables + [other])
        elif isinstance(other, Term):
            return Term(self._coef * other._coef, self._variables + other._variables)
        else:
            return NotImplemented

    def _populate_weights(self, weights):
        if self.degree() == 2:
            index1 = self._variables[0].problem_index()
            index2 = self._variables[1].problem_index()

            # The matrix is supposed to be symmetric.
            # Note: for the diagonal, this will double the value since index1 == index2.
            # This is the intended behavior
            weights[index1, index2] += self._coef
            weights[index2, index1] += self._coef

    def _populate_bias(self, bias: npt.NDArray):
        if self.degree() == 1:
            index = self._variables[0].problem_index()
            bias[index] += self._coef


def simplify(terms: List[Term]) -> List[Term]:
    """
    Simplify the given list of term by combining terms with the same variables.

    Examples
    --------
    `4x + 12xy + 9 + 3x - 6yx` -> `6xy + 7x + 9`
    """
    simplified_terms: Dict[List[Variable], float] = defaultdict(lambda: 0)
    variables_mapping: Dict[str, List[Variable]] = defaultdict(lambda: [])

    # add similar term together
    for term in terms:
        # the problem_index of each variable should be unique. If 2 variable have the same
        # problem index, we can conclude that they are the same. Thats why we sort them by this index
        variables = sorted(term.variables(), key=lambda v: v.problem_index())
        variables_key = ''.join(str(v) for v in variables)
        variables_mapping[variables_key] = variables
        simplified_terms[variables_key] += term.coef()

    new_terms: List[Term] = []
    for variables_key, coef in simplified_terms.items():
        if coef == 0:
            # skip term that has a coefficient of 0
            continue
        new_terms.append(Term(coef, variables_mapping[variables_key]))
    return new_terms

class Expression(MathObject):
    """
    An Expression is a sum of multiple term
    """
    def __init__(self, terms: List[Term] = []) -> None:
        super().__init__()
        self._terms = simplify(terms)

    def terms(self) -> List[Term]:
        return self._terms.copy()

    def __str__(self) -> str:
        return " + ".join([str(t) for t in self._terms])

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Expression(self._terms + [Term(other)])
        elif isinstance(other, Variable):
            return Expression(self._terms + [Term(1, [other])])
        elif isinstance(other, Term):
            return Expression(self._terms + [other])
        elif isinstance(other, Expression):
            return Expression(self._terms + other._terms)
        else:
            return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, float, Variable, Term)):
            return Expression([other * term for term in self._terms])
        elif isinstance(other, Expression):
            terms = []
            for t1 in self._terms:
                for t2 in other._terms:
                    terms.append(t1 * t2)
            return Expression(terms)
        else:
            return NotImplemented

    def _populate_weights(self, weights):
        for term in self._terms:
            term._populate_weights(weights)

    def _populate_bias(self, bias: npt.NDArray):
        for term in self._terms:
            term._populate_bias(bias)


class Equation():
    """
    Equation is 2 expression with a comparison operator between them

    Examples
    --------
    `4x + 2y > 3z`
    """
    def __init__(self, rhs: MathObject, operator: ConstraintType, lhs: MathObject) -> None:
        self._rhs = rhs
        self._operator = operator
        self._lhs = lhs

    def generate_constraint(self, variable_list: List[Variable]) -> Tuple[npt.NDArray, npt.NDArray]:
        """
        Generate the constraint matrix row defined by this equation

        Parameters
        ----------
        variables_list
            List of all variables of the problem
        """
        expression: Expression = self._rhs - self._lhs
        if not isinstance(expression, MathObject):
            raise TypeError("TitanQ only supports single expression constraint input")

        mask = np.zeros(len(variable_list), dtype=np.float32)
        const = 0

        for term in expression.terms():
            degree = term.degree()
            if degree == 0:
                const += term.coef()
            elif degree == 1:
                index = term._variables[0].problem_index()
                mask[index] += term.coef()
            else:
                raise ValueError(
                    "Quadratic terms are not supported in constraints. "
                    "Please ensure that the expression contains only linear terms when using it in a constraint."
                )

        bounds = []
        const = -const # inverse constant because it should be on the other side of the equation

        if self._operator == ConstraintType.EQUAL:
            bounds = [const, const]
        elif self._operator == ConstraintType.GREATER:
            # This should never be raise since greater get parsed as greater or equal
            raise NotImplementedError("TitanQ does not support strictly greater constraint")
        elif self._operator == ConstraintType.GREATER_EQUAL:
            bounds = [const, np.nan]
        elif self._operator == ConstraintType.LESSER:
            # This should never be raise since less than get parsed as less or equal than
            raise NotImplementedError("TitanQ does not support strictly lesser constraint")
        elif self._operator == ConstraintType.LESSER_EQUAL:
            bounds = [np.nan, const]

        return mask, np.array(bounds, dtype=np.float32)

    def __str__(self) -> str:
        return f"{self._rhs} {self._operator} {self._lhs}"
