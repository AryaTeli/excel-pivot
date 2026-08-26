import xml.etree.ElementTree as ET


CT_NS = (
    "http://schemas.openxmlformats.org/"
    "package/2006/content-types"
)


ET.register_namespace("", CT_NS)


def qname(tag):
    return f"{{{CT_NS}}}{tag}"


def generate_content_types():

    root = ET.Element(
        qname("Types")
    )

    ET.SubElement(
        root,
        qname("Default"),
        {
            "Extension": "rels",
            "ContentType": (
                "application/vnd.openxmlformats-"
                "package.relationships+xml"
            )
        }
    )

    ET.SubElement(
        root,
        qname("Default"),
        {
            "Extension": "xml",
            "ContentType": "application/xml"
        }
    )

    ET.SubElement(
        root,
        qname("Override"),
        {
            "PartName": "/xl/styles.xml",
            "ContentType": (
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.styles+xml"
            )
        }
    )

    ET.SubElement(
        root,
        qname("Override"),
        {
            "PartName": "/xl/workbook.xml",
            "ContentType": (
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.sheet.main+xml"
            )
        }
    )

    ET.SubElement(
        root,
        qname("Override"),
        {
            "PartName": (
                "/xl/worksheets/sheet1.xml"
            ),
            "ContentType": (
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.worksheet+xml"
            )
        }
    )

    ET.SubElement(
        root,
        qname("Override"),
        {
            "PartName": (
                "/xl/worksheets/sheet2.xml"
            ),
            "ContentType": (
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.worksheet+xml"
            )
        }
    )

    ET.SubElement(
        root,
        qname("Override"),
        {
            "PartName": (
                "/xl/pivotCache/"
                "pivotCacheDefinition1.xml"
            ),
            "ContentType": (
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.pivotCacheDefinition+xml"
            )
        }
    )

    ET.SubElement(
        root,
        qname("Override"),
        {
            "PartName": (
                "/xl/pivotCache/"
                "pivotCacheRecords1.xml"
            ),
            "ContentType": (
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.pivotCacheRecords+xml"
            )
        }
    )

    ET.SubElement(
        root,
        qname("Override"),
        {
            "PartName": (
                "/xl/pivotTables/"
                "pivotTable1.xml"
            ),
            "ContentType": (
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.pivotTable+xml"
            )
        }
    )

    ET.SubElement(
        root,
        qname("Override"),
        {
            "PartName": "/xl/tables/table1.xml",
            "ContentType": (
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.table+xml"
            )
        }
    )

    return root


def content_types_xml():

    root = generate_content_types()

    return ET.tostring(
        root,
        encoding="utf-8",
        xml_declaration=True
    )