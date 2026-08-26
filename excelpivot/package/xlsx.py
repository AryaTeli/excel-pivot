import zipfile
from pathlib import Path


from excelpivot.package.content_types import (
    content_types_xml
)

from excelpivot.package.workbook import (
    workbook_xml
)

from excelpivot.package.workbook_relationships import (
    workbook_relationships_xml
)

from excelpivot.package.worksheet import (
    worksheet_xml
)

from excelpivot.package.pivot_sheet import (
    pivot_sheet_xml
)

from excelpivot.package.worksheet_relationships import (
    pivot_worksheet_relationships_xml
)

from excelpivot.package.table import (
    table_xml
)

from excelpivot.package.table_relationships import (
    table_relationships_xml
)

from excelpivot.package.pivot_cache_relationships import (
    pivot_cache_relationships_xml
)

from excelpivot.package.pivot_table_relationships import (
    pivot_table_relationships_xml
)

from excelpivot.package.styles import (
    styles_xml
)


from excelpivot.ooxml.cache_definition import (
    cache_definition_xml
)

from excelpivot.ooxml.cache_records import (
    cache_records_xml
)

from excelpivot.ooxml.pivot_table import (
    pivot_table_definition_xml
)


ROOT_RELS = b"""<?xml version="1.0" encoding="utf-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship
        Id="rId1"
        Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
        Target="xl/workbook.xml"/>
</Relationships>
"""


def build_xlsx(
    output_path,
    headers,
    records,
    cache,
    pivot
):
    """
    Build an XLSX workbook containing:

    - Source worksheet
    - Excel Table
    - Pivot worksheet
    - PivotTable
    - Pivot cache definition
    - Pivot cache records
    - Required relationships
    """

    output_path = Path(
        output_path
    )

    with zipfile.ZipFile(
        output_path,
        "w",
        compression=zipfile.ZIP_DEFLATED
    ) as archive:

        # ==================================================
        # Build integer dimension shared items
        # ==================================================
        #
        # Integer fields used as dimensions
        # (row, column, filter) need shared items
        # built before XML generation.
        #

        cache.build_dimension_shared_items(
            pivot
        )

        # ==================================================
        # Root relationships
        # ==================================================

        archive.writestr(
            "_rels/.rels",
            ROOT_RELS
        )

        # ==================================================
        # Content Types
        # ==================================================

        archive.writestr(
            "[Content_Types].xml",
            content_types_xml()
        )

        # ==================================================
        # Workbook
        # ==================================================

        archive.writestr(
            "xl/workbook.xml",
            workbook_xml()
        )

        archive.writestr(
            "xl/_rels/workbook.xml.rels",
            workbook_relationships_xml()
        )

        # ==================================================
        # Styles
        # ==================================================

        archive.writestr(
            "xl/styles.xml",
            styles_xml()
        )

        # ==================================================
        # Source Worksheet
        # ==================================================
        #
        # This is the worksheet containing the original
        # source data.
        #
        # It also contains Table1.
        #

        archive.writestr(
            "xl/worksheets/sheet1.xml",
            worksheet_xml(
                headers,
                records,
                include_data=True,
                include_table=True
            )
        )

        # ==================================================
        # Source Worksheet Relationships
        # ==================================================
        #
        # sheet1.xml
        #     |
        #     └── rId1
        #            |
        #            └── ../tables/table1.xml
        #

        archive.writestr(
            "xl/worksheets/_rels/"
            "sheet1.xml.rels",
            table_relationships_xml()
        )

        # ==================================================
        # Excel Table
        # ==================================================

        archive.writestr(
            "xl/tables/table1.xml",
            table_xml(
                headers,
                len(records)
            )
        )

        # ==================================================
        # Pivot Worksheet
        # ==================================================
        #
        # IMPORTANT:
        #
        # Previously this was generated using:
        #
        #     worksheet_xml([], [])
        #
        # which produced:
        #
        #     <sheetData />
        #
        # Now we use pivot_sheet_xml(), which calls:
        #
        #     pivot.calculate()
        #
        # and writes the calculated PivotTable result
        # into sheet2.xml.
        #

        archive.writestr(
            "xl/worksheets/sheet2.xml",
            pivot_sheet_xml(
                pivot,
                start_row=3,
                start_column=0
            )
        )

        # ==================================================
        # Pivot Worksheet Relationships
        # ==================================================
        #
        # sheet2.xml
        #     |
        #     └── rId1
        #            |
        #            └── ../pivotTables/pivotTable1.xml
        #

        archive.writestr(
            "xl/worksheets/_rels/"
            "sheet2.xml.rels",
            pivot_worksheet_relationships_xml()
        )

        # ==================================================
        # Pivot Cache Definition
        # ==================================================

        archive.writestr(
            "xl/pivotCache/"
            "pivotCacheDefinition1.xml",
            cache_definition_xml(
                cache
            )
        )

        # ==================================================
        # Pivot Cache Records
        # ==================================================

        archive.writestr(
            "xl/pivotCache/"
            "pivotCacheRecords1.xml",
            cache_records_xml(
                cache,
                pivot
            )
        )

        # ==================================================
        # Pivot Cache Relationships
        # ==================================================

        archive.writestr(
            "xl/pivotCache/_rels/"
            "pivotCacheDefinition1.xml.rels",
            pivot_cache_relationships_xml()
        )

        # ==================================================
        # PivotTable Definition
        # ==================================================

        archive.writestr(
            "xl/pivotTables/"
            "pivotTable1.xml",
            pivot_table_definition_xml(
                cache,
                pivot
            )
        )

        # ==================================================
        # PivotTable Relationships
        # ==================================================

        archive.writestr(
            "xl/pivotTables/_rels/"
            "pivotTable1.xml.rels",
            pivot_table_relationships_xml()
        )

    return output_path