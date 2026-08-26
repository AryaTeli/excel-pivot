from excelpivot.source import ExcelSource
from excelpivot.cache import PivotCache
from excelpivot.ooxml.cache_definition import (
    generate_cache_definition,
    cache_definition_xml
)


def build_cache():

    source = ExcelSource(
        "reference/v1_simple.xlsx"
    )

    headers, records = source.read_table("Table1")

    return PivotCache(
        headers,
        records
    )


def test_cache_definition():

    cache = build_cache()

    root = generate_cache_definition(
        cache
    )

    assert root.tag.endswith(
        "pivotCacheDefinition"
    )

    cache_source = root.find(
        "{http://schemas.openxmlformats.org/"
        "spreadsheetml/2006/main}"
        "cacheSource"
    )

    assert cache_source is not None

    worksheet_source = cache_source.find(
        "{http://schemas.openxmlformats.org/"
        "spreadsheetml/2006/main}"
        "worksheetSource"
    )

    assert worksheet_source is not None

    assert worksheet_source.attrib["name"] == "Table1"


def test_cache_field_count():

    cache = build_cache()

    root = generate_cache_definition(
        cache
    )

    namespace = (
        "{http://schemas.openxmlformats.org/"
        "spreadsheetml/2006/main}"
    )

    cache_fields = root.find(
        namespace + "cacheFields"
    )

    assert cache_fields is not None

    assert cache_fields.attrib["count"] == "5"


def test_cache_definition_serialization():

    cache = build_cache()

    xml = cache_definition_xml(
        cache
    )

    assert xml.startswith(
        b"<?xml"
    )

    assert (
        b"pivotCacheDefinition"
        in xml
    )

    assert (
        b"cacheFields"
        in xml
    )