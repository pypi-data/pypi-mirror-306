from collections.abc import Generator
from typing import Any

from illallangi.rdf.models import (
    Aircraft,
    AirlineKey,
    ManufacturerKey,
)


class AircraftMixin:
    def get_aircraft(
        self,
        *_args: list[Any],
        **_kwargs: dict[str, Any],
    ) -> Generator[Aircraft, Any, list | None]:
        query = """
    PREFIX ic: <http://data.coley.au/rdf/class#>
    PREFIX ip: <http://data.coley.au/rdf/property#>
    SELECT
        ?manufacturer__label
        ?msn
    WHERE {{
        ?href a ic:aircraft .
        ?href ip:aircraftManufacturer [
            rdfs:label ?manufacturer__label ;
        ] .
        ?href ip:aircraftMsn ?msn .
    }}
    """
        for aircraft in self.query(
            query=query,
        ):
            yield Aircraft(
                **{
                    **{k: v for k, v in aircraft.items() if "__" not in k},
                    "manufacturer": ManufacturerKey(
                        label=str(aircraft["manufacturer__label"])
                    ),
                    "name": list(
                        self.get_aircraft_named(
                            **aircraft,
                        ),
                    ),
                    "operator": list(
                        self.get_aircraft_operated_by(
                            **aircraft,
                        ),
                    ),
                    "registration": list(
                        self.get_aircraft_registered_as(
                            **aircraft,
                        ),
                    ),
                    "type": list(
                        self.get_aircraft_typed_as(
                            **aircraft,
                        ),
                    ),
                },
            )

    def get_aircraft_named(
        self,
        *_args: list[Any],
        msn: str,
        manufacturer__label: str,
        **_kwargs: dict[str, Any],
    ) -> Generator[str, Any, list | None]:
        query = f"""
    PREFIX ic: <http://data.coley.au/rdf/class#>
    PREFIX ip: <http://data.coley.au/rdf/property#>
    PREFIX schema: <http://schema.org/>
    SELECT
        ?coverage
        ?aircraft_name__label
    WHERE {{
        ?href a ic:aircraft .
        ?href ip:aircraftMsn {msn} .
        ?href ip:aircraftManufacturer [
            rdfs:label "{manufacturer__label}" ;
        ] .
        ?href ip:aircraftNamed [
            ip:aircraftName [
                rdfs:label ?aircraft_name__label ;
            ] ;
            schema:temporalCoverage ?coverage ;
        ] .
    }}
    """
        for aircraft_name in self.query(
            query=query,
        ):
            yield Aircraft.Named(
                start=aircraft_name["coverage"].split("/")[0],
                finish=aircraft_name["coverage"].split("/")[1]
                if "/" in aircraft_name["coverage"]
                else None,
                name=Aircraft.Named.Name(
                    label=aircraft_name["aircraft_name__label"],
                ),
            )

    def get_aircraft_operated_by(
        self,
        *_args: list[Any],
        msn: str,
        manufacturer__label: str,
        **_kwargs: dict[str, Any],
    ) -> Generator[str, Any, list | None]:
        query = f"""
    PREFIX ic: <http://data.coley.au/rdf/class#>
    PREFIX ip: <http://data.coley.au/rdf/property#>
    PREFIX schema: <http://schema.org/>
    SELECT
        ?coverage
        ?aircraft_operator__label
        ?aircraft_operator__iata_code
    WHERE {{
        ?href a ic:aircraft .
        ?href ip:aircraftMsn {msn} .
        ?href ip:aircraftManufacturer [
            rdfs:label "{manufacturer__label}" ;
        ] .
        ?href ip:aircraftOperatedBy [
            ip:aircraftOperator [
                rdfs:label ?aircraft_operator__label ;
                ip:airline [
                    ip:airlineIataCode ?aircraft_operator__iata_code ;
                ] ;
            ] ;
            schema:temporalCoverage ?coverage ;
        ] .
    }}
    """
        for aircraft_operator in self.query(
            query=query,
        ):
            yield Aircraft.OperatedBy(
                start=aircraft_operator["coverage"].split("/")[0],
                finish=aircraft_operator["coverage"].split("/")[1]
                if "/" in aircraft_operator["coverage"]
                else None,
                operator=Aircraft.OperatedBy.Operator(
                    label=aircraft_operator["aircraft_operator__label"],
                    airline=AirlineKey(
                        iata=str(aircraft_operator["aircraft_operator__iata_code"]),
                    ),
                ),
            )

    def get_aircraft_registered_as(
        self,
        *_args: list[Any],
        msn: str,
        manufacturer__label: str,
        **_kwargs: dict[str, Any],
    ) -> Generator[str, Any, list | None]:
        query = f"""
    PREFIX ic: <http://data.coley.au/rdf/class#>
    PREFIX ip: <http://data.coley.au/rdf/property#>
    PREFIX schema: <http://schema.org/>
    SELECT
        ?coverage
        ?aircraft_registration__label
    WHERE {{
        ?href a ic:aircraft .
        ?href ip:aircraftMsn {msn} .
        ?href ip:aircraftManufacturer [
            rdfs:label "{manufacturer__label}" ;
        ] .
        ?href ip:aircraftRegisteredAs [
            ip:aircraftRegistration [
                rdfs:label ?aircraft_registration__label ;
            ] ;
            schema:temporalCoverage ?coverage ;
        ] .
    }}
    """
        for aircraft_registration in self.query(
            query=query,
        ):
            yield Aircraft.RegisteredAs(
                start=aircraft_registration["coverage"].split("/")[0],
                finish=aircraft_registration["coverage"].split("/")[1]
                if "/" in aircraft_registration["coverage"]
                else None,
                registration=Aircraft.RegisteredAs.Registration(
                    label=aircraft_registration["aircraft_registration__label"],
                ),
            )

    def get_aircraft_typed_as(
        self,
        *_args: list[Any],
        msn: str,
        manufacturer__label: str,
        **_kwargs: dict[str, Any],
    ) -> Generator[str, Any, list | None]:
        query = f"""
    PREFIX ic: <http://data.coley.au/rdf/class#>
    PREFIX ip: <http://data.coley.au/rdf/property#>
    PREFIX schema: <http://schema.org/>
    SELECT
        ?coverage
        ?aircraft_type__label
    WHERE {{
        ?href a ic:aircraft .
        ?href ip:aircraftMsn {msn} .
        ?href ip:aircraftManufacturer [
            rdfs:label "{manufacturer__label}" ;
        ] .
        ?href ip:aircraftTypedAs [
            ip:aircraftType [
                rdfs:label ?aircraft_type__label ;
            ] ;
            schema:temporalCoverage ?coverage ;
        ] .
    }}
    """
        for aircraft_type in self.query(
            query=query,
        ):
            yield Aircraft.Typed(
                start=aircraft_type["coverage"].split("/")[0],
                finish=aircraft_type["coverage"].split("/")[1]
                if "/" in aircraft_type["coverage"]
                else None,
                type=Aircraft.Typed.Type(
                    label=aircraft_type["aircraft_type__label"],
                ),
            )
