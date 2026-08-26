class PivotField:
    def __init__(
        self,
        name,
        index,
        data_type=None,
        role=None
    ):
        self.name = name
        self.index = index
        self.data_type = data_type
        self.role = role

    def __repr__(self):
        return (
            f"PivotField("
            f"name={self.name!r}, "
            f"index={self.index}, "
            f"data_type={self.data_type!r}, "
            f"role={self.role!r}"
            f")"
        )


class DataField:
    def __init__(
        self,
        field,
        aggregation="sum",
        name=None
    ):
        self.field = field
        self.aggregation = aggregation
        self.name = (
            name
            or f"{aggregation.title()} of {field.name}"
        )

    def __repr__(self):
        return (
            f"DataField("
            f"field={self.field.name!r}, "
            f"aggregation={self.aggregation!r}, "
            f"name={self.name!r}"
            f")"
        )