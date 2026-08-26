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


def generate_workbook():

    root = ET.Element(
        qname(MAIN_NS, "workbook")
    )

    sheets = ET.SubElement(
        root,
        qname(MAIN_NS, "sheets")
    )

    ET.SubElement(
        sheets,
        qname(MAIN_NS, "sheet"),
        {
            "name": "Data",
            "sheetId": "1",
            qname(REL_NS, "id"): "rId1"
        }
    )

    ET.SubElement(
        sheets,
        qname(MAIN_NS, "sheet"),
        {
            "name": "Pivot",
            "sheetId": "2",
            qname(REL_NS, "id"): "rId2"
        }
    )

    # Pivot cache registration
    pivot_caches = ET.SubElement(
        root,
        qname(MAIN_NS, "pivotCaches")
    )

    ET.SubElement(
        pivot_caches,
        qname(MAIN_NS, "pivotCache"),
        {
            "cacheId": "5",
            qname(REL_NS, "id"): "rId3"
        }
    )

    return root


def workbook_xml():

    root = generate_workbook()

    return ET.tostring(
        root,
        encoding="utf-8",
        xml_declaration=True
    )