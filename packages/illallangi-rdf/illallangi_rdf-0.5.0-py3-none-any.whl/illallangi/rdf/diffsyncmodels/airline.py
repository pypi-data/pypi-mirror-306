import diffsync


class Airline(
    diffsync.DiffSyncModel,
):
    _modelname = "Airline"
    _identifiers = ("iata",)
    _attributes = (
        "alliance__name",
        "dominant_color",
        "icao",
        "label",
    )

    iata: str

    alliance__name: str | None
    dominant_color: str
    icao: str | None
    label: str

    @classmethod
    def create(
        cls,
        adapter: diffsync.Adapter,
        ids: dict,
        attrs: dict,
    ) -> "Airline":
        raise NotImplementedError

    def update(
        self,
        attrs: dict,
    ) -> "Airline":
        raise NotImplementedError

    def delete(
        self,
    ) -> "Airline":
        raise NotImplementedError
