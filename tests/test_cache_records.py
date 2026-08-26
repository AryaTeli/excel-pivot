from excelpivot.source import ExcelSource
from excelpivot.cache import PivotCache
from excelpivot.pivot import PivotTable

from excelpivot.ooxml.cache_records import (
    generate_cache_records,
    cache_records_xml
)


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
        cache=cache
    )

    pivot.set_source("Table1")

    pivot.add_row("Region")
    pivot.add_column("Product")
    pivot.add_filter("Year")
    pivot.add_value("Revenue", "sum")

    cache.build_dimension_shared_items(pivot)

    return cache, pivot


def test_record_count():

    cache, pivot = build_pivot()

    root = generate_cache_records(
        cache,
        pivot
    )

    assert root.attrib["count"] == "10"

    records = list(root)

    assert len(records) == 10


def test_first_record():

    cache, pivot = build_pivot()

    root = generate_cache_records(
        cache,
        pivot
    )

    first_record = list(root)[0]

    values = [
        (
            element.tag.split("}")[-1],
            element.attrib.get("v")
        )
        for element in first_record
    ]

    assert values == [
        ("x", "0"),
        ("x", "0"),
        ("x", "0"),
        ("n", "10000"),
        ("n", "10"),
    ]


def test_second_record():

    cache, pivot = build_pivot()

    root = generate_cache_records(
        cache,
        pivot
    )

    second_record = list(root)[1]

    values = [
        (
            element.tag.split("}")[-1],
            element.attrib.get("v")
        )
        for element in second_record
    ]

    assert values == [
        ("x", "0"),
        ("x", "1"),
        ("x", "0"),
        ("n", "5000"),
        ("n", "5"),
    ]


def test_serialization():

    cache, pivot = build_pivot()

    xml = cache_records_xml(
        cache,
        pivot
    )

    assert xml.startswith(
        b"<?xml"
    )

    assert (
        b"pivotCacheRecords"
        in xml
    )

    assert (
        b'count="10"'
        in xml
    )