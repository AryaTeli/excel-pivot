import zipfile


REFERENCE = "reference/v1_simple.xlsx"
GENERATED = "generated_pivot.xlsx"


PARTS = [
    "xl/workbook.xml",
    "xl/_rels/workbook.xml.rels",

    "xl/worksheets/sheet1.xml",
    "xl/worksheets/sheet2.xml",

    "xl/worksheets/_rels/sheet2.xml.rels",

    "xl/pivotCache/pivotCacheDefinition1.xml",
    "xl/pivotCache/pivotCacheRecords1.xml",

    "xl/pivotTables/pivotTable1.xml",
]


def read_part(path, part):

    with zipfile.ZipFile(path) as z:

        if part not in z.namelist():

            return None

        return z.read(part).decode(
            "utf-8"
        )


for part in PARTS:

    print()
    print("=" * 80)
    print(part)
    print("=" * 80)

    reference = read_part(
        REFERENCE,
        part
    )

    generated = read_part(
        GENERATED,
        part
    )

    print()
    print("REFERENCE:")
    print()

    if reference is None:
        print("[MISSING]")
    else:
        print(reference)

    print()
    print("GENERATED:")
    print()

    if generated is None:
        print("[MISSING]")
    else:
        print(generated)