import uuid

from data_generation_tool.constraints.column_constraints import Unique
from data_generation_tool.generators import ColumnGenerator
from data_generation_tool.requests import ColumnGenerationRequest
from data_generation_tool.types import UUID


class UUIDGenerator(ColumnGenerator):
    """
    Generator used for UUID columns (v4)

    The builtin python UUID generator is used

    A UUID represents a 128-bit value.
    """

    def generate(self, column: ColumnGenerationRequest, count: int) -> list:
        if column.column_type != UUID:
            raise ValueError(f"Column type {column.column_type} is not UUID")

        unique = False
        for constraint in column.constraints:
            if isinstance(constraint, Unique):
                unique = True
                break

        values = []
        for _ in range(count):
            values.append(str(uuid.uuid4()))

        if unique:
            unique_elements = set(values)

            while len(unique_elements) < count:
                diff = count - len(unique_elements)
                for _ in range(diff):
                    unique_elements.add(str(uuid.uuid4()))
            values = list(unique_elements)

        return self.post_processing(values, column.constraints)

