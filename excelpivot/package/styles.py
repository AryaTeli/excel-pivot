import xml.etree.ElementTree as ET


MAIN_NS = (
    "http://schemas.openxmlformats.org/"
    "spreadsheetml/2006/main"
)


ET.register_namespace("", MAIN_NS)


def qname(tag):
    return f"{{{MAIN_NS}}}{tag}"


def generate_styles():
    root = ET.Element(qname("styleSheet"))

    fonts = ET.SubElement(root, qname("fonts"), {"count": "1"})
    font = ET.SubElement(fonts, qname("font"))
    ET.SubElement(font, qname("sz"), {"val": "11"})
    ET.SubElement(font, qname("color"), {"theme": "1"})
    ET.SubElement(font, qname("name"), {"val": "Calibri"})
    ET.SubElement(font, qname("family"), {"val": "2"})

    fills = ET.SubElement(root, qname("fills"), {"count": "2"})
    fill0 = ET.SubElement(fills, qname("fill"))
    ET.SubElement(fill0, qname("patternFill"), {"patternType": "none"})
    fill1 = ET.SubElement(fills, qname("fill"))
    ET.SubElement(fill1, qname("patternFill"), {"patternType": "gray125"})

    borders = ET.SubElement(root, qname("borders"), {"count": "1"})
    border = ET.SubElement(borders, qname("border"))
    ET.SubElement(border, qname("left"))
    ET.SubElement(border, qname("right"))
    ET.SubElement(border, qname("top"))
    ET.SubElement(border, qname("bottom"))
    ET.SubElement(border, qname("diagonal"))

    csxfs = ET.SubElement(root, qname("cellStyleXfs"), {"count": "1"})
    ET.SubElement(csxfs, qname("xf"), {"numFmtId": "0", "fontId": "0", "fillId": "0", "borderId": "0"})

    cxfs = ET.SubElement(root, qname("cellXfs"), {"count": "1"})
    ET.SubElement(cxfs, qname("xf"), {"numFmtId": "0", "fontId": "0", "fillId": "0", "borderId": "0", "xfId": "0"})

    cstyles = ET.SubElement(root, qname("cellStyles"), {"count": "1"})
    ET.SubElement(cstyles, qname("cellStyle"), {"name": "Normal", "xfId": "0", "builtinId": "0"})

    ET.SubElement(root, qname("dxfs"), {"count": "0"})

    ET.SubElement(root, qname("tableStyles"), {
        "count": "0",
        "defaultTableStyle": "TableStyleMedium2",
        "defaultPivotStyle": "PivotStyleLight16"
    })

    return root


def styles_xml():
    root = generate_styles()
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)
