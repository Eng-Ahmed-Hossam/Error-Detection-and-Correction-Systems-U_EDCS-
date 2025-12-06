import pytest
from core.checksum import Checksum

# ------------------------------
# Tests for Internet checksum
# ------------------------------

def test_internet_checksum_valid():
    # Example: 16-bit blocks
    data = "11100110011001101101010101010101"  # 32 bits
    checksum = Checksum.compute_checksum(data, block_size=16)
    packet = data + checksum
    assert Checksum.verify(packet, block_size=16) is True

def test_internet_checksum_invalid():
    data = "11100110011001101101010101010101"
    checksum = Checksum.compute_checksum(data, block_size=16)
    packet = data + checksum
    # Flip one bit to corrupt
    corrupted = packet[:-1] + ("1" if packet[-1] == "0" else "0")
    assert Checksum.verify(corrupted, block_size=16) is False

def test_internet_checksum_visualization():
    data = "11100110011001101101010101010101"
    viz = Checksum.visualize_addition(data, block_size=16)
    assert "steps" in viz
    assert "final_sum" in viz
    assert "checksum" in viz
    assert isinstance(viz["steps"], list)


# ------------------------------
# Tests for Normal checksum
# ------------------------------

def test_normal_checksum_valid():
    # Example 10.18: numbers (7, 11, 12, 0, 6)
    # Binary strings for 4-bit blocks
    data = "0111" + "1011" + "1100" + "0000" + "0110"  # 7,11,12,0,6
    checksum = Checksum.compute_normal(data, block_size=4)
    # Expected sum = 36 → binary "100100"
    assert checksum == "100100"
    assert Checksum.verify_normal(data, checksum, block_size=4) is True

def test_normal_checksum_invalid():
    data = "0111" + "1011" + "1100" + "0000" + "0110"
    checksum = Checksum.compute_normal(data, block_size=4)
    # Corrupt checksum
    bad_checksum = "000000"
    assert Checksum.verify_normal(data, bad_checksum, block_size=4) is False


# ------------------------------
# Edge cases
# ------------------------------

def test_invalid_input_checksum():
    with pytest.raises(ValueError):
        Checksum.compute_checksum("102", block_size=16)
    with pytest.raises(TypeError):
        Checksum.compute_checksum(1010, block_size=16)

def test_invalid_block_size():
    with pytest.raises(ValueError):
        Checksum.compute_checksum("1010", block_size=12)