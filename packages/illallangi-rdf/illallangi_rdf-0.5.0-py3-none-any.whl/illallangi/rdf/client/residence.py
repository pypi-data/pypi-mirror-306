from collections.abc import Generator
from typing import Any

from illallangi.rdf.models import Residence


class ResidenceMixin:
    def get_residences(
        self,
        *_args: list[Any],
        rdf_root: str,
        **_kwargs: dict[str, Any],
    ) -> Generator[Residence, Any, list | None]:
        query = f"""
SELECT ?start ?finish ?label ?street ?locality ?region ?postal_code ?country ?open_location_code WHERE {{
    <{ rdf_root }> ip:residedAt ?residedAt .
    OPTIONAL {{ ?residedAt ip:startTime ?start }} .
    OPTIONAL {{ ?residedAt ip:endTime ?finish }} .
    ?residedAt ip:atResidence ?atResidence .

    OPTIONAL {{ ?atResidence rdfs:label ?label . }}

    OPTIONAL {{ ?atResidence v:Address ?address
        OPTIONAL {{ ?address v:street-address ?street }}
        OPTIONAL {{ ?address v:locality ?locality }}
        OPTIONAL {{ ?address v:region ?region }}
        OPTIONAL {{ ?address v:postal-code ?postal_code }}
        OPTIONAL {{ ?address v:country-name ?country }}
    }}
    OPTIONAL {{ ?atResidence ip:olc ?open_location_code }} .
}}
"""

        for residence in self.query(
            query=query,
        ):
            yield Residence(
                **residence,
            )
