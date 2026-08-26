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


def generate_cache_definition(cache):
    root = ET.Element(
        qname(MAIN_NS, "pivotCacheDefinition"),
        {
            qname(REL_NS, "id"): "rId1",
            "recordCount": str(len(cache.records)),
            "createdVersion": "8",
            "refreshedVersion": "8",
            "minRefreshableVersion": "3",
            "refreshOnLoad": "1",
        }
    )

    cache_source = ET.SubElement(
        root,
        qname(MAIN_NS, "cacheSource"),
        {
            "type": "worksheet"
        }
    )

    ET.SubElement(
        cache_source,
        qname(MAIN_NS, "worksheetSource"),
        {
            "name": "Table1"
        }
    )

    cache_fields = ET.SubElement(
        root,
        qname(MAIN_NS, "cacheFields"),
        {
            "count": str(len(cache.fields))
        }
    )

    for field in cache.fields:

        cache_field = ET.SubElement(
            cache_fields,
            qname(MAIN_NS, "cacheField"),
            {
                "name": field.name,
                "numFmtId": "0"
            }
        )

        shared_items = cache.shared_items.get(
            field.name,
            {}
        )

        if field.data_type == "string":

            items = ET.SubElement(
                cache_field,
                qname(MAIN_NS, "sharedItems"),
                {
                    "count": str(len(shared_items))
                }
            )

            for value in shared_items.keys():

                ET.SubElement(
                    items,
                    qname(MAIN_NS, "s"),
                    {
                        "v": value
                    }
                )

        elif field.data_type == "integer":

            metadata = cache.field_metadata[
                field.name
            ]

            if shared_items:

                items = ET.SubElement(
                    cache_field,
                    qname(MAIN_NS, "sharedItems"),
                    {
                        "containsSemiMixedTypes": "0",
                        "containsString": "0",
                        "containsNumber": "1",
                        "containsInteger": "1",
                        "minValue": str(
                            metadata["min"]
                        ),
                        "maxValue": str(
                            metadata["max"]
                        ),
                        "count": str(
                            len(shared_items)
                        ),
                    }
                )

                for value in shared_items.keys():

                    ET.SubElement(
                        items,
                        qname(MAIN_NS, "n"),
                        {
                            "v": str(value)
                        }
                    )

            else:

                ET.SubElement(
                    cache_field,
                    qname(MAIN_NS, "sharedItems"),
                    {
                        "containsSemiMixedTypes":
                            "0",
                        "containsString": "0",
                        "containsNumber": "1",
                        "containsInteger": "1",
                        "minValue": str(
                            metadata["min"]
                        ),
                        "maxValue": str(
                            metadata["max"]
                        ),
                    }
                )

        elif field.data_type == "number":

            metadata = cache.field_metadata[
                field.name
            ]

            ET.SubElement(
                cache_field,
                qname(MAIN_NS, "sharedItems"),
                {
                    "containsSemiMixedTypes": "0",
                    "containsString": "0",
                    "containsNumber": "1",
                    "containsInteger": "0",
                    "minValue": str(metadata["min"]),
                    "maxValue": str(metadata["max"]),
                }
            )

        else:

            ET.SubElement(
                cache_field,
                qname(MAIN_NS, "sharedItems")
            )

    return root


def cache_definition_xml(cache):

    root = generate_cache_definition(
        cache
    )

    return ET.tostring(
        root,
        encoding="utf-8",
        xml_declaration=True
    )