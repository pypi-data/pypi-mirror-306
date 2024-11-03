from attrs import define, field, validators


@define(kw_only=True)
class ManufacturerKey:
    # Natural Keys

    label: str = field(
        validator=[
            validators.instance_of(str),
            validators.matches_re(r"^[0-9A-Za-z -]+$"),
        ],
    )


@define(kw_only=True)
class Manufacturer(ManufacturerKey):
    pass
