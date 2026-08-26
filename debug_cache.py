from excelpivot.source import ExcelSource
from excelpivot.cache import PivotCache
from excelpivot.pivot import PivotTable

from excelpivot.ooxml.cache_definition import (
    cache_definition_xml
)

from excelpivot.ooxml.cache_records import (
    cache_records_xml
)

from excelpivot.ooxml.pivot_table import (
    pivot_table_definition_xml
)


source = ExcelSource(
    "reference/v1_simple.xlsx"
)

headers, records = source.read_table(
    "Table1"
)

cache = PivotCache(
    headers,
    records
)

pivot = PivotTable(
    cache=cache
)

pivot.set_source("Table1")

pivot.add_row("Region")
pivot.add_column("Product")
pivot.add_filter("Year")
pivot.add_value(
    "Revenue",
    "sum"
)


with open(
    "generated_pivotCacheDefinition.xml",
    "wb"
) as f:

    f.write(
        cache_definition_xml(cache)
    )


with open(
    "generated_pivotCacheRecords.xml",
    "wb"
) as f:

    f.write(
        cache_records_xml(
            cache,
            pivot
        )
    )


with open(
    "generated_pivotTable1.xml",
    "wb"
) as f:

    f.write(
        pivot_table_definition_xml(
            cache,
            pivot
        )
    )


print(
    "Generated all PivotTable XML files."
)