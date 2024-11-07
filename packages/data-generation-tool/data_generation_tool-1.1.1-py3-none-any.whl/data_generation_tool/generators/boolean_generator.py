from data_generation_tool.constraints.column_constraints import Bernoulli
from data_generation_tool.generators import ColumnGenerator
from data_generation_tool.requests import ColumnGenerationRequest
from data_generation_tool.types import Boolean


class BooleanGenerator(ColumnGenerator):
    """
    Generator for boolean columns.
    """

    def generate(self, column: ColumnGenerationRequest, count: int) -> list:
        if column.column_type != Boolean:
            raise ValueError(f"Column type {column.column_type} is not Boolean")

        true_percentage = self.rng.uniform()
        for constraint in column.constraints:
            if isinstance(constraint, Bernoulli):
                true_percentage = constraint.p

        true_values_count = int(true_percentage * count)
        values = [True for _ in range(true_values_count)]
        values.extend([False for _ in range(count - true_values_count)])
        self.rng.shuffle(values)
        return self.post_processing(values, column.constraints)
