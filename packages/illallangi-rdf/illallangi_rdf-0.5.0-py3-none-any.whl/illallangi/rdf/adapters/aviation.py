from typing import ClassVar

import diffsync
from cattrs import global_converter, structure, unstructure

from illallangi.rdf import RDFClient
from illallangi.rdf.diffsyncmodels import Airline, Airport


@global_converter.register_structure_hook
def airline_structure_hook(
    value: dict,
    type: type,  # noqa: A002, ARG001
) -> Airline:
    return Airline(
        alliance__name=value["alliance"]["name"]
        if "alliance" in value and value["alliance"] is not None
        else None,
        **value,
    )


@global_converter.register_structure_hook
def airport_structure_hook(
    value: dict,
    type: type,  # noqa: A002, ARG001
) -> Airport:
    return Airport(
        **value,
    )


class AviationAdapter(diffsync.Adapter):
    def __init__(
        self,
        *args: list,
        **kwargs: dict,
    ) -> None:
        super().__init__()
        self.client = RDFClient(
            *args,
            **kwargs,
        )

    Airline = Airline
    Airport = Airport

    top_level: ClassVar = [
        "Airline",
        "Airport",
    ]

    type = "rdf_aviation"

    def load(
        self,
        *args: list,
        **kwargs: dict,
    ) -> None:
        for obj in self.client.get_airlines(
            *args,
            **kwargs,
        ):
            d = unstructure(
                obj,
            )
            o = structure(
                d,
                Airline,
            )
            self.add(
                o,
            )

        for obj in self.client.get_airports(
            *args,
            **kwargs,
        ):
            d = unstructure(
                obj,
            )
            o = structure(
                d,
                Airport,
            )
            self.add(
                o,
            )
