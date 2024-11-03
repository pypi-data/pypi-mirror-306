from attrs import define, field, validators
from partial_date import PartialDate

from illallangi.rdf.converters.partial_date import to_partial_date


@define(kw_only=True)
class ResidenceKey:
    # Natural Keys

    label: str = field(
        validator=[
            validators.instance_of(str),
            validators.matches_re(r"^[\w ]{1,63}$"),
        ],
    )


@define(kw_only=True)
class Residence(ResidenceKey):
    country: str = field(
        validator=[
            validators.instance_of(str),
            validators.matches_re(r"^[\w ]{1,63}$"),
        ],
    )

    finish: PartialDate | None = field(
        converter=to_partial_date,
        default="",
        validator=[
            validators.instance_of(PartialDate | None),
        ],
    )

    locality: str = field(
        validator=[
            validators.instance_of(str),
            validators.matches_re(r"^[\w ]{1,63}$"),
        ],
    )

    open_location_code: str = field(
        validator=[
            validators.instance_of(str),
            validators.matches_re(
                r"^[23456789CFGHJMPQRVWX]{8}\+[23456789CFGHJMPQRVWX]{2,}$"
            ),
        ],
    )

    postal_code: str = field(
        validator=[
            validators.instance_of(str),
            validators.matches_re(r"^\d{4}$"),
        ],
    )

    region: str = field(
        validator=[
            validators.instance_of(str),
            validators.matches_re(r"^[\w ]{1,63}$"),
        ],
    )

    start: PartialDate | None = field(
        converter=to_partial_date,
        default="",
        validator=[
            validators.instance_of(PartialDate | None),
        ],
    )

    street: str = field(
        validator=[
            validators.instance_of(str),
            validators.matches_re(r"^[\w /,]{1,63}$"),
        ],
    )
