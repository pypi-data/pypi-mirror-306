from data_generation_tool.constraints.column_constraints import ColumnConstraint
from data_generation_tool.types import Boolean


class BooleanConstraint(ColumnConstraint):
    """
    Base class for constraints that are related to boolean values
    """

    def target_column_type(self) -> type:
        return Boolean


class Bernoulli(BooleanConstraint):
    """
    Indicates the generated values will follow a Bernoulli distribution, given a parameter `p`
    `p` indicates the proportion of truthy values generated

    Attributes
    ----------
        p: float
            The parameter for the distribution, between 0 and 1 inclusive


    Raises
    -------
        ValueError
            If `p` > 1 or `p` < 0
    """

    def __init__(self, p: float):
        if p < 0 or p > 1:
            raise ValueError("p must be between 0 and 1 inclusive")
        self.p = p
