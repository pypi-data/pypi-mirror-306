import re
from datetime import time, datetime, timedelta

import pytest

from data_generation_tool.constraints.column_constraints import TimeFormatType, IncrementalTime, TimeFormat
from data_generation_tool.generators import TimeGenerator
from data_generation_tool.requests import ColumnGenerationRequest
from data_generation_tool.types import Numeric, Time


class TestTimeGenerator:
    def test_time_generator_generation_with_unsupported_column_type(self):
        with pytest.raises(ValueError) as _:
            _ = TimeGenerator().generate(
                column=ColumnGenerationRequest(
                    column_type=Numeric,
                    name="Dummy",
                ),
                count=4
            )

    def test_time_generator_generation_without_constraints(self):
        data = TimeGenerator().generate(
            column=ColumnGenerationRequest(
                column_type=Time,
                name="Dummy",
            ),
            count=4
        )

        assert len(data) == 4
        assert all(re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$", x) for x in data)

    def test_time_generator_generation_incremental(self):
        data = TimeGenerator().generate(
            column=ColumnGenerationRequest(
                column_type=Time,
                name="Dummy",
                constraints=[IncrementalTime()]
            ),
            count=4
        )

        assert len(data) == 4
        assert all(re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d$", x) for x in data)
        times = [datetime.strptime(time_str, "%H:%M:%S") for time_str in data]
        print(times)

        times_valid = True
        for i in range(len(times) - 1):
            if times[i] > times[i + 1]:
                times_valid = False

        for i in range(len(times) - 1):
            if times[i + 1] - times[i] != timedelta(seconds=1):
                times_valid = False

        assert times_valid

    def test_time_generator_generation_with_format(self):
        for fmt_type in [x for x in TimeFormatType.__members__.values()]:
            data = TimeGenerator().generate(
                column=ColumnGenerationRequest(
                    column_type=Time,
                    name="Dummy",
                    constraints=[TimeFormat(fmt_type)]
                ),
                count=4
            )

            assert len(data) == 4
            assert check_time_format(data, fmt_type.value)


# Util function
def check_time_format(time_strings: list, time_format: str):
    for time_str in time_strings:
        try:
            datetime.strptime(time_str, time_format)
        except ValueError:
            return False
    return True
