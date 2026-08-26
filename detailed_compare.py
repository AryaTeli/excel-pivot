"""
Deep comparison between reference/v1_simple.xlsx and generated_pivot.xlsx
"""
import zipfile
import xml.etree.ElementTree as ET
import sys


REF = "reference/v1_simple.xlsx"
GEN = "generated_pivot.xlsx"


def get_xml_tree(z, filename):
    data = z.read(filename)
    return ET.fromstring(data)


def canonical_xml(element):
    # Sort attributes
    element.attrib = dict(sorted(element.attrib.items()))
    for child in element:
        canonical_xml(child)


with zipfile.ZipFile(REF) as ref_z, zipfile.ZipFile(GEN) as gen_z:
    ref_files = set(ref_z.namelist())
    gen_files = set(gen_z.namelist())

    print("=== MISSING FILES IN GENERATED ===")
    for f in sorted(ref_files - gen_files):
        print(" ", f)

    print("\n=== EXTRA FILES IN GENERATED ===")
    for f in sorted(gen_files - ref_files):
        print(" ", f)

    print("\n=== XML DIFFERENCES IN COMMON FILES ===")
    for f in sorted(ref_files & gen_files):
        if not f.endswith(".xml") and not f.endswith(".rels"):
            continue
        try:
            ref_tree = get_xml_tree(ref_z, f)
            gen_tree = get_xml_tree(gen_z, f)

            canonical_xml(ref_tree)
            canonical_xml(gen_tree)

            ref_str = ET.tostring(ref_tree, encoding="unicode")
            gen_str = ET.tostring(gen_tree, encoding="unicode")

            if ref_str != gen_str:
                print(f"\n--- DIFFERENCE IN {f} ---")
                print("REF:")
                print(" ", ref_str[:500])
                print("GEN:")
                print(" ", gen_str[:500])
            else:
                print(f"  {f}: MATCH")
        except Exception as e:
            print(f"  {f}: ERROR {e}")
