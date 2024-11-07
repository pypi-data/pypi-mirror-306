import re

import pytest

from data_generation_tool.generators import UUIDGenerator
from data_generation_tool.requests import ColumnGenerationRequest
from data_generation_tool.types import Numeric, UUID


class TestUUIDGenerator:
    def test_uuid_generator_generation_with_unsupported_column_type(self):
        with pytest.raises(ValueError) as _:
            _ = UUIDGenerator().generate(
                column=ColumnGenerationRequest(
                    column_type=Numeric,
                    name="Dummy",
                ),
                count=4
            )

    def test_uuid_generation_without_constraints(self):
        data = UUIDGenerator().generate(
            column=ColumnGenerationRequest(
                column_type=UUID,
                name="Bar",
                constraints=[]
            ), count=4)

        assert len(data) == 4
        assert all(
            re.match(r"^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$", x) for x
            in data)
