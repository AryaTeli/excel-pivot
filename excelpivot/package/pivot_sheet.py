import xml.etree.ElementTree as ET


MAIN_NS = (
    "http://schemas.openxmlformats.org/"
    "spreadsheetml/2006/main"
)

REL_NS = (
    "http://schemas.openxmlformats.org/"
    "officeDocument/2006/relationships"
)


ET.register_namespace("", MAIN_NS)
ET.register_namespace("r", REL_NS)


def qname(namespace, tag):
    return f"{{{namespace}}}{tag}"


def column_name(index):

    result = ""

    index += 1

    while index:

        index, remainder = divmod(
            index - 1,
            26
        )

        result = (
            chr(65 + remainder)
            + result
        )

    return result


def cell_reference(
    row,
    column
):

    return (
        f"{column_name(column)}"
        f"{row}"
    )


def add_string_cell(
    row,
    row_number,
    column_number,
    value
):

    cell = ET.SubElement(
        row,
        qname(
            MAIN_NS,
            "c"
        ),
        {
            "r": cell_reference(
                row_number,
                column_number
            ),
            "t": "inlineStr"
        }
    )

    inline_string = ET.SubElement(
        cell,
        qname(
            MAIN_NS,
            "is"
        )
    )

    text = ET.SubElement(
        inline_string,
        qname(
            MAIN_NS,
            "t"
        )
    )

    text.text = str(value)

    return cell


def add_number_cell(
    row,
    row_number,
    column_number,
    value
):

    cell = ET.SubElement(
        row,
        qname(
            MAIN_NS,
            "c"
        ),
        {
            "r": cell_reference(
                row_number,
                column_number
            )
        }
    )

    value_element = ET.SubElement(
        cell,
        qname(
            MAIN_NS,
            "v"
        )
    )

    value_element.text = str(value)

    return cell


def add_value_cell(
    row,
    row_number,
    column_number,
    value
):

    if isinstance(
        value,
        str
    ):

        return add_string_cell(
            row,
            row_number,
            column_number,
            value
        )

    return add_number_cell(
        row,
        row_number,
        column_number,
        value
    )

def add_filter_area(
    sheet_data,
    pivot,
):
    """
    Generate the PivotTable page/filter area.

    For V1 we support one filter field.

    Example:

        A1 = Year
        B1 = (All)
    """

    if not pivot.filters:
        return

    filter_field = pivot.filters[0]

    row_number = 1

    row = ET.SubElement(
        sheet_data,
        qname(
            MAIN_NS,
            "row"
        ),
        {
            "r": str(row_number)
        }
    )

    # Filter field name
    add_string_cell(
        row,
        row_number,
        0,
        filter_field.name
    )

    # Current selection
    add_string_cell(
        row,
        row_number,
        1,
        "(All)"
    )


def generate_pivot_sheet(
    pivot,
    start_row=3,
    start_column=0
):

    result = pivot.calculate()

    headers = result["headers"]

    data_rows = result["rows"]

    root = ET.Element(
        qname(
            MAIN_NS,
            "worksheet"
        )
    )

    # ==================================================
    # Dimension
    # ==================================================
    #
    # Excel's PivotTable definition occupies A3:E9.
    #
    # Row 3 = Pivot header
    # Row 4 = actual column headers
    # Rows 5-9 = data
    #

    first_row = 1 if pivot.filters else start_row

    last_row = (
        start_row
        + len(data_rows)
        + 1
    )

    last_column = (
        start_column
        + len(headers)
        - 1
    )

    dimension_ref = (
        f"{cell_reference(first_row, start_column)}:"
        f"{cell_reference(last_row, last_column)}"
    )

    ET.SubElement(
        root,
        qname(
            MAIN_NS,
            "dimension"
        ),
        {
            "ref": dimension_ref
        }
    )

    # ==================================================
    # Sheet Views
    # ==================================================

    sheet_views = ET.SubElement(
        root,
        qname(
            MAIN_NS,
            "sheetViews"
        )
    )

    sheet_view = ET.SubElement(
        sheet_views,
        qname(
            MAIN_NS,
            "sheetView"
        ),
        {
            "workbookViewId": "0"
        }
    )

    ET.SubElement(
        sheet_view,
        qname(
            MAIN_NS,
            "selection"
        ),
        {
            "activeCell": "A3",
            "sqref": "A3"
        }
    )

    # ==================================================
    # Sheet Data
    # ==================================================

    sheet_data = ET.SubElement(
        root,
        qname(
            MAIN_NS,
            "sheetData"
        )
    )
    add_filter_area(
        sheet_data,
        pivot
    )

    # Pivot Header Row
    pivot_header_row = ET.SubElement(
        sheet_data,
        qname(
            MAIN_NS,
            "row"
        ),
        {
            "r": str(start_row)
        }
    )

    add_string_cell(
        pivot_header_row,
        start_row,
        start_column,
        "Row Labels"
    )

    if pivot.columns:
        add_string_cell(
            pivot_header_row,
            start_row,
            start_column + 1,
            "Column Labels"
        )

    # Actual Pivot Headers
    header_row_number = start_row + 1
    header_row = ET.SubElement(
        sheet_data,
        qname(
            MAIN_NS,
            "row"
        ),
        {
            "r": str(header_row_number)
        }
    )

    for offset, value in enumerate(headers):
        column_number = start_column + offset
        add_string_cell(
            header_row,
            header_row_number,
            column_number,
            value
        )

    # Data Rows
    for row_offset, values in enumerate(data_rows, start=2):
        row_number = start_row + row_offset
        row = ET.SubElement(
            sheet_data,
            qname(
                MAIN_NS,
                "row"
            ),
            {
                "r": str(row_number)
            }
        )

        for column_offset, value in enumerate(values):
            column_number = start_column + column_offset
            add_value_cell(
                row,
                row_number,
                column_number,
                value
            )

    # ==================================================
    # Page Margins
    # ==================================================

    ET.SubElement(
        root,
        qname(
            MAIN_NS,
            "pageMargins"
        ),
        {
            "left": "0.7",
            "right": "0.7",
            "top": "0.75",
            "bottom": "0.75",
            "header": "0.3",
            "footer": "0.3"
        }
    )

    # ==================================================
    # Pivot Table Parts
    # ==================================================

    pivot_table_parts = ET.SubElement(
        root,
        qname(
            MAIN_NS,
            "pivotTableParts"
        ),
        {
            "count": "1"
        }
    )

    ET.SubElement(
        pivot_table_parts,
        qname(
            MAIN_NS,
            "pivotTablePart"
        ),
        {
            qname(
                REL_NS,
                "id"
            ): "rId1"
        }
    )

    return root


def pivot_sheet_xml(
    pivot,
    start_row=3,
    start_column=0
):

    root = generate_pivot_sheet(
        pivot,
        start_row=start_row,
        start_column=start_column
    )

    return ET.tostring(
        root,
        encoding="utf-8",
        xml_declaration=True
    )