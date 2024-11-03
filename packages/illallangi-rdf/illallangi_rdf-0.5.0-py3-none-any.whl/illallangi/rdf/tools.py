from typing import Any

import click
import orjson
import tabulate
from cattrs import unstructure
from dotenv import load_dotenv
from partial_date import PartialDate

from illallangi.rdf.__version__ import __version__
from illallangi.rdf.client import RDFClient

load_dotenv(
    override=True,
)

airline_iata_argument = click.argument(
    "airline_iata",
    nargs=-1,
    required=True,
    type=click.STRING,
)

airport_iata_argument = click.argument(
    "airport_iata",
    nargs=-1,
    required=True,
    type=click.STRING,
)

github_file_path_option = click.option(
    "--github-file-path",
    required=True,
    help="The path to the file in the repository.",
    envvar="RDF_GITHUB_FILE_PATH",
)

github_repo_name_option = click.option(
    "--github-repo-name",
    required=True,
    help="The name of the repository.",
    envvar="RDF_GITHUB_REPO_NAME",
)

github_repo_owner_option = click.option(
    "--github-repo-owner",
    required=True,
    help="The owner of the repository.",
    envvar="RDF_GITHUB_REPO_OWNER",
)

github_token_option = click.option(
    "--github-token",
    required=True,
    help="The GitHub personal access token.",
    envvar="RDF_GITHUB_TOKEN",
)

json_output_format_option = click.option(
    "--json",
    "output_format",
    flag_value="json",
    help="Output as JSON.",
)

rdf_root_option = click.option(
    "--rdf-root",
    required=True,
    help="The root URL of the RDF object.",
    envvar="RDF_ROOT",
)

table_output_format_option = click.option(
    "--table",
    "output_format",
    flag_value="table",
    default=True,
    help="Output as a table (default).",
)

version_option = click.version_option(
    version=__version__,
    prog_name="rdf-tools",
)


@click.group()
@click.pass_context
@github_file_path_option
@github_repo_name_option
@github_repo_owner_option
@github_token_option
@version_option
def cli(
    ctx: click.Context,
    *args: list,
    **kwargs: dict,
) -> None:
    ctx.obj = RDFClient(
        *args,
        **kwargs,
    )


@cli.command()
@click.pass_context
@json_output_format_option
@table_output_format_option
def aircraft(
    ctx: click.Context,
    *args: list,
    **kwargs: dict,
) -> None:
    output(
        *args,
        fn=ctx.obj.get_aircraft,
        **kwargs,
    )


@cli.command()
@click.pass_context
@airline_iata_argument
@json_output_format_option
@table_output_format_option
def airlines(
    ctx: click.Context,
    *args: list,
    **kwargs: dict,
) -> None:
    output(
        *args,
        fn=ctx.obj.get_airlines,
        **kwargs,
    )


@cli.command()
@click.pass_context
@airport_iata_argument
@json_output_format_option
@table_output_format_option
def airports(
    ctx: click.Context,
    *args: list,
    **kwargs: dict,
) -> None:
    output(
        *args,
        fn=ctx.obj.get_airports,
        **kwargs,
    )


@cli.command()
@click.pass_context
@json_output_format_option
@rdf_root_option
@table_output_format_option
def courses(
    ctx: click.Context,
    *args: list,
    **kwargs: dict,
) -> None:
    output(
        *args,
        fn=ctx.obj.get_courses,
        **kwargs,
    )


@cli.command()
@click.pass_context
@json_output_format_option
@table_output_format_option
def manufacturers(
    ctx: click.Context,
    *args: list,
    **kwargs: dict,
) -> None:
    output(
        *args,
        fn=ctx.obj.get_manufacturers,
        **kwargs,
    )


@cli.command()
@click.pass_context
@json_output_format_option
@rdf_root_option
@table_output_format_option
def residences(
    ctx: click.Context,
    *args: list,
    **kwargs: dict,
) -> None:
    output(
        *args,
        fn=ctx.obj.get_residences,
        **kwargs,
    )


def output(
    fn: callable,
    *args: list,
    output_format: str,
    **kwargs: dict,
) -> None:
    objs = fn(
        *args,
        **kwargs,
    )

    if not objs:
        return

    # JSON output
    if output_format in [
        "json",
    ]:

        def default(
            obj: Any,  # noqa: ANN401
        ) -> str:
            if isinstance(obj, PartialDate):
                return str(obj)
            raise TypeError

        click.echo(
            orjson.dumps(
                [{k: v for k, v in unstructure(obj).items() if v} for obj in objs],
                option=orjson.OPT_SORT_KEYS,
                default=default,
            ),
        )
        return

    # Table output
    if output_format in [
        "table",
    ]:
        click.echo(
            tabulate.tabulate(
                [{k: v for k, v in unstructure(obj).items() if v} for obj in objs],
                headers="keys",
                tablefmt="presto",
                numalign="left",
                stralign="left",
            )
        )
        return

    raise NotImplementedError
