import xml.etree.ElementTree as ET


MAIN_NS = (
    "http://schemas.openxmlformats.org/"
    "spreadsheetml/2006/main"
)


ET.register_namespace("", MAIN_NS)


def qname(tag):
    return f"{{{MAIN_NS}}}{tag}"


def generate_table(
    headers,
    table_name="Table1",
    display_name="Table1"
):

    root = ET.Element(
        qname("table"),
        {
            "id": "1",
            "name": table_name,
            "displayName": display_name,
            "ref": (
                f"A1:"
                f"{column_name(len(headers) - 1)}"
                f"{2}"
            ),
            "headerRowCount": "1"
        }
    )

    auto_filter = ET.SubElement(
        root,
        qname("autoFilter"),
        {
            "ref": root.attrib["ref"]
        }
    )

    table_columns = ET.SubElement(
        root,
        qname("tableColumns"),
        {
            "count": str(len(headers))
        }
    )

    for index, header in enumerate(
        headers,
        start=1
    ):

        ET.SubElement(
            table_columns,
            qname("tableColumn"),
            {
                "id": str(index),
                "name": str(header)
            }
        )

    ET.SubElement(
        root,
        qname("tableStyleInfo"),
        {
            "name": "TableStyleMedium2",
            "showFirstColumn": "0",
            "showLastColumn": "0",
            "showRowStripes": "1",
            "showColumnStripes": "0"
        }
    )

    return root


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


def table_xml(
    headers,
    record_count,
    table_name="Table1",
    display_name="Table1"
):

    last_row = record_count + 1

    root = ET.Element(
        qname("table"),
        {
            "id": "1",
            "name": table_name,
            "displayName": display_name,
            "ref": (
                f"A1:"
                f"{column_name(len(headers) - 1)}"
                f"{last_row}"
            ),
            "headerRowCount": "1"
        }
    )

    ET.SubElement(
        root,
        qname("autoFilter"),
        {
            "ref": root.attrib["ref"]
        }
    )

    table_columns = ET.SubElement(
        root,
        qname("tableColumns"),
        {
            "count": str(len(headers))
        }
    )

    for index, header in enumerate(
        headers,
        start=1
    ):

        ET.SubElement(
            table_columns,
            qname("tableColumn"),
            {
                "id": str(index),
                "name": str(header)
            }
        )

    ET.SubElement(
        root,
        qname("tableStyleInfo"),
        {
            "name": "TableStyleMedium2",
            "showFirstColumn": "0",
            "showLastColumn": "0",
            "showRowStripes": "1",
            "showColumnStripes": "0"
        }
    )

    return ET.tostring(
        root,
        encoding="utf-8",
        xml_declaration=True
    )