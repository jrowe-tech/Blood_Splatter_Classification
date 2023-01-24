from pdf_utils import PDF


def generate_pdf_example():
    pdf = PDF(path=r'../reports/sample.pdf')

    pdf.addLineText("Title", 300, 300, width=20, height=20)
    pdf.addHorizontalLine(200, thickness=0.2, margin=0.1)
    pdf.save()


if __name__ == "__main__":
    generate_pdf_example()
