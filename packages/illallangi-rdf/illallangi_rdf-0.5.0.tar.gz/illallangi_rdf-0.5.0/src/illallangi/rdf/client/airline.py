from collections.abc import Generator
from typing import Any

from illallangi.rdf.models import Airline, Alliance


class AirlinesNotFoundError(Exception):
    def __init__(
        self,
        airline_iata: list[str],
    ) -> None:
        self.airline_iata = airline_iata
        msg = f"Airline(s) not found: {', '.join(airline_iata)}"
        super().__init__(msg)


class AirlineMixin:
    def get_airlines(
        self,
        *_args: list[Any],
        airline_iata: list[str] | None = None,
        **_kwargs: dict[str, Any],
    ) -> Generator[Airline, Any, list | None]:
        if airline_iata is None:
            return []
        airline_iata = [i.upper() for i in airline_iata]

        query = f"""
    SELECT ?label ?iata ?icao ?alliance ?dominant_color WHERE {{
        VALUES (?value) {{ ( "{'" ) ( "'.join(airline_iata)}" ) }}
        ?href ip:airlineIataCode ?value.
        ?href rdfs:label ?label .
        ?href ip:airlineIataCode ?iata .
        OPTIONAL {{ ?href ip:airlineIcaoCode ?icao . }}
        OPTIONAL {{
            ?href ip:memberOfAirlineAlliance ?allianceHref .
            ?allianceHref rdfs:label ?alliance .
        }}
        OPTIONAL {{ ?href ip:dominantColor ?dominant_color . }}
        ?href a ic:airline .
    }}
    """

        found = []

        for airline in self.query(
            query=query,
        ):
            found.append(airline["iata"])
            yield Airline(
                **{
                    **airline,
                    "alliance": Alliance(name=str(airline["alliance"]))
                    if "alliance" in airline
                    else None,
                },
            )

        not_found = [i for i in airline_iata if i not in found]
        if not_found:
            raise AirlinesNotFoundError(not_found)
