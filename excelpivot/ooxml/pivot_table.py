import xml.etree.ElementTree as ET


MAIN_NS = (
    "http://schemas.openxmlformats.org/"
    "spreadsheetml/2006/main"
)


ET.register_namespace("", MAIN_NS)


def qname(namespace, tag):
    return f"{{{namespace}}}{tag}"


def ordered_shared_indexes(cache, field, pivot=None):
    """
    Return shared-item indexes in the same order as the
    calculated PivotTable.

    Example:

        cache:
            0 = North
            1 = South
            2 = West
            3 = East

        calculated result:
            East
            North
            South
            West

        result:
            [3, 0, 1, 2]
    """

    shared_items = cache.shared_items[field.name]

    values = []

    for index, item in enumerate(shared_items):

        if hasattr(item, "value"):
            value = item.value
        else:
            value = item

        values.append((index, value))

    if pivot is not None:

        try:
            result = pivot.calculate()

            headers = result["headers"]
            rows = result["rows"]

            # ------------------------------------------
            # Row field ordering
            # ------------------------------------------

            if (
                pivot.rows
                and field.name == pivot.rows[0].name
            ):

                displayed_values = [
                    row[0]
                    for row in rows
                    if row and row[0] != "Grand Total"
                ]

                index_map = {
                    value: index
                    for index, value in values
                }

                ordered = []

                for value in displayed_values:

                    if value in index_map:
                        ordered.append(
                            index_map[value]
                        )

                if ordered:
                    return ordered

            # ------------------------------------------
            # Column field ordering
            # ------------------------------------------

            if (
                pivot.columns
                and field.name == pivot.columns[0].name
            ):

                displayed_values = [
                    header
                    for header in headers
                    if (
                        header != field.name
                        and header != "Grand Total"
                    )
                ]

                index_map = {
                    value: index
                    for index, value in values
                }

                ordered = []

                for value in displayed_values:

                    if value in index_map:
                        ordered.append(
                            index_map[value]
                        )

                if ordered:
                    return ordered

        except Exception:
            pass

    return [
        index
        for index, value in values
    ]


def add_items(
    pivot_field,
    cache,
    field,
    pivot=None,
    include_grand_total=True
):
    """
    Add the <items> section to a pivotField.
    """

    indexes = ordered_shared_indexes(
        cache,
        field,
        pivot
    )

    count = len(indexes)

    if include_grand_total:
        count += 1

    items = ET.SubElement(
        pivot_field,
        qname(
            MAIN_NS,
            "items"
        ),
        {
            "count": str(count)
        }
    )

    for index in indexes:

        ET.SubElement(
            items,
            qname(
                MAIN_NS,
                "item"
            ),
            {
                "x": str(index)
            }
        )

    if include_grand_total:

        ET.SubElement(
            items,
            qname(
                MAIN_NS,
                "item"
            ),
            {
                "t": "default"
            }
        )


def add_row_items(
    root,
    cache,
    pivot
):
    """
    Generate the <rowItems> section.

    Currently supports one row field.
    """

    if not pivot.rows:
        return

    field = pivot.rows[0]

    indexes = ordered_shared_indexes(
        cache,
        field,
        pivot
    )

    row_items = ET.SubElement(
        root,
        qname(
            MAIN_NS,
            "rowItems"
        ),
        {
            "count": str(
                len(indexes) + 1
            )
        }
    )

    for item_index in range(len(indexes)):

        item = ET.SubElement(
            row_items,
            qname(
                MAIN_NS,
                "i"
            )
        )

        x_elem = ET.SubElement(
            item,
            qname(
                MAIN_NS,
                "x"
            )
        )

        if item_index != 0:
            x_elem.set("v", str(item_index))

    grand_total = ET.SubElement(
        row_items,
        qname(
            MAIN_NS,
            "i"
        ),
        {
            "t": "grand"
        }
    )

    ET.SubElement(
        grand_total,
        qname(
            MAIN_NS,
            "x"
        )
    )


def add_column_items(
    root,
    cache,
    pivot
):
    """
    Generate the <colItems> section.

    Currently supports one column field.
    """

    if not pivot.columns:
        return

    field = pivot.columns[0]

    indexes = ordered_shared_indexes(
        cache,
        field,
        pivot
    )

    col_items = ET.SubElement(
        root,
        qname(
            MAIN_NS,
            "colItems"
        ),
        {
            "count": str(
                len(indexes) + 1
            )
        }
    )

    for item_index in range(len(indexes)):

        item = ET.SubElement(
            col_items,
            qname(
                MAIN_NS,
                "i"
            )
        )

        x_elem = ET.SubElement(
            item,
            qname(
                MAIN_NS,
                "x"
            )
        )

        if item_index != 0:
            x_elem.set("v", str(item_index))

    grand_total = ET.SubElement(
        col_items,
        qname(
            MAIN_NS,
            "i"
        ),
        {
            "t": "grand"
        }
    )

    ET.SubElement(
        grand_total,
        qname(
            MAIN_NS,
            "x"
        )
    )


def column_name(index):
    result = ""
    index += 1
    while index:
        index, remainder = divmod(index - 1, 26)
        result = chr(65 + remainder) + result
    return result


def calculate_pivot_location(pivot, start_row=3, start_column=0):
    try:
        result = pivot.calculate()
        headers = result["headers"]
        rows = result["rows"]
        num_cols = len(headers) if headers else 1
        num_rows = (len(rows) + 2) if rows else 2
    except Exception:
        num_cols = 5
        num_rows = 7

    start_col_str = column_name(start_column)
    end_col_str = column_name(start_column + max(num_cols, 1) - 1)
    end_row_num = start_row + max(num_rows, 1) - 1

    return f"{start_col_str}{start_row}:{end_col_str}{end_row_num}"


