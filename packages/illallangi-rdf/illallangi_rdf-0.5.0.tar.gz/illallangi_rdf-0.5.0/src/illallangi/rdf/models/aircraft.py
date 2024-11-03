from attrs import define, field, validators
from partial_date import PartialDate

from illallangi.rdf.converters.partial_date import to_partial_date
from illallangi.rdf.models.airline import AirlineKey
from illallangi.rdf.models.manufacturer import ManufacturerKey


@define(kw_only=True)
class AircraftKey:
    # Natural Keys

    manufacturer: ManufacturerKey = field(
        validator=[
            validators.instance_of(ManufacturerKey),
        ],
    )

    msn: str = field(
        validator=[
            validators.instance_of(str),
            validators.matches_re(r"^[0-9A-Za-z ]+$"),
        ],
    )


@define(kw_only=True)
class Aircraft(AircraftKey):
    # Classes

    @define(kw_only=True)
    class Named:
        @define(kw_only=True)
        class Name:
            label: str = field(
                validator=[
                    validators.instance_of(str),
                    validators.matches_re(r"^[0-9A-Za-z -]+$"),
                ],
            )

        start: PartialDate | None = field(
            converter=to_partial_date,
            default="",
            validator=[
                validators.instance_of(PartialDate | None),
            ],
        )

        finish: PartialDate | None = field(
            converter=to_partial_date,
            default="",
            validator=[
                validators.instance_of(PartialDate | None),
            ],
        )

        name: Name = field(
            validator=[
                validators.instance_of(Name),
            ],
        )

    @define(kw_only=True)
    class OperatedBy:
        @define(kw_only=True)
        class Operator:
            label: str = field(
                validator=[
                    validators.instance_of(str),
                    validators.matches_re(r"^[0-9A-Za-z -]+$"),
                ],
            )

            airline: AirlineKey = field(
                validator=[
                    validators.instance_of(AirlineKey),
                ],
            )

        start: PartialDate | None = field(
            converter=to_partial_date,
            default="",
            validator=[
                validators.instance_of(PartialDate | None),
            ],
        )

        finish: PartialDate | None = field(
            converter=to_partial_date,
            default="",
            validator=[
                validators.instance_of(PartialDate | None),
            ],
        )

        operator: Operator = field(
            validator=[
                validators.instance_of(Operator),
            ],
        )

    @define(kw_only=True)
    class RegisteredAs:
        @define(kw_only=True)
        class Registration:
            label: str = field(
                validator=[
                    validators.instance_of(str),
                    validators.matches_re(r"^[0-9A-Za-z -]+$"),
                ],
            )

        start: PartialDate | None = field(
            converter=to_partial_date,
            default="",
            validator=[
                validators.instance_of(PartialDate | None),
            ],
        )

        finish: PartialDate | None = field(
            converter=to_partial_date,
            default="",
            validator=[
                validators.instance_of(PartialDate | None),
            ],
        )

        registration: Registration = field(
            validator=[
                validators.instance_of(Registration),
            ],
        )

    @define(kw_only=True)
    class Typed:
        @define(kw_only=True)
        class Type:
            label: str = field(
                validator=[
                    validators.instance_of(str),
                    validators.matches_re(r"^[0-9A-Za-z -]+$"),
                ],
            )

        start: PartialDate | None = field(
            converter=to_partial_date,
            default="",
            validator=[
                validators.instance_of(PartialDate | None),
            ],
        )

        finish: PartialDate | None = field(
            converter=to_partial_date,
            default="",
            validator=[
                validators.instance_of(PartialDate | None),
            ],
        )

        type: Type = field(
            validator=[
                validators.instance_of(Type),
            ],
        )

    # Fields

    name: list[Named] = field(
        validator=[
            validators.instance_of(list),
        ],
    )

    operator: list[OperatedBy] = field(
        validator=[
            validators.instance_of(list),
        ],
    )

    registration: list[RegisteredAs] = field(
        validator=[
            validators.instance_of(list),
        ],
    )

    type: list[Typed] = field(
        validator=[
            validators.instance_of(list),
        ],
    )
