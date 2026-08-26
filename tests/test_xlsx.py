import zipfile

from excelpivot.source import ExcelSource
from excelpivot.cache import PivotCache
from excelpivot.pivot import PivotTable

from excelpivot.package.xlsx import (
    build_xlsx
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

    return headers, records, cache, pivot


def test_xlsx_created(tmp_path):

    headers, records, cache, pivot = (
        build_pivot()
    )

    output = (
        tmp_path
        / "generated_pivot.xlsx"
    )

    result = build_xlsx(
        output,
        headers,
        records,
        cache,
        pivot
    )

    assert result.exists()

    assert result.stat().st_size > 0


def test_xlsx_structure(tmp_path):

    headers, records, cache, pivot = (
        build_pivot()
    )

    output = (
        tmp_path
        / "generated_pivot.xlsx"
    )

    build_xlsx(
        output,
        headers,
        records,
        cache,
        pivot
    )

    with zipfile.ZipFile(
        output,
        "r"
    ) as archive:

        names = archive.namelist()

    assert "[Content_Types].xml" in names

    assert "_rels/.rels" in names

    assert "xl/workbook.xml" in names

    assert (
        "xl/_rels/workbook.xml.rels"
        in names
    )

    assert (
        "xl/worksheets/sheet1.xml"
        in names
    )

    assert (
        "xl/worksheets/sheet2.xml"
        in names
    )

    assert (
        "xl/worksheets/_rels/"
        "sheet2.xml.rels"
        in names
    )

    assert (
        "xl/pivotCache/"
        "pivotCacheDefinition1.xml"
        in names
    )

    assert (
        "xl/pivotCache/"
        "pivotCacheRecords1.xml"
        in names
    )

    assert (
        "xl/pivotTables/"
        "pivotTable1.xml"
        in names
    )

    assert (
        "xl/pivotCache/_rels/"
        "pivotCacheDefinition1.xml.rels"
        in names
    )

    assert (
        "xl/pivotTables/_rels/"
        "pivotTable1.xml.rels"
        in names
    )

    assert (
        "xl/styles.xml"
        in names
    )

    assert (
        "xl/tables/table1.xml"
        in names
    )