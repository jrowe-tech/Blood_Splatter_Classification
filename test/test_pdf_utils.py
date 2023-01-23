from pdf_utils import PDF

pdf = PDF()


def test_file_formatting():
    results = pdf.get_file_name(r"test/sample/bin.file")
    assert results == "bin"
