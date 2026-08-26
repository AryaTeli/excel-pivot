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
    """
    Convert zero-based column index to Excel column letters.

    0  -> A
    1  -> B
    25 -> Z
    26 -> AA
    27 -> AB
    """

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


def cell_reference(row, column):
    """
    Create an Excel cell reference.

    Example:

    row=1, column=0 -> A1
    row=5, column=3 -> D5
    """

    return (
        f"{column_name(column)}"
        f"{row}"
    )


def generate_worksheet(
    headers,
    records,
    include_data=True,
    include_pivot_table=False,
    include_table=False
):
    """
    Generate worksheet XML.

    Parameters
    ----------
    headers:
        Column names.

    records:
        Worksheet data.

    include_data:
        Whether to write the source data.

    include_pivot_table:
        Whether this worksheet contains a PivotTable.

    include_table:
        Whether this worksheet contains an Excel Table.
    """

    root = ET.Element(
        qname(
            MAIN_NS,
            "worksheet"
        )
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

    # ==================================================
    # Header Row
    # ==================================================

    if headers:

        header_row = ET.SubElement(
            sheet_data,
            qname(
                MAIN_NS,
                "row"
            ),
            {
                "r": "1"
            }
        )

        for column_index, header in enumerate(
            headers
        ):

            cell = ET.SubElement(
                header_row,
                qname(
                    MAIN_NS,
                    "c"
                ),
                {
                    "r": cell_reference(
                        1,
                        column_index
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

            text.text = str(header)

    # ==================================================
    # Data Rows
    # ==================================================

    if include_data:

        for row_index, record in enumerate(
            records,
            start=2
        ):

            row = ET.SubElement(
                sheet_data,
                qname(
                    MAIN_NS,
                    "row"
                ),
                {
                    "r": str(row_index)
                }
            )

            for column_index, value in enumerate(
                record
            ):

                cell = ET.SubElement(
                    row,
                    qname(
                        MAIN_NS,
                        "c"
                    ),
                    {
                        "r": cell_reference(
                            row_index,
                            column_index
                        )
                    }
                )

                # --------------------------------------
                # String
                # --------------------------------------

                if isinstance(
                    value,
                    str
                ):

                    cell.set(
                        "t",
                        "inlineStr"
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

                    text.text = value

                # --------------------------------------
                # Empty value
                # --------------------------------------

                elif value is None:

                    cell.set(
                        "t",
                        "inlineStr"
                    )

                    ET.SubElement(
                        cell,
                        qname(
                            MAIN_NS,
                            "is"
                        )
                    )

                # --------------------------------------
                # Number
                # --------------------------------------

                else:

                    value_element = ET.SubElement(
                        cell,
                        qname(
                            MAIN_NS,
                            "v"
                        )
                    )

                    value_element.text = str(
                        value
                    )

    # ==================================================
    # Excel Table
    # ==================================================

    if include_table:

        table_parts = ET.SubElement(
            root,
            qname(
                MAIN_NS,
                "tableParts"
            ),
            {
                "count": "1"
            }
        )

        ET.SubElement(
            table_parts,
            qname(
                MAIN_NS,
                "tablePart"
            ),
            {
                qname(
                    REL_NS,
                    "id"
                ): "rId1"
            }
        )

    # ==================================================
    # PivotTable
    # ==================================================

    if include_pivot_table:

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


def worksheet_xml(
    headers,
    records,
    include_data=True,
    include_pivot_table=False,
    include_table=False
):
    """
    Serialize worksheet XML.
    """

    root = generate_worksheet(
        headers,
        records,
        include_data=include_data,
        include_pivot_table=include_pivot_table,
        include_table=include_table
    )

    return ET.tostring(
        root,
        encoding="utf-8",
        xml_declaration=True
    )