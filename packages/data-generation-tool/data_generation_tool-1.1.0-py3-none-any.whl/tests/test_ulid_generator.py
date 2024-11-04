import re

import pytest

from data_generation_tool.generators import ULIDGenerator
from data_generation_tool.requests import ColumnGenerationRequest
from data_generation_tool.types import Numeric, ULID


class TestULIDGenerator:
    def test_uuid_generator_generation_with_unsupported_column_type(self):
        with pytest.raises(ValueError) as _:
            _ = ULIDGenerator().generate(
                column=ColumnGenerationRequest(
                    column_type=Numeric,
                    name="Dummy",
                ),
                count=4
            )

    def test_uuid_generation_without_constraints(self):
        data = ULIDGenerator().generate(
            column=ColumnGenerationRequest(
                column_type=ULID,
                name="Bar",
                constraints=[]
            ), count=4)

        assert len(data) == 4
        assert all(re.match(r"[0-7][0-9A-HJKMNP-TV-Z]{25}", x) for x in data)
