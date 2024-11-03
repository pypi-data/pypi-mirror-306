import diffsync
from partial_date import PartialDate


class Course(
    diffsync.DiffSyncModel,
):
    _modelname = "Course"
    _identifiers = ("label",)
    _attributes = (
        "country",
        "finish",
        "institution",
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
    institution: str
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
    ) -> "Course":
        raise NotImplementedError

    def update(
        self,
        attrs: dict,
    ) -> "Course":
        raise NotImplementedError

    def delete(
        self,
    ) -> "Course":
        raise NotImplementedError
