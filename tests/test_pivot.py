from excelpivot import PivotTable, PivotCache


def create_cache():

    headers = [
        "Region",
        "Product",
        "Year",
        "Revenue",
        "Quantity"
    ]

    records = [
        ("North", "Laptop", 2025, 10000, 10),
        ("South", "Phone", 2026, 7000, 7),
    ]

    return PivotCache(
        headers,
        records
    )


def test_pivot_model():

    cache = create_cache()

    pivot = PivotTable(
        cache=cache
    )

    pivot.set_source("Table1")

    pivot.add_row("Region")
    pivot.add_column("Product")
    pivot.add_filter("Year")
    pivot.add_value("Revenue", "sum")

    assert pivot.source == "Table1"

    assert pivot.rows[0].name == "Region"

    assert pivot.columns[0].name == "Product"

    assert pivot.filters[0].name == "Year"

    assert pivot.values[0].field.name == "Revenue"

    assert pivot.values[0].aggregation == "sum"


def test_field_roles():

    cache = create_cache()

    pivot = PivotTable(
        cache=cache
    )

    pivot.add_row("Region")
    pivot.add_column("Product")
    pivot.add_filter("Year")
    pivot.add_value("Revenue", "sum")

    assert cache.get_field(
        "Region"
    ).role == "row"

    assert cache.get_field(
        "Product"
    ).role == "column"

    assert cache.get_field(
        "Year"
    ).role == "filter"

    assert cache.get_field(
        "Revenue"
    ).role == "value"