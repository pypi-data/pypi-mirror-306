from datetime import datetime, timedelta

from data_generation_tool.constraints.column_constraints import Future, Past, After, Before, Period, DateFormat, \
    RandomDate, IncrementalDate
from data_generation_tool.errors import UnsatisfiableConstraints
from data_generation_tool.generators import ColumnGenerator
from data_generation_tool.requests import ColumnGenerationRequest
from data_generation_tool.types import Date
from data_generation_tool.utils import DateIncrementUnit, DateFormatType


class DateGenerator(ColumnGenerator):
    """
    Generator for date columns.

    The format of the generated date can be specified using a constraint, otherwise python the date objects
    """

    def generate(self, column: ColumnGenerationRequest, count: int) -> list:
        if column.column_type != Date:
            raise ValueError(f"Column type {column.column_type} is not Date")

        now = datetime.now()
        start_date = None
        end_date = None

        date_format = DateFormatType.EU
        mode = "random"
        increment_step = 1
        increment_unit = DateIncrementUnit.DAY

        for constraint in column.constraints:
            if isinstance(constraint, Future):
                if start_date is None:
                    start_date = now
                else:
                    start_date = max(start_date, now)

            elif isinstance(constraint, Past):
                if end_date is None:
                    end_date = now
                else:
                    end_date = min(end_date, now)

            elif isinstance(constraint, After):
                if start_date is None:
                    start_date = constraint.value
                else:
                    start_date = max(start_date, constraint.value)

            elif isinstance(constraint, Before):
                if end_date is None:
                    end_date = constraint.value
                else:
                    end_date = min(end_date, constraint.value)

            elif isinstance(constraint, Period):
                if start_date is None:
                    start_date = constraint.lower_bound
                else:
                    start_date = max(start_date, constraint.lower_bound)

                if end_date is None:
                    end_date = constraint.upper_bound
                else:
                    end_date = min(end_date, constraint.upper_bound)

            elif isinstance(constraint, RandomDate):
                mode = "random"

            elif isinstance(constraint, IncrementalDate):
                mode = "incremental"
                increment_step = constraint.step
                increment_unit = constraint.unit

            elif isinstance(constraint, DateFormat):
                date_format = constraint.value

        if start_date is None:
            if end_date is None:
                days_between = 84370
                random_days = self.rng.integers(0, days_between)
                start_date = datetime(1970, 1, 1) + timedelta(days=int(random_days))
            else:
                start_date = end_date - timedelta(days=3650)

        if end_date is None:
            end_date = start_date + timedelta(days=3650)

        if start_date > end_date:
            raise UnsatisfiableConstraints("The constraints are unsatisfiable.")

        values = []
        if mode == "random":
            for _ in range(count):
                random_date = start_date + timedelta(
                    days=int(self.rng.integers(0, (end_date - start_date).days, endpoint=True))
                )
                values.append(random_date.strftime(str(date_format.value)))
        else:
            if increment_unit == DateIncrementUnit.SECOND:
                delta = increment_step * timedelta(seconds=1)
            elif increment_unit == DateIncrementUnit.MINUTE:
                delta = increment_step * timedelta(minutes=1)
            elif increment_unit == DateIncrementUnit.HOUR:
                delta = increment_step * timedelta(hours=1)
            else:
                delta = increment_step * timedelta(days=1)

            for i in range(count):
                incremental_date = start_date + i * delta
                values.append(incremental_date.strftime(str(date_format.value)))

        return self.post_processing(values, column.constraints)
