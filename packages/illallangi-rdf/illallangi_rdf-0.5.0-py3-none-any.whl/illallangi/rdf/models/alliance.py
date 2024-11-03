from attrs import define, field, validators


@define(kw_only=True)
class AllianceKey:
    # Natural Keys

    name: str = field(
        validator=[
            validators.instance_of(str),
            validators.matches_re(r"^[\w ]{1,255}$"),
        ],
    )


@define(kw_only=True)
class Alliance(AllianceKey):
    pass
