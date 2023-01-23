from pdf_utils import PDF

pdf = PDF()


def test_file_formatting():
    results = pdf.get_file_name(r"test/sample/bin.file")
    assert results == "bin"


def generate_pdf_example():
    pdf.addLineText("Title", 300, 300, width=20, height=20)
    pdf.save()


if __name__ == "__main__":
    generate_pdf_example()
