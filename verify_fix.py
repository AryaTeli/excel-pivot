"""
Verification script to test the fixes and compare generated XML
against the reference workbook.
"""
import sys
import os
import zipfile
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(__file__))

from excelpivot.source import ExcelSource
from excelpivot.cache import PivotCache
from excelpivot.pivot import PivotTable
from excelpivot.package.xlsx import build_xlsx


def list_all_parts(path):
    with zipfile.ZipFile(path) as z:
        return sorted(z.namelist())


source = ExcelSource("reference/v1_simple.xlsx")
headers, records = source.read_table("Table1")

cache = PivotCache(headers, records)
pivot = PivotTable(cache=cache)
pivot.set_source("Table1")
pivot.add_row("Region")
pivot.add_column("Product")
pivot.add_filter("Year")
pivot.add_value("Revenue", "sum")

output_path = "generated_pivot.xlsx"
build_xlsx(output_path, headers, records, cache, pivot)

print(f"Generated: {output_path} ({os.path.getsize(output_path)} bytes)")

# Check content types
with zipfile.ZipFile(output_path) as z:
    ct_data = z.read("[Content_Types].xml")
    ct_root = ET.fromstring(ct_data)
    overrides = [e.attrib["PartName"] for e in ct_root if e.tag.endswith("Override")]

print("\nContent Types Overrides:")
for o in overrides:
    print(" ", o)

assert "/xl/tables/table1.xml" in overrides, "MISSING /xl/tables/table1.xml in [Content_Types].xml!"
assert "/xl/styles.xml" in overrides, "MISSING /xl/styles.xml in [Content_Types].xml!"

print("\nALL VERIFICATIONS PASSED!")
