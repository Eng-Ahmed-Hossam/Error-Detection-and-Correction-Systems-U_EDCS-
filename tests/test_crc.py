import pytest
from core.crc import CRC

# ------------------------------
# Basic CRC tests
# ------------------------------

def test_crc_remainder_example():
    """
    Example from Forouzan: data = 11010011101100, generator = 1011 (x^3 + x + 1).
    Expected remainder is "100" (Figure 10.15).
    """
    crc = CRC("1011")
    data = "11010011101100"
    remainder = crc.compute_remainder(data)
    assert remainder == "100"

def test_crc_encode_and_verify():
    crc = CRC("1011")
    data = "11010011101100"
    codeword = crc.encode(data)
    assert crc.verify(codeword) is True

    # Flip one bit to corrupt
    corrupted = list(codeword)
    corrupted[5] = "1" if corrupted[5] == "0" else "0"
    corrupted = "".join(corrupted)
    assert crc.verify(corrupted) is False

def test_crc_with_polynomial_string():
    """
    Polynomial string form should be parsed correctly.
    "x^3 + x + 1" -> binary "1011".
    """
    crc = CRC("x^3 + x + 1")
    data = "11010011101100"
    remainder = crc.compute_remainder(data)
    assert remainder == "100"
    codeword = crc.encode(data)
    assert crc.verify(codeword) is True

def test_crc_with_standard_polynomial():
    """
    Standard named polynomial should normalize to binary bits.
    """
    crc = CRC("crc-8")
    data = "10101010"
    codeword = crc.encode(data)
    assert crc.verify(codeword) is True

# ------------------------------
# Visualization tests
# ------------------------------

def test_visualize_division_steps():
    crc = CRC("1011")
    data = "11010011101100"
    steps = crc.visualize_division(data)
    assert isinstance(steps, list)
    assert "step_index" in steps[0]
    assert "working_bits" in steps[0]
    assert "xor_mask" in steps[0]

# ------------------------------
# Edge cases
# ------------------------------

def test_invalid_data_bits():
    crc = CRC("1011")
    with pytest.raises(ValueError):
        crc.compute_remainder("10201")

def test_invalid_generator():
    with pytest.raises(ValueError):
        CRC("abc")

def test_empty_data_bits():
    crc = CRC("1011")
    data = ""
    remainder = crc.compute_remainder(data)
    # For empty data, remainder should be zeros of length len(gen)-1
    assert remainder == "000"