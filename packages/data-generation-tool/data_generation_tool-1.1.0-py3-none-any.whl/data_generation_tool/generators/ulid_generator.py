import ulid

from data_generation_tool.constraints.column_constraints import Unique
from data_generation_tool.generators import ColumnGenerator
from data_generation_tool.requests import ColumnGenerationRequest
from data_generation_tool.types import ULID


class ULIDGenerator(ColumnGenerator):
    """
    Generator used for ULID columns generation

    ULID is a specification for generating unique and lexicographically sortable 128-bit identifiers
    """

    def generate(self, column: ColumnGenerationRequest, count: int) -> list:
        if column.column_type != ULID:
            raise ValueError(f"Column type {column.column_type} is not ULID")

        unique = False
        for constraint in column.constraints:
            if isinstance(constraint, Unique):
                unique = True
                break

        values = []
        for _ in range(count):
            values.append(str(ulid.ULID()))

        if unique:
            unique_elements = set(values)

            while len(unique_elements) < count:
                diff = count - len(unique_elements)
                for _ in range(diff):
                    unique_elements.add(str(ulid.ULID()))
            values = list(unique_elements)

        return self.post_processing(values, column.constraints)
