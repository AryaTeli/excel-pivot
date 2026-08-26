import xml.etree.ElementTree as ET


def load_xml(path):

    return ET.parse(path).getroot()


def local_name(tag):

    return tag.split("}")[-1]


def test_generated_cache_records_structure():

    root = load_xml(
        "generated_pivotCacheRecords.xml"
    )

    assert local_name(
        root.tag
    ) == "pivotCacheRecords"

    assert root.attrib[
        "count"
    ] == "10"

    records = list(root)

    assert len(records) == 10

    first = records[0]

    assert [
        local_name(element.tag)
        for element in first
    ] == [
        "x",
        "x",
        "x",
        "n",
        "n"
    ]


def test_generated_pivot_table_structure():

    root = load_xml(
        "generated_pivotTable1.xml"
    )

    assert local_name(
        root.tag
    ) == "pivotTableDefinition"

    assert root.attrib[
        "name"
    ] == "PivotTable1"

    assert root.attrib[
        "cacheId"
    ] == "5"

    children = [
        local_name(child.tag)
        for child in root
    ]

    assert "location" in children

    assert "pivotFields" in children

    assert "rowFields" in children

    assert "rowItems" in children

    assert "colFields" in children

    assert "colItems" in children

    assert "pageFields" in children

    assert "dataFields" in children