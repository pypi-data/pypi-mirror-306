import diffsync


class Airport(
    diffsync.DiffSyncModel,
):
    _modelname = "Airport"
    _identifiers = ("iata",)
    _attributes = (
        "icao",
        "label",
    )

    iata: str

    icao: str
    label: str

    @classmethod
    def create(
        cls,
        adapter: diffsync.Adapter,
        ids: dict,
        attrs: dict,
    ) -> "Airport":
        raise NotImplementedError

    def update(
        self,
        attrs: dict,
    ) -> "Airport":
        raise NotImplementedError

    def delete(
        self,
    ) -> "Airport":
        raise NotImplementedError
