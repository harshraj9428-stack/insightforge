import os
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.pagesizes import letter

def generate_pdf(df, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    doc = SimpleDocTemplate(output_path, pagesize=letter)
    table_data = [df.columns.tolist()] + df.values.tolist()

    table = Table(table_data)
    doc.build([table])

    return output_path
