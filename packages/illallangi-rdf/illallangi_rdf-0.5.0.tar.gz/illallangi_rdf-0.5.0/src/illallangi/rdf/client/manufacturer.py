from collections.abc import Generator
from typing import Any

from illallangi.rdf.models import Manufacturer


class ManufacturerMixin:
    def get_manufacturers(
        self,
        *_args: list[Any],
        **_kwargs: dict[str, Any],
    ) -> Generator[Manufacturer, Any, list | None]:
        query = """
    SELECT
        ?label
    WHERE {{
        ?href a ic:manufacturer .
        ?href rdfs:label ?label .
    }}
    """
        for manufacturer in self.query(
            query=query,
        ):
            yield Manufacturer(
                **manufacturer,
            )
