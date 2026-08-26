from excelpivot.source import ExcelSource
from excelpivot.cache import PivotCache
from excelpivot.pivot import PivotTable

from excelpivot.ooxml.pivot_table import (
    generate_pivot_table_definition,
    pivot_table_definition_xml
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
    pivot.add_value(
        "Revenue",
        "sum"
    )

    cache.build_dimension_shared_items(pivot)

    return cache, pivot


def test_pivot_root():

    cache, pivot = build_pivot()

    root = generate_pivot_table_definition(
        cache,
        pivot
    )

    assert root.tag.endswith(
        "pivotTableDefinition"
    )

    assert root.attrib["name"] == "PivotTable1"

    assert root.attrib["cacheId"] == "5"


def test_row_fields():

    cache, pivot = build_pivot()

    root = generate_pivot_table_definition(
        cache,
        pivot
    )

    ns = (
        "{http://schemas.openxmlformats.org/"
        "spreadsheetml/2006/main}"
    )

    row_fields = root.find(
        ns + "rowFields"
    )

    assert row_fields.attrib[
        "count"
    ] == "1"

    assert row_fields[0].attrib[
        "x"
    ] == "0"


def test_column_fields():

    cache, pivot = build_pivot()

    root = generate_pivot_table_definition(
        cache,
        pivot
    )

    ns = (
        "{http://schemas.openxmlformats.org/"
        "spreadsheetml/2006/main}"
    )

    col_fields = root.find(
        ns + "colFields"
    )

    assert col_fields.attrib[
        "count"
    ] == "1"

    assert col_fields[0].attrib[
        "x"
    ] == "1"


def test_filter():

    cache, pivot = build_pivot()

    root = generate_pivot_table_definition(
        cache,
        pivot
    )

    ns = (
        "{http://schemas.openxmlformats.org/"
        "spreadsheetml/2006/main}"
    )

    page_fields = root.find(
        ns + "pageFields"
    )

    assert page_fields.attrib[
        "count"
    ] == "1"

    assert page_fields[0].attrib[
        "fld"
    ] == "2"


def test_data_field():

    cache, pivot = build_pivot()

    root = generate_pivot_table_definition(
        cache,
        pivot
    )

    ns = (
        "{http://schemas.openxmlformats.org/"
        "spreadsheetml/2006/main}"
    )

    data_fields = root.find(
        ns + "dataFields"
    )

    data_field = data_fields[0]

    assert data_field.attrib[
        "name"
    ] == "Sum of Revenue"

    assert data_field.attrib[
        "fld"
    ] == "3"


def test_serialization():

    cache, pivot = build_pivot()

    xml = pivot_table_definition_xml(
        cache,
        pivot
    )

    assert xml.startswith(
        b"<?xml"
    )

    assert (
        b"pivotTableDefinition"
        in xml
    )