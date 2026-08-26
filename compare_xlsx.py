import zipfile


REFERENCE = "reference/v1_simple.xlsx"
GENERATED = "generated_pivot.xlsx"


def list_parts(path):

    with zipfile.ZipFile(path) as z:

        return set(z.namelist())


reference_parts = list_parts(
    REFERENCE
)

generated_parts = list_parts(
    GENERATED
)


print()
print("=" * 70)
print("PARTS ONLY IN REFERENCE")
print("=" * 70)

for part in sorted(
    reference_parts - generated_parts
):
    print(part)


print()
print("=" * 70)
print("PARTS ONLY IN GENERATED")
print("=" * 70)

for part in sorted(
    generated_parts - reference_parts
):
    print(part)


print()
print("=" * 70)
print("COMMON PARTS")
print("=" * 70)

common = (
    reference_parts
    & generated_parts
)

for part in sorted(common):
    print(part)