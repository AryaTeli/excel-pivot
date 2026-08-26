from excelpivot.source import ExcelSource
from excelpivot.cache import PivotCache
from excelpivot.pivot import PivotTable

from excelpivot.package.pivot_sheet import (
    generate_pivot_sheet,
    pivot_sheet_xml
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


def local_name(tag):

    return tag.split("}")[-1]


def test_pivot_sheet():

    pivot = build_pivot()

    root = generate_pivot_sheet(
        pivot,
        start_row=3,
        start_column=0
    )

    assert local_name(
        root.tag
    ) == "worksheet"


def test_dimension():

    pivot = build_pivot()

    root = generate_pivot_sheet(
        pivot,
        start_row=3,
        start_column=0
    )

    dimension = next(
        element
        for element in root
        if local_name(element.tag)
        == "dimension"
    )

    assert dimension.attrib[
        "ref"
    ] == "A1:E9"


def test_pivot_values():

    pivot = build_pivot()

    root = generate_pivot_sheet(
        pivot,
        start_row=3,
        start_column=0
    )

    sheet_data = next(
        element
        for element in root
        if local_name(element.tag)
        == "sheetData"
    )

    # Filter + Header + Rows
    assert len(sheet_data) >= 2


def test_pivot_relationship():

    pivot = build_pivot()

    root = generate_pivot_sheet(
        pivot
    )

    pivot_parts = next(
        element
        for element in root
        if local_name(element.tag)
        == "pivotTableParts"
    )

    assert pivot_parts.attrib[
        "count"
    ] == "1"

    assert (
        pivot_parts[0].attrib[
            "{http://schemas.openxmlformats.org/"
            "officeDocument/2006/relationships}"
            "id"
        ]
        == "rId1"
    )


def test_serialization():

    pivot = build_pivot()

    xml = pivot_sheet_xml(
        pivot,
        start_row=3
    )

    assert xml.startswith(
        b"<?xml"
    )

    assert b"sheetData" in xml

    assert b"pivotTableParts" in xml



def test_filter_area():

    pivot = build_pivot()

    root = generate_pivot_sheet(
        pivot,
        start_row=3,
        start_column=0
    )

    sheet_data = next(
        element
        for element in root
        if local_name(element.tag)
        == "sheetData"
    )

    first_row = sheet_data[0]

    assert first_row.attrib[
        "r"
    ] == "1"

    cells = list(first_row)

    assert cells[0].attrib[
        "r"
    ] == "A1"

    assert cells[1].attrib[
        "r"
    ] == "B1"


def test_filter_values():

    pivot = build_pivot()

    root = generate_pivot_sheet(
        pivot,
        start_row=3,
        start_column=0
    )

    sheet_data = next(
        element
        for element in root
        if local_name(element.tag)
        == "sheetData"
    )

    first_row = sheet_data[0]

    values = []

    for cell in first_row:

        text = cell.find(
            ".//{http://schemas.openxmlformats.org/"
            "spreadsheetml/2006/main}t"
        )

        values.append(
            text.text
        )

    assert values == [
        "Year",
        "(All)"
    ]