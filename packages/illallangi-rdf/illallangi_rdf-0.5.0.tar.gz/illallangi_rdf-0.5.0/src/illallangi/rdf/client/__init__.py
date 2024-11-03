from collections.abc import Generator
from functools import cached_property
from typing import Any

import rdflib
import requests

from illallangi.rdf.client.aircraft import AircraftMixin
from illallangi.rdf.client.airline import AirlineMixin
from illallangi.rdf.client.airport import AirportMixin
from illallangi.rdf.client.course import CourseMixin
from illallangi.rdf.client.manufacturer import ManufacturerMixin
from illallangi.rdf.client.residence import ResidenceMixin


class RDFClient(
    AircraftMixin,
    AirlineMixin,
    AirportMixin,
    CourseMixin,
    ManufacturerMixin,
    ResidenceMixin,
):
    def __init__(
        self,
        github_file_path: str,
        github_repo_name: str,
        github_repo_owner: str,
        github_token: str,
    ) -> None:
        self.github_file_path = github_file_path
        self.github_repo_name = github_repo_name
        self.github_repo_owner = github_repo_owner
        self.github_token = github_token

    @cached_property
    def graph(self) -> rdflib.Graph:
        url = f"https://api.github.com/repos/{self.github_repo_owner}/{self.github_repo_name}/contents/{self.github_file_path}"
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3.raw",
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=5,
        )

        response.raise_for_status()

        return rdflib.Graph().parse(data=response.content)

    def query(
        self,
        query: str,
    ) -> Generator[dict[str, str | None], Any, None]:
        results = self.graph.query(
            query,
        )

        for result in results.bindings:
            yield {
                k: v
                for k, v in {
                    str(key): str(result[str(key)]) if str(key) in result else None
                    for key in results.vars
                }.items()
                if v is not None and v not in ["", "None"]
            }
