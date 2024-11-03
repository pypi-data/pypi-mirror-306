from typing import ClassVar

import diffsync
from cattrs import global_converter, structure, unstructure

from illallangi.rdf import RDFClient
from illallangi.rdf.diffsyncmodels import Residence


@global_converter.register_structure_hook
def trip_structure_hook(
    value: dict,
    type: type,  # noqa: A002, ARG001
) -> Residence:
    return Residence(
        **value,
    )


class ResidentialAdapter(diffsync.Adapter):
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

    Residence = Residence

    top_level: ClassVar = [
        "Residence",
    ]

    type = "rdf_residential"

    def load(
        self,
        *args: list,
        **kwargs: dict,
    ) -> None:
        for obj in self.client.get_residences(
            *args,
            **kwargs,
        ):
            d = unstructure(
                obj,
            )
            o = structure(
                d,
                Residence,
            )
            self.add(
                o,
            )
