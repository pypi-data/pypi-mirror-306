from attrs import define, field, validators

from illallangi.rdf.models.alliance import Alliance


@define(kw_only=True)
class AirlineKey:
    # Natural Keys

    iata: str = field(
        validator=[
            validators.instance_of(str),
            validators.matches_re(r"^[0-9A-Z]{2}$"),
        ],
    )


@define(kw_only=True)
class Airline(AirlineKey):
    # Fields

    alliance: Alliance | None = field(
        validator=[
            validators.instance_of(Alliance | None),
        ],
    )

    dominant_color: str = field(
        validator=[
            validators.instance_of(str),
            validators.matches_re(r"^#[0-9a-f]{6}$"),
        ],
    )

    icao: str | None = field(
        default=None,
        validator=[
            validators.instance_of(str | None),
            # validators.matches_re(r"^[0-9A-Z]{3}$"),
        ],
    )

    label: str = field(
        validator=[
            validators.instance_of(str),
        ],
    )
