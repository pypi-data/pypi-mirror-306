import pytest

from data_generation_tool.constraints.column_constraints import Bernoulli
from data_generation_tool.generators import BooleanGenerator
from data_generation_tool.requests import ColumnGenerationRequest
from data_generation_tool.types import Numeric, Boolean


class TestBooleanGenerator:
    def test_boolean_generator_generation_with_unsupported_column_type(self):
        with pytest.raises(ValueError) as _:
            _ = BooleanGenerator().generate(
                column=ColumnGenerationRequest(
                    column_type=Numeric,
                    name="Dummy",
                ),
                count=4
            )

    def test_date_generator_generation_without_constraints(self):
        data = BooleanGenerator().generate(
            column=ColumnGenerationRequest(
                column_type=Boolean,
                name="Dummy",
            ),
            count=4
        )

        assert len(data) == 4

    def test_date_generator_generation_with_distribution(self):
        data = BooleanGenerator().generate(
            column=ColumnGenerationRequest(
                column_type=Boolean,
                name="Dummy",
                constraints=[Bernoulli(p=0.6)]
            ),
            count=10,

        )

        assert len(data) == 10
        assert len(list(filter(lambda x: x == True, data))) == 6