def generate_pivot_table_definition(
    cache,
    pivot,
    name="PivotTable1",
    cache_id=5,
    location=None
):
    """
    Generate the XML tree for pivotTableDefinition.
    """
    if location is None:
        location = calculate_pivot_location(pivot)

    root = ET.Element(
        qname(
            MAIN_NS,
            "pivotTableDefinition"
        ),
        {
            "name": name,
            "cacheId": str(cache_id),
            "applyNumberFormats": "0",
            "applyBorderFormats": "0",
            "applyFontFormats": "0",
            "applyPatternFormats": "0",
            "applyAlignmentFormats": "0",
            "applyWidthHeightFormats": "1",
            "dataCaption": "Values",
            "updatedVersion": "8",
            "minRefreshableVersion": "3",
            "useAutoFormatting": "1",
            "itemPrintTitles": "1",
            "createdVersion": "8",
            "indent": "0",
            "outline": "1",
            "outlineData": "1",
            "multipleFieldFilters": "0"
        }
    )

    # ==================================================
    # Location
    # ==================================================

    ET.SubElement(
        root,
        qname(
            MAIN_NS,
            "location"
        ),
        {
            "ref": location,
            "firstHeaderRow": "1",
            "firstDataRow": "2",
            "firstDataCol": "1",
            "rowPageCount": "1",
            "colPageCount": "1"
        }
    )

    # ==================================================
    # Pivot Fields
    # ==================================================

    pivot_fields = ET.SubElement(
        root,
        qname(
            MAIN_NS,
            "pivotFields"
        ),
        {
            "count": str(
                len(cache.fields)
            )
        }
    )

    for field in cache.fields:

        attributes = {
            "showAll": "0"
        }

        if field.role == "row":

            attributes["axis"] = "axisRow"

        elif field.role == "column":

            attributes["axis"] = "axisCol"

        elif field.role == "filter":

            attributes["axis"] = "axisPage"

        elif field.role == "value":

            attributes["dataField"] = "1"

        pivot_field = ET.SubElement(
            pivot_fields,
            qname(
                MAIN_NS,
                "pivotField"
            ),
            attributes
        )

        if field.role in (
            "row",
            "column",
            "filter"
        ):

            add_items(
                pivot_field,
                cache,
                field,
                pivot
            )

    # ==================================================
    # Row Fields
    # ==================================================

    row_fields = ET.SubElement(
        root,
        qname(
            MAIN_NS,
            "rowFields"
        ),
        {
            "count": str(
                len(pivot.rows)
            )
        }
    )

    for field in pivot.rows:

        ET.SubElement(
            row_fields,
            qname(
                MAIN_NS,
                "field"
            ),
            {
                "x": str(field.index)
            }
        )

    # ==================================================
    # Row Items
    # ==================================================

    add_row_items(
        root,
        cache,
        pivot
    )

    # ==================================================
    # Column Fields
    # ==================================================

    col_fields = ET.SubElement(
        root,
        qname(
            MAIN_NS,
            "colFields"
        ),
        {
            "count": str(
                len(pivot.columns)
            )
        }
    )

    for field in pivot.columns:

        ET.SubElement(
            col_fields,
            qname(
                MAIN_NS,
                "field"
            ),
            {
                "x": str(field.index)
            }
        )

    # ==================================================
    # Column Items
    # ==================================================

    add_column_items(
        root,
        cache,
        pivot
    )

    # ==================================================
    # Page / Filter Fields
    # ==================================================

    page_fields = ET.SubElement(
        root,
        qname(
            MAIN_NS,
            "pageFields"
        ),
        {
            "count": str(
                len(pivot.filters)
            )
        }
    )

    for field in pivot.filters:

        ET.SubElement(
            page_fields,
            qname(
                MAIN_NS,
                "pageField"
            ),
            {
                "fld": str(field.index),
                "hier": "-1"
            }
        )

    # ==================================================
    # Data Fields
    # ==================================================

    data_fields = ET.SubElement(
        root,
        qname(
            MAIN_NS,
            "dataFields"
        ),
        {
            "count": str(
                len(pivot.values)
            )
        }
    )

    for data_field in pivot.values:

        ET.SubElement(
            data_fields,
            qname(
                MAIN_NS,
                "dataField"
            ),
            {
                "name": data_field.name,
                "fld": str(
                    data_field.field.index
                ),
                "baseField": "0",
                "baseItem": "0"
            }
        )

    # ==================================================
    # Pivot Table Style
    # ==================================================

    ET.SubElement(
        root,
        qname(
            MAIN_NS,
            "pivotTableStyleInfo"
        ),
        {
            "name": "PivotStyleLight16",
            "showRowHeaders": "1",
            "showColHeaders": "1",
            "showRowStripes": "0",
            "showColStripes": "0",
            "showLastColumn": "1"
        }
    )

    return root


def pivot_table_definition_xml(
    cache,
    pivot,
    name="PivotTable1",
    cache_id=5,
    location=None
):
    """
    Serialize pivotTableDefinition to XML bytes.
    """

    root = generate_pivot_table_definition(
        cache,
        pivot,
        name=name,
        cache_id=cache_id,
        location=location
    )

    return ET.tostring(
        root,
        encoding="utf-8",
        xml_declaration=True
    )