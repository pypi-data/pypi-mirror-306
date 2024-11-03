from collections.abc import Generator
from typing import Any

from illallangi.rdf.models import Course


class CourseMixin:
    def get_courses(
        self,
        *_args: list[Any],
        rdf_root: str,
        **_kwargs: dict[str, Any],
    ) -> Generator[Course, Any, list | None]:
        query = f"""
SELECT ?start ?finish ?label ?institution ?street ?locality ?region ?postal_code ?country ?open_location_code WHERE {{
    <{ rdf_root }> ip:attendedCourse ?attended_course .
    OPTIONAL {{ ?attended_course ip:startTime ?start }} .
    OPTIONAL {{ ?attended_course ip:endTime ?finish }} .
    ?attended_course rdfs:label ?label .
    ?attended_course ip:atInstitution ?at_institution .

    OPTIONAL {{ ?at_institution rdfs:label ?institution . }}

    OPTIONAL {{ ?at_institution v:Address ?address
        OPTIONAL {{ ?address v:street-address ?street }}
        OPTIONAL {{ ?address v:locality ?locality }}
        OPTIONAL {{ ?address v:region ?region }}
        OPTIONAL {{ ?address v:postal-code ?postal_code }}
        OPTIONAL {{ ?address v:country-name ?country }}
    }}
    OPTIONAL {{ ?at_institution ip:olc ?open_location_code }} .
}}
"""

        for course in self.query(
            query=query,
        ):
            yield Course(
                **course,
            )
