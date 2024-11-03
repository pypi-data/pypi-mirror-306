from collections.abc import Generator
from typing import Any

from illallangi.rdf.models import Airport


class AirportsNotFoundError(Exception):
    def __init__(
        self,
        airport_iata: list[str],
    ) -> None:
        self.airport_iata = airport_iata
        msg = f"Airport(s) not found: {', '.join(airport_iata)}"
        super().__init__(msg)


class AirportMixin:
    def get_airports(
        self,
        *_args: list[Any],
        airport_iata: list[str] | None = None,
        **_kwargs: dict[str, Any],
    ) -> Generator[Airport, Any, list | None]:
        if airport_iata is None:
            return []
        airport_iata = [i.upper() for i in airport_iata]

        query = f"""
SELECT ?label ?iata ?icao WHERE {{
    VALUES (?value) {{ ( "{'" ) ( "'.join(airport_iata)}" ) }}
    ?href ip:airportIataCode ?value.
    ?href rdfs:label ?label .
    ?href ip:airportIataCode ?iata .
    ?href ip:airportIcaoCode ?icao .
    ?href a ic:airport .
}}
"""

        found = []

        for airport in self.query(
            query=query,
        ):
            found.append(airport["iata"])
            yield Airport(
                **airport,
            )

        not_found = [i for i in airport_iata if i not in found]
        if not_found:
            raise AirportsNotFoundError(not_found)
