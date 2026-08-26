from openpyxl import load_workbook


class ExcelSource:
    def __init__(self, filename):
        self.filename = filename

    def read_table(self, table_name):
        wb = load_workbook(
            self.filename,
            data_only=False
        )

        for ws in wb.worksheets:

            if table_name not in ws.tables:
                continue

            table = ws.tables[table_name]

            rows = ws[table.ref]

            headers = [
                cell.value
                for cell in rows[0]
            ]

            records = [
                tuple(cell.value for cell in row)
                for row in rows[1:]
            ]

            return headers, records

        raise ValueError(
            f"Table not found: {table_name}"
        )