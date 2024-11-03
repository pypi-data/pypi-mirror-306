from typing import ClassVar

import diffsync
from cattrs import global_converter, structure, unstructure

from illallangi.rdf import RDFClient
from illallangi.rdf.diffsyncmodels import Course


@global_converter.register_structure_hook
def trip_structure_hook(
    value: dict,
    type: type,  # noqa: A002, ARG001
) -> Course:
    return Course(
        **value,
    )


class EducationAdapter(diffsync.Adapter):
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

    Course = Course

    top_level: ClassVar = [
        "Course",
    ]

    type = "rdf_education"

    def load(
        self,
        *args: list,
        **kwargs: dict,
    ) -> None:
        for obj in self.client.get_courses(
            *args,
            **kwargs,
        ):
            d = unstructure(
                obj,
            )
            o = structure(
                d,
                Course,
            )
            self.add(
                o,
            )
