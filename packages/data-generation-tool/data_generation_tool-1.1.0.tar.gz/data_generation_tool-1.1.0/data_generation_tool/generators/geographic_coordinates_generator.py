import importlib.resources
import json

import numpy as np
from shapely import Point
from shapely.geometry import shape
from shapely.prepared import prep

from data_generation_tool.constraints.column_constraints import Unique, CoordinatesFormat, CoordinatesDecimalPrecision, \
    CountryCoordinates, ContinentCoordinates
from data_generation_tool.generators import ColumnGenerator
from data_generation_tool.requests import ColumnGenerationRequest
from data_generation_tool.types import GeographicCoordinates


class GeographicCoordinatesGenerator(ColumnGenerator):
    """
    Generator used for generating a couple of values (latitude, longitude) which express the position of a point on earth\n
    If the `ContinentCoordinates` constraint is passed with the `CountryCoordinates` constraint, only the `CountryCoordinates`
    constraint will be considered since it is more specific.
    """

    def generate(self, column: ColumnGenerationRequest, count: int) -> list:
        if column.column_type != GeographicCoordinates:
            raise ValueError(f"Column type {column.column_type} is not GeographicCoordinates")

        unique = False
        fmt = "lat , long"
        precision = 8
        continents, countries = None, None

        for constraint in column.constraints:
            if isinstance(constraint, Unique):
                unique = True
            elif isinstance(constraint, CoordinatesFormat):
                fmt = constraint.fmt
            elif isinstance(constraint, CoordinatesDecimalPrecision):
                precision = constraint.value
            elif isinstance(constraint, ContinentCoordinates):
                if countries is None:
                    continents = constraint.value
            elif isinstance(constraint, CountryCoordinates):
                countries = constraint.value
                continents = None

        if continents is None and countries is None:
            values = self._generate_raw(precision, count, fmt)
        elif countries is None:
            values = self._generate_in_continents(precision, count, fmt, continents)
        else:
            values = self._generate_in_countries(precision, count, fmt, countries)

        if unique:
            unique_elements = set(values)

            while len(unique_elements) < count:
                diff = count - len(unique_elements)
                for _ in range(diff):
                    if continents is None and countries is None:
                        unique_elements |= self._generate_raw(precision, count, fmt)
                    elif countries is None:
                        unique_elements |= self._generate_in_continents(precision, count, fmt, continents)
                    else:
                        unique_elements |= self._generate_in_countries(precision, count, fmt, countries)

            values = list(unique_elements)

        return self.post_processing(values, column.constraints)

    def _generate_raw(self, precision: int, number: int, fmt: str) -> list[str]:
        values = []
        for _ in range(number):
            lat = round(-90 + 180 * self.rng.random(), precision)
            long = round(-180 + 360 * self.rng.random(), precision)
            values.append(fmt.replace("lat", str(lat)).replace("long", str(long)))
        return values

    def _generate_in_continents(self, precision: int, number: int, fmt: str, continents: set[str]) -> list[str]:
        """
        Between all the desired continents, split randomly the total number of coordinates to generate
        Then, iterate over all continents, if a continent which belongs to the constraints is found,
        extract its bounding box and generate the required amount of positions
        """
        with importlib.resources.open_text("data_generation_tool.geojson", "world_continents.geojson") as f:
            continents_data = json.load(f)

        number_of_positions_per_continent = self._assign_random_count_to_labels(list(continents), number)
        values = []
        prepared_geometries = {
            feature['properties']['CONTINENT']: prep(shape(feature['geometry']))
            for feature in continents_data['features']
            if feature['properties']['CONTINENT'] in continents
        }

        for continent, geometry in prepared_geometries.items():
            minx, miny, maxx, maxy = geometry.context.bounds
            for _ in range(number_of_positions_per_continent[continent]):
                while True:
                    lat = round(self.rng.uniform(miny, maxy), precision)
                    long = round(self.rng.uniform(minx, maxx), precision)
                    point = Point(long, lat)

                    if geometry.contains(point):
                        values.append(fmt.replace("lat", str(lat)).replace("long", str(long)))
                        break

        return values

    def _generate_in_countries(self, precision: int, number: int, fmt: str, countries: set[str]) -> list[str]:
        """
        Between all the desired countries, split randomly the total number of coordinates to generate
        Then, iterate over all countries, if a country which belongs to the constraints is found,
        extract its bounding box and generate the required amount of positions
        """
        with importlib.resources.open_text("data_generation_tool.geojson", "world_countries.geojson") as f:
            countries_data = json.load(f)

        number_of_positions_per_country = self._assign_random_count_to_labels(list(countries), number)
        values = []
        prepared_geometries = {
            feature['properties']['iso_3166_1_alpha_2_codes']: prep(shape(feature['geometry']))
            for feature in countries_data['features']
            if feature['properties']['iso_3166_1_alpha_2_codes'] in countries
        }

        for country, geometry in prepared_geometries.items():
            minx, miny, maxx, maxy = geometry.context.bounds
            for _ in range(number_of_positions_per_country[country]):
                while True:
                    lat = round(self.rng.uniform(miny, maxy), precision)
                    long = round(self.rng.uniform(minx, maxx), precision)
                    point = Point(long, lat)

                    if geometry.contains(point):
                        values.append(fmt.replace("lat", str(lat)).replace("long", str(long)))
                        break

        return values

    def _assign_random_count_to_labels(self, labels: list[str], total_count: int) -> dict[str, int]:
        random_numbers = self.rng.random(len(labels))
        scaled_numbers = np.floor((random_numbers / random_numbers.sum()) * total_count).astype(int)
        diff = total_count - scaled_numbers.sum()

        if diff > 0:
            indices = np.argpartition(-random_numbers, diff)[:diff]
            scaled_numbers[indices] += 1

        return dict(zip(labels, scaled_numbers))
