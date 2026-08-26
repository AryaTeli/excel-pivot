from excelpivot.source import ExcelSource
from excelpivot.cache import PivotCache


def build_cache():

    source = ExcelSource(
        "reference/v1_simple.xlsx"
    )

    headers, records = source.read_table("Table1")

    return PivotCache(
        headers,
        records
    )


def test_field_types():

    cache = build_cache()

    assert cache.get_field("Region").data_type == "string"

    assert cache.get_field("Product").data_type == "string"

    assert cache.get_field("Year").data_type == "integer"

    assert cache.get_field("Revenue").data_type == "integer"

    assert cache.get_field("Quantity").data_type == "integer"


def test_numeric_metadata():

    cache = build_cache()

    revenue = cache.field_metadata["Revenue"]

    assert revenue["min"] == 4000
    assert revenue["max"] == 11000

    quantity = cache.field_metadata["Quantity"]

    assert quantity["min"] == 4
    assert quantity["max"] == 11

    year = cache.field_metadata["Year"]

    assert year["min"] == 2025
    assert year["max"] == 2026


def test_shared_items():

    cache = build_cache()

    assert list(
        cache.shared_items["Region"].keys()
    ) == [
        "North",
        "South",
        "West",
        "East"
    ]

    assert list(
        cache.shared_items["Product"].keys()
    ) == [
        "Laptop",
        "Phone",
        "Tablet"
    ]

    assert list(
        cache.shared_items["Year"].keys()
    ) == [
        2025,
        2026
    ]


def test_shared_indexes():

    cache = build_cache()

    assert cache.get_shared_index(
        "Region",
        "North"
    ) == 0

    assert cache.get_shared_index(
        "Region",
        "South"
    ) == 1

    assert cache.get_shared_index(
        "Product",
        "Laptop"
    ) == 0

    assert cache.get_shared_index(
        "Product",
        "Phone"
    ) == 1

    assert cache.get_shared_index(
        "Year",
        2025
    ) == 0

    assert cache.get_shared_index(
        "Year",
        2026
    ) == 1