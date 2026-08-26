import xml.etree.ElementTree as ET


MAIN_NS = (
    "http://schemas.openxmlformats.org/"
    "spreadsheetml/2006/main"
)


ET.register_namespace("", MAIN_NS)


def qname(namespace, tag):
    return f"{{{namespace}}}{tag}"


def generate_cache_records(cache, pivot):

    root = ET.Element(
        qname(MAIN_NS, "pivotCacheRecords"),
        {
            "count": str(len(cache.records))
        }
    )

    dimension_field_indexes = {
        field.index
        for field in cache.fields
        if field.role in (
            "row",
            "column",
            "filter"
        )
    }

    for record in cache.records:

        record_element = ET.SubElement(
            root,
            qname(MAIN_NS, "r")
        )

        for field in cache.fields:

            value = record[field.index]

            if value is None:

                ET.SubElement(
                    record_element,
                    qname(MAIN_NS, "m")
                )

            elif field.index in dimension_field_indexes:

                shared_index = cache.get_shared_index(
                    field.name,
                    value
                )

                ET.SubElement(
                    record_element,
                    qname(MAIN_NS, "x"),
                    {
                        "v": str(shared_index)
                    }
                )

            elif field.data_type in (
                "integer",
                "number"
            ):

                ET.SubElement(
                    record_element,
                    qname(MAIN_NS, "n"),
                    {
                        "v": str(value)
                    }
                )

            else:

                shared_index = cache.get_shared_index(
                    field.name,
                    value
                )

                ET.SubElement(
                    record_element,
                    qname(MAIN_NS, "x"),
                    {
                        "v": str(shared_index)
                    }
                )

    return root


def cache_records_xml(cache, pivot):

    root = generate_cache_records(
        cache,
        pivot
    )

    return ET.tostring(
        root,
        encoding="utf-8",
        xml_declaration=True
    )