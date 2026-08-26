from excelpivot.package.content_types import (
    generate_content_types
)

from excelpivot.package.workbook import (
    generate_workbook
)

from excelpivot.package.workbook_relationships import (
    generate_workbook_relationships
)

from excelpivot.package.worksheet_relationships import (
    generate_pivot_worksheet_relationships
)

from excelpivot.package.pivot_cache_relationships import (
    generate_pivot_cache_relationships
)

from excelpivot.package.pivot_table_relationships import (
    generate_pivot_table_relationships
)


def local_name(tag):
    return tag.split("}")[-1]


def test_content_types():

    root = generate_content_types()

    assert local_name(root.tag) == "Types"

    overrides = [
        element
        for element in root
        if local_name(element.tag) == "Override"
    ]

    assert len(overrides) == 8


def test_workbook():

    root = generate_workbook()

    assert local_name(root.tag) == "workbook"

    sheets = next(
        element
        for element in root
        if local_name(element.tag) == "sheets"
    )

    assert len(sheets) == 2

    assert sheets[0].attrib["name"] == "Data"

    assert sheets[1].attrib["name"] == "Pivot"


def test_workbook_relationships():

    root = generate_workbook_relationships()

    assert local_name(root.tag) == "Relationships"

    relationships = list(root)

    assert len(relationships) == 4

    assert relationships[0].attrib["Id"] == "rId1"

    assert relationships[1].attrib["Id"] == "rId2"

    assert relationships[2].attrib["Id"] == "rId3"

    assert relationships[3].attrib["Id"] == "rId4"

def test_pivot_worksheet_relationships():

    root = (
        generate_pivot_worksheet_relationships()
    )

    assert local_name(
        root.tag
    ) == "Relationships"

    relationships = list(root)

    assert len(relationships) == 1

    assert relationships[0].attrib[
        "Id"
    ] == "rId1"

    assert relationships[0].attrib[
        "Target"
    ] == "../pivotTables/pivotTable1.xml"


def test_pivot_cache_relationships():

    root = generate_pivot_cache_relationships()

    relationships = list(root)

    assert len(relationships) == 1

    assert relationships[0].attrib["Id"] == "rId1"

    assert (
        relationships[0].attrib["Target"]
        == "pivotCacheRecords1.xml"
    )