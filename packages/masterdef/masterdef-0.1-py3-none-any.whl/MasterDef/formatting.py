from openpyxl import load_workbook

def autofit_columns(filename):
    wb = load_workbook(filename)
    sheet = wb.active

    for column_cells in sheet.columns:
        length = max(len(str(cell.value)) for cell in column_cells if cell.value is not None)
        sheet.column_dimensions[column_cells[0].column_letter].width = length + 2  # Adding padding

    wb.save(filename)
