from excelpivot.source import ExcelSource
from excelpivot.cache import PivotCache
from excelpivot.pivot import PivotTable


def build_pivot():

    source = ExcelSource(
        "reference/v1_simple.xlsx"
    )

    headers, records = source.read_table(
        "Table1"
    )

    cache = PivotCache(
        headers,
        records
    )

    pivot = PivotTable(
        cache
    )

    pivot.set_source(
        "Table1"
    )

    pivot.add_row(
        "Region"
    )

    pivot.add_column(
        "Product"
    )

    pivot.add_filter(
        "Year"
    )

    pivot.add_value(
        "Revenue",
        "sum"
    )

    return pivot


def test_calculate():

    pivot = build_pivot()

    result = pivot.calculate()

    assert "headers" in result

    assert "rows" in result

    assert len(
        result["headers"]
    ) == 5


def test_calculate_headers():

    pivot = build_pivot()

    result = pivot.calculate()

    assert result["headers"] == [
        "Region",
        "Laptop",
        "Phone",
        "Tablet",
        "Grand Total"
    ]