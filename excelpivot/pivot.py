from .fields import DataField


class PivotTable:

    def __init__(self, cache=None):
        self.source = None
        self.cache = cache

        self.rows = []
        self.columns = []
        self.filters = []
        self.values = []

    # ==================================================
    # Source
    # ==================================================

    def set_source(self, source):
        self.source = source
        return self

    # ==================================================
    # Cache
    # ==================================================

    def set_cache(self, cache):
        self.cache = cache
        return self

    # ==================================================
    # Field Resolution
    # ==================================================

    def _resolve_field(self, field):

        if isinstance(field, str):

            if self.cache is None:
                raise ValueError(
                    "A PivotCache is required "
                    "when using field names."
                )

            return self.cache.get_field(field)

        return field

    # ==================================================
    # Row Field
    # ==================================================

    def add_row(self, field):

        field = self._resolve_field(field)

        field.role = "row"

        self.rows.append(field)

        return self

    # ==================================================
    # Column Field
    # ==================================================

    def add_column(self, field):

        field = self._resolve_field(field)

        field.role = "column"

        self.columns.append(field)

        return self

    # ==================================================
    # Filter Field
    # ==================================================

    def add_filter(self, field):

        field = self._resolve_field(field)

        field.role = "filter"

        self.filters.append(field)

        return self

    # ==================================================
    # Value Field
    # ==================================================

    def add_value(
        self,
        field,
        aggregation="sum"
    ):

        field = self._resolve_field(field)

        field.role = "value"

        self.values.append(
            DataField(
                field=field,
                aggregation=aggregation
            )
        )

        return self

    # ==================================================
    # Validation
    # ==================================================

    def _validate_calculation(self):

        if self.cache is None:
            raise ValueError(
                "A PivotCache is required "
                "to calculate a PivotTable."
            )

        if len(self.rows) != 1:
            raise ValueError(
                "V1 supports exactly one "
                "row field."
            )

        if len(self.columns) != 1:
            raise ValueError(
                "V1 supports exactly one "
                "column field."
            )

        if len(self.values) != 1:
            raise ValueError(
                "V1 supports exactly one "
                "value field."
            )

    # ==================================================
    # Calculate
    # ==================================================

    def calculate(self):
        """
        Calculate the visible PivotTable.

        V1 supports:

            one row field
            one column field
            optional one filter field
            one value field

        Returns:

        {
            "headers": [...],
            "rows": [...]
        }
        """

        self._validate_calculation()

        # ----------------------------------------------
        # Cache
        # ----------------------------------------------

        cache = self.cache

        records = cache.records

        fields = cache.fields

        # ----------------------------------------------
        # Field indexes
        # ----------------------------------------------

        field_index = {
            field.name: index
            for index, field in enumerate(fields)
        }

        # ----------------------------------------------
        # Row
        # ----------------------------------------------

        row_field = self.rows[0]

        row_name = row_field.name

        row_index = field_index[
            row_name
        ]

        # ----------------------------------------------
        # Column
        # ----------------------------------------------

        column_field = self.columns[0]

        column_name = column_field.name

        column_index = field_index[
            column_name
        ]

        # ----------------------------------------------
        # Value
        # ----------------------------------------------

        data_field = self.values[0]

        value_field = data_field.field

        value_name = value_field.name

        value_index = field_index[
            value_name
        ]

        aggregation = (
            data_field.aggregation
        )

        # ----------------------------------------------
        # Filter
        # ----------------------------------------------

        # filtered_records = list(records)

        # if self.filters:

        #     filter_field = self.filters[0]

        #     filter_name = filter_field.name

        #     filter_index = field_index[
        #         filter_name
        #     ]

        #     filter_values = sorted(
        #         {
        #             record[filter_index]
        #             for record in records
        #         }
        #     )

        #     if filter_values:

        #         # V1:
        #         # use the first available value.
        #         #
        #         # Later this becomes a real
        #         # PivotTable filter selection.

        #         selected_value = (
        #             filter_values[0]
        #         )

        #         filtered_records = [
        #             record
        #             for record in records
        #             if record[filter_index]
        #             == selected_value
        #         ]
        filtered_records = list(records)

        # ----------------------------------------------
        # Row values
        # ----------------------------------------------

        row_values = sorted(
            {
                record[row_index]
                for record in filtered_records
            }
        )

        # ----------------------------------------------
        # Column values
        # ----------------------------------------------

        column_values = sorted(
            {
                record[column_index]
                for record in filtered_records
            }
        )

        # ----------------------------------------------
        # Matrix
        # ----------------------------------------------

        matrix = {}

        for row_value in row_values:

            matrix[row_value] = {}

            for column_value in column_values:

                matching_values = []

                for record in filtered_records:

                    if (
                        record[row_index]
                        == row_value
                        and
                        record[column_index]
                        == column_value
                    ):

                        value = record[
                            value_index
                        ]

                        if value is not None:

                            matching_values.append(
                                value
                            )

                result = self._aggregate(
                    matching_values,
                    aggregation
                )

                matrix[
                    row_value
                ][
                    column_value
                ] = result

        # ----------------------------------------------
        # Headers
        # ----------------------------------------------

        headers = [
            row_name,
            *column_values,
            "Grand Total"
        ]

        # ----------------------------------------------
        # Output rows
        # ----------------------------------------------

        output_rows = []

        for row_value in row_values:

            row = [
                row_value
            ]

            row_total = 0

            for column_value in column_values:

                value = matrix[
                    row_value
                ][
                    column_value
                ]

                row.append(value)

                row_total += value

            row.append(
                row_total
            )

            output_rows.append(
                row
            )

        # ----------------------------------------------
        # Grand Total
        # ----------------------------------------------

        grand_total = [
            "Grand Total"
        ]

        overall_total = 0

        for column_value in column_values:

            column_total = sum(
                matrix[
                    row_value
                ][
                    column_value
                ]
                for row_value in row_values
            )

            grand_total.append(
                column_total
            )

            overall_total += column_total

        grand_total.append(
            overall_total
        )

        output_rows.append(
            grand_total
        )

        return {
            "headers": headers,
            "rows": output_rows
        }

    # ==================================================
    # Aggregation
    # ==================================================

    @staticmethod
    def _aggregate(
        values,
        aggregation
    ):

        if not values:

            return 0

        aggregation = aggregation.lower()

        if aggregation == "sum":

            return sum(values)

        if aggregation == "count":

            return len(values)

        if aggregation == "average":

            return sum(values) / len(values)

        if aggregation == "min":

            return min(values)

        if aggregation == "max":

            return max(values)

        raise ValueError(
            f"Unsupported aggregation: "
            f"{aggregation}"
        )

    # ==================================================
    # Result
    # ==================================================

    def result(self):

        return self.calculate()

    # ==================================================
    # Representation
    # ==================================================

    def __repr__(self):

        return (
            f"PivotTable("
            f"source={self.source!r}, "
            f"rows={self.rows!r}, "
            f"columns={self.columns!r}, "
            f"filters={self.filters!r}, "
            f"values={self.values!r}"
            f")"
        )