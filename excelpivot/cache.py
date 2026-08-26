from collections import OrderedDict
from .fields import PivotField


class PivotCache:
    def __init__(self, headers, records):
        self.headers = headers
        self.records = records

        self.fields = [
            PivotField(
                name=header,
                index=index
            )
            for index, header in enumerate(headers)
        ]

        self.shared_items = {}
        self.field_metadata = {}

        self._detect_types()
        self._build_shared_items()

    def _detect_types(self):
        for field in self.fields:

            values = [
                record[field.index]
                for record in self.records
                if record[field.index] is not None
            ]

            if not values:
                field.data_type = "empty"
                continue

            if all(isinstance(v, bool) for v in values):
                field.data_type = "boolean"

            elif all(
                isinstance(v, int)
                and not isinstance(v, bool)
                for v in values
            ):
                field.data_type = "integer"

            elif all(
                isinstance(v, (int, float))
                and not isinstance(v, bool)
                for v in values
            ):
                field.data_type = "number"

            else:
                field.data_type = "string"

            self.field_metadata[field.name] = {
                "min": min(values) if field.data_type in (
                    "integer",
                    "number"
                ) else None,

                "max": max(values) if field.data_type in (
                    "integer",
                    "number"
                ) else None
            }

    def _build_shared_items(self):
        for field in self.fields:

            if field.data_type not in (
                "string",
                "integer"
            ):
                continue

            values = []

            for record in self.records:
                value = record[field.index]

                if value is not None and value not in values:
                    values.append(value)

            self.shared_items[field.name] = OrderedDict(
                (value, index)
                for index, value in enumerate(values)
            )

    def get_field(self, name):
        for field in self.fields:
            if field.name == name:
                return field

        raise ValueError(
            f"Field not found: {name}"
        )

    def get_shared_index(self, field_name, value):
        return self.shared_items[field_name][value]

    def __repr__(self):
        return (
            f"PivotCache("
            f"fields={self.fields!r}, "
            f"records={len(self.records)}, "
            f"shared_items={self.shared_items!r}"
            f")"
        )