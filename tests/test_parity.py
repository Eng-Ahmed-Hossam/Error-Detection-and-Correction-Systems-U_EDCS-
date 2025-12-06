import pytest
from core.parity import Parity
from core.parity2d import Parity2D

# ------------------------------
# Tests for core/parity.py
# ------------------------------

def test_even_parity_bit():
    assert Parity.even_parity_bit("1010") == "0"   # 2 ones → even
    assert Parity.even_parity_bit("111") == "1"    # 3 ones → odd → parity bit 1

def test_odd_parity_bit():
    assert Parity.odd_parity_bit("1010") == "1"    # 2 ones → even → odd parity bit 1
    assert Parity.odd_parity_bit("111") == "0"     # 3 ones → odd → odd parity bit 0

def test_encode_even_and_validate():
    encoded = Parity.encode_even("1010")           # → "10100"
    assert encoded == "10100"
    assert Parity.validate_even(encoded) is True
    assert Parity.validate_even("10101") is False  # corrupted

def test_encode_odd_and_validate():
    encoded = Parity.encode_odd("1010")            # → "10101"
    assert encoded == "10101"
    assert Parity.validate_odd(encoded) is True
    assert Parity.validate_odd("10100") is False   # corrupted

def test_invalid_input_parity():
    with pytest.raises(ValueError):
        Parity.even_parity_bit("102")
    with pytest.raises(TypeError):
        Parity.even_parity_bit(1010)  # not a string


# ------------------------------
# Tests for core/parity2d.py
# ------------------------------

def test_encode_2d_parity_even():
    matrix = ["101", "010"]
    encoded = Parity2D.encode(matrix, mode="even", add_overall=True)
    # Each row gets a parity bit, plus final row for column parities (+ overall)
    assert len(encoded) == 3  # 2 rows + 1 parity row
    assert all(isinstance(row, str) for row in encoded)

def test_check_valid_matrix():
    matrix = ["101", "010"]
    encoded = Parity2D.encode(matrix, mode="even", add_overall=True)
    result = Parity2D.check(encoded, mode="even", has_overall=True)
    assert result["valid"] is True
    assert result["error_row"] is None
    assert result["error_col"] is None
    assert result["correctable"] is False

def test_single_bit_error_detection_and_correction():
    matrix = ["101", "010"]
    encoded = Parity2D.encode(matrix, mode="even", add_overall=True)

    # Introduce single-bit error in row 0, col 1
    corrupted = encoded.copy()
    corrupted[0] = corrupted[0][:1] + ("1" if corrupted[0][1] == "0" else "0") + corrupted[0][2:]

    check_result = Parity2D.check(corrupted, mode="even", has_overall=True)
    assert check_result["valid"] is False
    assert check_result["correctable"] is True
    assert check_result["error_row"] == 0
    assert check_result["error_col"] == 1

    corrected, info, success = Parity2D.correct(corrupted, mode="even")
    assert success is True
    assert Parity2D.check(corrected, mode="even", has_overall=True)["valid"] is True

def test_multiple_bit_error_uncorrectable():
    matrix = ["101", "010"]
    encoded = Parity2D.encode(matrix, mode="even", add_overall=True)

    # Introduce two errors
    corrupted = encoded.copy()
    corrupted[0] = corrupted[0][:0] + ("1" if corrupted[0][0] == "0" else "0") + corrupted[0][1:]
    corrupted[1] = corrupted[1][:1] + ("1" if corrupted[1][1] == "0" else "0") + corrupted[1][2:]

    check_result = Parity2D.check(corrupted, mode="even", has_overall=True)
    assert check_result["valid"] is False
    assert check_result["correctable"] is False

def test_invalid_matrix_input():
    with pytest.raises(ValueError):
        Parity2D.encode([], mode="even")
    with pytest.raises(ValueError):
        Parity2D.encode(["101", "10"], mode="even")  # inconsistent row lengths
    with pytest.raises(ValueError):
        Parity2D.encode(["10A"], mode="even")        # invalid character