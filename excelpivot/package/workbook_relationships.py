import xml.etree.ElementTree as ET


REL_NS = (
    "http://schemas.openxmlformats.org/"
    "package/2006/relationships"
)


ET.register_namespace("", REL_NS)


def qname(tag):
    return f"{{{REL_NS}}}{tag}"


def generate_workbook_relationships():

    root = ET.Element(
        qname("Relationships")
    )

    # Data worksheet
    ET.SubElement(
        root,
        qname("Relationship"),
        {
            "Id": "rId1",
            "Type": (
                "http://schemas.openxmlformats.org/"
                "officeDocument/2006/relationships/"
                "worksheet"
            ),
            "Target": "worksheets/sheet1.xml"
        }
    )

    # Pivot worksheet
    ET.SubElement(
        root,
        qname("Relationship"),
        {
            "Id": "rId2",
            "Type": (
                "http://schemas.openxmlformats.org/"
                "officeDocument/2006/relationships/"
                "worksheet"
            ),
            "Target": "worksheets/sheet2.xml"
        }
    )

    # Pivot cache definition
    ET.SubElement(
        root,
        qname("Relationship"),
        {
            "Id": "rId3",
            "Type": (
                "http://schemas.openxmlformats.org/"
                "officeDocument/2006/relationships/"
                "pivotCacheDefinition"
            ),
            "Target": (
                "pivotCache/"
                "pivotCacheDefinition1.xml"
            )
        }
    )

    # Styles
    ET.SubElement(
        root,
        qname("Relationship"),
        {
            "Id": "rId4",
            "Type": (
                "http://schemas.openxmlformats.org/"
                "officeDocument/2006/relationships/"
                "styles"
            ),
            "Target": "styles.xml"
        }
    )

    return root


def workbook_relationships_xml():

    root = generate_workbook_relationships()

    return ET.tostring(
        root,
        encoding="utf-8",
        xml_declaration=True
    )