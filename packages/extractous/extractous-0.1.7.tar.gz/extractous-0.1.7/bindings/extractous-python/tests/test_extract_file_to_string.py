import pytest

from extractous import Extractor
from utils import cosine_similarity

TEST_CASES = [
    ("2022_Q3_AAPL.pdf", 0.9),
    ("science-exploration-1p.pptx", 0.9),
    ("simple.odt", 0.9),
    ("table-multi-row-column-cells-actual.csv", 0.9),
    ("vodafone.xlsx", 0.4),
    ("category-level.docx", 0.9),
    ("simple.doc", 0.9),
    ("simple.pptx", 0.9),
    ("table-multi-row-column-cells.png", -1.0),
    ("winter-sports.epub", 0.9),
    ("bug_16.docx", 0.9),
    ("deu-ocr.pdf", 0.9),
]

@pytest.mark.parametrize("file_name, target_dist", TEST_CASES)
def test_extract_file_to_string(file_name, target_dist):
    """Test the extraction and comparison of various file types."""
    original_filepath = f"../../test_files/documents/{file_name}"
    expected_result_filepath = f"../../test_files/expected_result/{file_name}.txt"
    extractor = Extractor()
    result = extractor.extract_file_to_string(original_filepath)
    with open(expected_result_filepath, "r",  encoding="utf8") as file:
        expected = file.read()
    
    assert cosine_similarity(result, expected) > target_dist, \
        f"Cosine similarity is less than {target_dist} for file: {file_name}"

