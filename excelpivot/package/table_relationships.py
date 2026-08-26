import xml.etree.ElementTree as ET


REL_NS = (
    "http://schemas.openxmlformats.org/"
    "package/2006/relationships"
)


ET.register_namespace("", REL_NS)


def qname(tag):
    return f"{{{REL_NS}}}{tag}"


def table_relationships_xml():

    root = ET.Element(
        qname("Relationships")
    )

    ET.SubElement(
        root,
        qname("Relationship"),
        {
            "Id": "rId1",
            "Type": (
                "http://schemas.openxmlformats.org/"
                "officeDocument/2006/relationships/"
                "table"
            ),
            "Target": "../tables/table1.xml"
        }
    )

    return ET.tostring(
        root,
        encoding="utf-8",
        xml_declaration=True
    )