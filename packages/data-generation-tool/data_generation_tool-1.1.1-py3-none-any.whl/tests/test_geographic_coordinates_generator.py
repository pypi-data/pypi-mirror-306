import re

import pytest

from data_generation_tool.constraints.column_constraints import CoordinatesFormat, CoordinatesDecimalPrecision
from data_generation_tool.generators import GeographicCoordinatesGenerator
from data_generation_tool.requests import ColumnGenerationRequest
from data_generation_tool.types import GeographicCoordinates, ULID


class TestGeographicCoordinatesGenerator:
    def test_geographic_coordinates_generator_generation_with_unsupported_column_type(self):
        with pytest.raises(ValueError) as _:
            _ = GeographicCoordinatesGenerator().generate(
                column=ColumnGenerationRequest(
                    column_type=ULID,
                    name="Dummy",
                ),
                count=4
            )

    def test_geographic_coordinates_generation_without_constraints(self):
        data = GeographicCoordinatesGenerator().generate(
            column=ColumnGenerationRequest(
                column_type=GeographicCoordinates,
                name="Bar",
                constraints=[]
            ), count=4)

        assert len(data) == 4
        assert all(
            re.match(r"^-?(90(\.0+)?|[1-8]?\d(\.\d+)?)\s*,\s*-?(180(\.0+)?|1[0-7]\d(\.\d+)?|\d{1,2}(\.\d+)?)$", x) for x
            in data)

    def test_geographic_coordinates_with_invalid_fmt_constraint(self):
        with pytest.raises(ValueError) as _:
            _ = GeographicCoordinatesGenerator().generate(
                column=ColumnGenerationRequest(
                    column_type=GeographicCoordinates,
                    name="Bar",
                    constraints=[
                        CoordinatesFormat("lat")
                    ]
                ), count=4)

    def test_geographic_coordinates_with_custom_fmt(self):
        data = GeographicCoordinatesGenerator().generate(
            column=ColumnGenerationRequest(
                column_type=GeographicCoordinates,
                name="Bar",
                constraints=[
                    CoordinatesFormat("lat#long")
                ]
            ), count=4)
        assert len(data) == 4
        assert all(
            re.match(r"^-?(90(\.0+)?|[1-8]?\d(\.\d+)?)#-?(180(\.0+)?|1[0-7]\d(\.\d+)?|\d{1,2}(\.\d+)?)$", x) for x
            in data)

    def test_geographic_coordinates_with_custom_fmt_and_precision(self):
        data = GeographicCoordinatesGenerator().generate(
            column=ColumnGenerationRequest(
                column_type=GeographicCoordinates,
                name="Bar",
                constraints=[
                    CoordinatesFormat("lat#long"),
                    CoordinatesDecimalPrecision(2)
                ]
            ), count=4)

        assert len(data) == 4
        assert all(
            re.match(r"^-?(90(\.\d{1,2})?|[1-8]?\d(\.\d{1,2})?)#-?(180(\.\d{1,2})?|1[0-7]\d(\.\d{1,2})?|\d{1,2}(\.\d{1,2})?)$", x) for x
            in data)