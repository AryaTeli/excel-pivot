from excelpivot.package.worksheet import (
    generate_worksheet,
    worksheet_xml,
    column_name,
    cell_reference
)


def local_name(tag):
    return tag.split("}")[-1]


def test_column_names():

    assert column_name(0) == "A"

    assert column_name(1) == "B"

    assert column_name(25) == "Z"

    assert column_name(26) == "AA"

    assert column_name(27) == "AB"


def test_cell_reference():

    assert cell_reference(1, 0) == "A1"

    assert cell_reference(1, 4) == "E1"

    assert cell_reference(10, 0) == "A10"


def test_worksheet():

    headers = [
        "Region",
        "Product",
        "Year",
        "Revenue",
        "Quantity"
    ]

    records = [
        (
            "North",
            "Laptop",
            2025,
            10000,
            10
        ),
        (
            "South",
            "Phone",
            2026,
            7000,
            7
        )
    ]

    root = generate_worksheet(
        headers,
        records
    )

    assert local_name(
        root.tag
    ) == "worksheet"

    sheet_data = next(
        element
        for element in root
        if local_name(element.tag)
        == "sheetData"
    )

    assert len(sheet_data) == 3


def test_worksheet_serialization():

    xml = worksheet_xml(
        ["A"],
        [(1,)]
    )

    assert xml.startswith(
        b"<?xml"
    )

    assert b"worksheet" in xml

    assert b"sheetData" in xml


def test_pivot_table_part():

    root = generate_worksheet(
        [],
        [],
        include_data=False,
        include_pivot_table=True
    )

    ns = (
        "{http://schemas.openxmlformats.org/"
        "spreadsheetml/2006/main}"
    )

    pivot_parts = root.find(
        ns + "pivotTableParts"
    )

    assert pivot_parts is not None

    assert pivot_parts.attrib[
        "count"
    ] == "1"

    pivot_part = pivot_parts[0]

    relationship_id = (
        "{http://schemas.openxmlformats.org/"
        "officeDocument/2006/relationships}"
        "id"
    )

    assert pivot_part.attrib[
        relationship_id
    ] == "rId1"