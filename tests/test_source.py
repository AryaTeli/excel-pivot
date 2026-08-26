from excelpivot.source import ExcelSource


def test_read_table():

    source = ExcelSource(
        "reference/v1_simple.xlsx"
    )

    headers, records = source.read_table("Table1")

    assert headers == [
        "Region",
        "Product",
        "Year",
        "Revenue",
        "Quantity"
    ]

    assert len(records) == 10

    assert records[0] == (
        "North",
        "Laptop",
        2025,
        10000,
        10
    )