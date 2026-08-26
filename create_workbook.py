from excelpivot.source import ExcelSource
from excelpivot.cache import PivotCache
from excelpivot.pivot import PivotTable

from excelpivot.package.xlsx import (
    build_xlsx
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


build_xlsx(
    "generated_pivot.xlsx",
    headers,
    records,
    cache,
    pivot
)

print(
    "Created generated_pivot.xlsx"
)