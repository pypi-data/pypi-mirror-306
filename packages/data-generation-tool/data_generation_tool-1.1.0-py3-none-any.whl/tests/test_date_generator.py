import re
from datetime import datetime, timedelta

import pytest

from data_generation_tool.constraints.column_constraints import After, Before, Period, DateFormatType, IncrementalDate, \
    DateFormat
from data_generation_tool.generators import DateGenerator
from data_generation_tool.requests import ColumnGenerationRequest
from data_generation_tool.types import Numeric, Date


class TestDateGenerator:
    def test_date_generator_generation_with_unsupported_column_type(self):
        with pytest.raises(ValueError) as _:
            _ = DateGenerator().generate(
                column=ColumnGenerationRequest(
                    column_type=Numeric,
                    name="Dummy",
                ),
                count=4
            )

    def test_date_generator_generation_without_constraints(self):
        data = DateGenerator().generate(
            column=ColumnGenerationRequest(
                column_type=Date,
                name="Dummy",
            ),
            count=4
        )

        assert len(data) == 4
        assert all(re.match(r'^\d{2}/\d{2}/\d{4}$', x) for x in data)

    def test_date_generator_generation_after_date(self):
        data = DateGenerator().generate(
            column=ColumnGenerationRequest(
                column_type=Date,
                name="Dummy",
                constraints=[
                    After(datetime(2000, 1, 1))
                ]
            ),
            count=4
        )

        assert len(data) == 4
        assert all(re.match(r'^\d{2}/\d{2}/\d{4}$', x) for x in data)
        assert all(datetime.strptime(x, '%d/%m/%Y') >= datetime(2000, 1, 1) for x in data)

    def test_date_generator_generation_before_date(self):
        data = DateGenerator().generate(
            column=ColumnGenerationRequest(
                column_type=Date,
                name="Dummy",
                constraints=[
                    Before(datetime(2000, 1, 1))
                ]
            ),
            count=4
        )

        assert len(data) == 4
        assert all(re.match(r'^\d{2}/\d{2}/\d{4}$', x) for x in data)
        assert all(datetime.strptime(x, '%d/%m/%Y') <= datetime(2000, 1, 1) for x in data)

    def test_date_generator_generation_in_period(self):
        data = DateGenerator().generate(
            column=ColumnGenerationRequest(
                column_type=Date,
                name="Dummy",
                constraints=[
                    Period(
                        lower_bound=datetime(2000, 1, 1),
                        upper_bound=datetime(2003, 1, 1)
                    )
                ]
            ),
            count=4
        )

        assert len(data) == 4
        assert all(re.match(r'^\d{2}/\d{2}/\d{4}$', x) for x in data)
        assert all(datetime(2000, 1, 1) <= datetime.strptime(x, '%d/%m/%Y') <= datetime(2003, 1, 1) for x in data)

    def test_date_generator_generation_incremental(self):
        data = DateGenerator().generate(
            column=ColumnGenerationRequest(
                column_type=Date,
                name="Dummy",
                constraints=[
                    IncrementalDate()
                ]
            ),
            count=4
        )

        assert len(data) == 4
        assert all(re.match(r'^\d{2}/\d{2}/\d{4}$', x) for x in data)
        dates = [datetime.strptime(date_str, '%d/%m/%Y') for date_str in data]

        dates_valid = True
        for i in range(len(dates) - 1):
            if dates[i] > dates[i + 1]:
                dates_valid = False

        for i in range(len(dates) - 1):
            if dates[i + 1] - dates[i] != timedelta(days=1):
                dates_valid = False

        assert dates_valid

    def test_date_generator_generation_with_format(self):
        for fmt_type in [x for x in DateFormatType.__members__.values()]:
            data = DateGenerator().generate(
                column=ColumnGenerationRequest(
                    column_type=Date,
                    name="Dummy",
                    constraints=[
                        DateFormat(fmt_type)
                    ]
                ),
                count=4
            )

            assert len(data) == 4
            assert check_date_format(data, fmt_type.value)


# Util function
def check_date_format(date_strings: list, date_format: str):
    for date_str in date_strings:
        try:
            datetime.strptime(date_str, date_format)
        except ValueError:
            return False
    return True
