import diffsync
from partial_date import PartialDate


class Residence(
    diffsync.DiffSyncModel,
):
    _modelname = "Residence"
    _identifiers = ("label",)
    _attributes = (
        "country",
        "finish",
        "locality",
        "open_location_code",
        "postal_code",
        "region",
        "start",
        "street",
    )

    label: str

    country: str
    finish: PartialDate | None
    locality: str
    open_location_code: str
    postal_code: str
    region: str
    start: PartialDate | None
    street: str

    @classmethod
    def create(
        cls,
        adapter: diffsync.Adapter,
        ids: dict,
        attrs: dict,
    ) -> "Residence":
        raise NotImplementedError

    def update(
        self,
        attrs: dict,
    ) -> "Residence":
        raise NotImplementedError

    def delete(
        self,
    ) -> "Residence":
        raise NotImplementedError
