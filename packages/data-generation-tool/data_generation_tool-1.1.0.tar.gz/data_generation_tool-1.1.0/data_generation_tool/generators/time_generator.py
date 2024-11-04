from datetime import timedelta, datetime, time

from data_generation_tool.constraints.column_constraints import RandomTime, IncrementalTime, TimeFormat
from data_generation_tool.generators import ColumnGenerator
from data_generation_tool.requests import ColumnGenerationRequest
from data_generation_tool.types import Time
from data_generation_tool.utils import TimeFormatType, TimeIncrementUnit


class TimeGenerator(ColumnGenerator):
    """
    Generator for time columns
    """

    def generate(self, column: ColumnGenerationRequest, count: int) -> list:
        if column.column_type != Time:
            raise ValueError(f"Column type {column.column_type} is not Time")

        time_format = TimeFormatType.HOUR_MIN_SEC_24
        mode = "random"
        increment_step = 1
        increment_unit = TimeIncrementUnit.SECOND

        for constraint in column.constraints:
            if isinstance(constraint, RandomTime):
                mode = "random"

            elif isinstance(constraint, IncrementalTime):
                mode = "incremental"
                increment_step = constraint.step
                increment_unit = constraint.unit

            elif isinstance(constraint, TimeFormat):
                time_format = constraint.value

        values = []
        if mode == "random":
            for _ in range(count):
                random_time = time(self.rng.integers(0, 24), self.rng.integers(0, 60), self.rng.integers(0, 60))
                values.append(random_time.strftime(str(time_format.value)))
        else:
            start_time = time(self.rng.integers(0, 24), self.rng.integers(0, 60), self.rng.integers(0, 60))

            if increment_unit == TimeIncrementUnit.SECOND:
                delta = increment_step * timedelta(seconds=1)
            elif increment_unit == TimeIncrementUnit.MINUTE:
                delta = increment_step * timedelta(minutes=1)
            else:
                delta = increment_step * timedelta(hours=1)

            for i in range(count):
                incremental_time = add_to_time(start_time, i * delta)
                values.append(incremental_time.strftime(str(time_format.value)))

        return self.post_processing(values, column.constraints)


def add_to_time(t: time, delta: timedelta) -> time:
    return (datetime.combine(datetime.today(), t) + delta).time()


def subtract_to_time(t: time, delta: timedelta) -> time:
    return (datetime.combine(datetime.today(), t) - delta).time()
