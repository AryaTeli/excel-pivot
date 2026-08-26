"""
Analyze the generated XLSX without opening it in Excel.
Generates the xlsx, then compares each XML part with the reference.
"""
import zipfile
import xml.etree.ElementTree as ET
from io import BytesIO

from excelpivot.source import ExcelSource
from excelpivot.cache import PivotCache
from excelpivot.pivot import PivotTable
from excelpivot.package.xlsx import build_xlsx


# Build the workbook in memory by writing to file first
source = ExcelSource("reference/v1_simple.xlsx")
headers, records = source.read_table("Table1")

cache = PivotCache(headers, records)
pivot = PivotTable(cache=cache)
pivot.set_source("Table1")
pivot.add_row("Region")
pivot.add_column("Product")
pivot.add_filter("Year")
pivot.add_value("Revenue", "sum")

build_xlsx("generated_pivot.xlsx", headers, records, cache, pivot)

# Now compare
REFERENCE = "reference/v1_simple.xlsx"
GENERATED = "generated_pivot.xlsx"

PARTS = [
    "[Content_Types].xml",
    "_rels/.rels",
    "xl/workbook.xml",
    "xl/_rels/workbook.xml.rels",
    "xl/worksheets/sheet1.xml",
    "xl/worksheets/sheet2.xml",
    "xl/worksheets/_rels/sheet1.xml.rels",
    "xl/worksheets/_rels/sheet2.xml.rels",
    "xl/tables/table1.xml",
    "xl/pivotCache/pivotCacheDefinition1.xml",
    "xl/pivotCache/pivotCacheRecords1.xml",
    "xl/pivotCache/_rels/pivotCacheDefinition1.xml.rels",
    "xl/pivotTables/pivotTable1.xml",
    "xl/pivotTables/_rels/pivotTable1.xml.rels",
]


def read_part(path, part):
    with zipfile.ZipFile(path) as z:
        if part not in z.namelist():
            return None
        return z.read(part).decode("utf-8")


def list_all_parts(path):
    with zipfile.ZipFile(path) as z:
        return sorted(z.namelist())


def pretty_xml(xml_str):
    """Pretty-print XML for comparison."""
    try:
        root = ET.fromstring(xml_str)
        ET.indent(root)
        return ET.tostring(root, encoding="unicode")
    except ET.ParseError:
        return xml_str


print("=" * 80)
print("REFERENCE PARTS:")
print("=" * 80)
for p in list_all_parts(REFERENCE):
    print(f"  {p}")

print()
print("=" * 80)
print("GENERATED PARTS:")
print("=" * 80)
for p in list_all_parts(GENERATED):
    print(f"  {p}")

print()
print("=" * 80)
print("PART-BY-PART COMPARISON")
print("=" * 80)

for part in PARTS:
    ref = read_part(REFERENCE, part)
    gen = read_part(GENERATED, part)

    ref_status = "PRESENT" if ref else "MISSING"
    gen_status = "PRESENT" if gen else "MISSING"

    if ref_status != gen_status:
        print(f"\n{'='*80}")
        print(f"MISMATCH: {part}")
        print(f"  Reference: {ref_status}")
        print(f"  Generated: {gen_status}")
        print(f"{'='*80}")
        continue

    if ref is None and gen is None:
        continue

    # Compare the XML content (ignoring formatting differences)
    try:
        ref_pretty = pretty_xml(ref)
        gen_pretty = pretty_xml(gen)
        if ref_pretty == gen_pretty:
            print(f"\n  {part}: MATCH")
        else:
            print(f"\n{'='*80}")
            print(f"DIFF: {part}")
            print(f"{'='*80}")
            print(f"\n--- REFERENCE ---")
            print(ref_pretty[:3000])
            print(f"\n--- GENERATED ---")
            print(gen_pretty[:3000])
    except Exception as e:
        print(f"\n  {part}: ERROR comparing: {e}")


# Also check for parts in reference not in generated
print()
print("=" * 80)
print("PARTS IN REFERENCE BUT NOT IN GENERATED:")
print("=" * 80)
ref_parts = set(list_all_parts(REFERENCE))
gen_parts = set(list_all_parts(GENERATED))
for p in sorted(ref_parts - gen_parts):
    print(f"  MISSING: {p}")

print()
print("PARTS IN GENERATED BUT NOT IN REFERENCE:")
for p in sorted(gen_parts - ref_parts):
    print(f"  EXTRA: {p}")
