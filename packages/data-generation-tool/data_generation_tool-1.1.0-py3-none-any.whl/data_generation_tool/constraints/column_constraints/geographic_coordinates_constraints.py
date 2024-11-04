from data_generation_tool.constraints.column_constraints import ColumnConstraint
from data_generation_tool.types import GeographicCoordinates
from data_generation_tool.utils import COUNTRIES_ISO_CODES


class GeographicCoordinateConstraint(ColumnConstraint):
    """
    Base class for constraints that can be applied to columns containing geographic coordinates
    """

    def target_column_type(self) -> type:
        return GeographicCoordinates


class CoordinatesFormat(GeographicCoordinateConstraint):
    """
    Indicate how the coordinates should be encoded within the string.\n
    By default, the format will be lat, long

    Attributes
    ----------
        fmt: str
            The format for the encoded coordinates

    Raises
    -------
        ValueError
            If `format` does not contain exactly one occurrence of lat and long, because they are required for the formatting to be done
    """

    def __init__(self, fmt: str):
        if fmt.count('lat') != 1 or fmt.count('long') != 1:
            raise ValueError("Invalid fmt string")

        self.fmt = fmt


class CoordinatesDecimalPrecision(GeographicCoordinateConstraint):
    """
       Indicate that the longitude and latitude generated should have a certain max precision.\n
       Higher the precision is, lower will be the error in the location\n
       - 0 decimal places : An error of 110,574.3 meters (≈ 111 kilometers)\n
       - 1 decimal place : An error of 11,057.43 meters (≈ 11 kilometers)\n
       - 2 decimal places : An error of 1,105.74 meters (≈ 1 kilometer)\n
       - 3 decimal places : An error of 110.57 meters (≈ 110 meters)\n
       - 4 decimal places : An error of 11.06 meters (≈ 11 meters)\n
       - 5 decimal places : An error of 1.11 meters (≈ 1 meter)\n
       - 6 decimal places : An error of 0.11 meters (≈ 11 centimeters)\n
       - 7 decimal places : An error of 0.01 meters (≈ 1 centimeter)\n
       - 8 decimal places : An error of 0.001 meters (≈ 1 millimeter)

       Attributes
       ----------
           value: int
               The number of digits.

       Raises
       -------
           ValueError
               If `value` is lower than 0 or higher than 8.
   """

    def __init__(self, value: int):
        if value < 0:
            raise ValueError("The precision should be non-negative")

        if value > 8:
            raise ValueError("The precision must be lower than 8")

        self.value = value


class ContinentCoordinates(GeographicCoordinateConstraint):
    """
    Indicate that the generated coordinates should belong to a continent.\n
    The accepted continents are "Africa", "America", "Antarctica", "Asia", "Europe", "North America" and "South America"\n

    Attributes
    ----------
        value: frozenset
            The continents the generated points should belong to

    Raises
    -------
        ValueError
            If an unknown value is given for the continent
    """

    def __init__(self, *values):
        if not values:
            raise ValueError("At least one value is required.")

        continents = set()
        for value in values:
            if value != "Africa" and value != "America" and value != "Antarctica" and value != "Asia" and \
                    value != "Europe" and value != "North America" and value != "South America":
                raise ValueError("Invalid continent " + value)

            if value == "America":
                continents.add("North America")
                continents.add("South America")
            else:
                continents.add(value)

        self.value = continents


class CountryCoordinates(GeographicCoordinateConstraint):
    """
    Indicate that the generated coordinates should belong to a country.\n
    The accepted values are the ISO 3166-1 alpha-2 codes of all countries

    Attributes
    ----------
        value: frozenset
            The countries the generated points should belong to

    Raises
    -------
        ValueError
            If an unknown value is given for the code
    """

    def __init__(self, *values):
        if not values:
            raise ValueError("At least one value is required.")

        countries_codes = set()
        for value in values:
            if value not in COUNTRIES_ISO_CODES:
                raise ValueError("Invalid country code " + value)

            countries_codes.add(value)

        self.value = countries_codes
