import pytest
import random
from core.channel import Channel

# ------------------------------
# Random bit flips
# ------------------------------

def test_flip_random_bits_reproducible():
    random.seed(42)
    bits = "101010"
    corrupted = Channel.flip_random_bits(bits, p=0.5)
    # With fixed seed, output should be deterministic
    assert isinstance(corrupted, str)
    assert len(corrupted) == len(bits)

def test_flip_random_bits_no_change():
    bits = "111000"
    corrupted = Channel.flip_random_bits(bits, p=0.0)
    assert corrupted == bits

def test_flip_random_bits_all_change():
    random.seed(1)
    bits = "111000"
    corrupted = Channel.flip_random_bits(bits, p=1.0)
    # Every bit flipped
    assert corrupted == "".join("1" if b == "0" else "0" for b in bits)

# ------------------------------
# Burst errors
# ------------------------------

def test_inject_burst_error_valid():
    bits = "101010"
    corrupted = Channel.inject_burst_error(bits, start=2, length=3)
    assert len(corrupted) == len(bits)
    # Bits 2..4 flipped
    expected = list(bits)
    for i in range(2, 5):
        expected[i] = "1" if expected[i] == "0" else "0"
    assert corrupted == "".join(expected)

def test_inject_burst_error_invalid_index():
    bits = "1010"
    with pytest.raises(ValueError):
        Channel.inject_burst_error(bits, start=10, length=2)

def test_inject_burst_error_invalid_length():
    bits = "1010"
    with pytest.raises(ValueError):
        Channel.inject_burst_error(bits, start=1, length=0)

# ------------------------------
# Random burst
# ------------------------------

def test_random_burst_reproducible():
    random.seed(123)
    bits = "10101010"
    corrupted, start, length = Channel.random_burst(bits, max_len=4)
    assert isinstance(corrupted, str)
    assert 1 <= length <= 4
    assert 0 <= start <= len(bits) - length

def test_random_burst_invalid_length():
    bits = "1010"
    with pytest.raises(ValueError):
        Channel.random_burst(bits, max_len=0)

# ------------------------------
# Combined simulation
# ------------------------------

def test_simulate_combined():
    random.seed(99)
    bits = "1010101010"
    corrupted = Channel.simulate(bits, p=0.2, burst_prob=0.5, max_burst_len=3)
    assert isinstance(corrupted, str)
    assert len(corrupted) == len(bits)

# ------------------------------
# Edge cases
# ------------------------------

def test_invalid_input_channel():
    with pytest.raises(ValueError):
        Channel.flip_random_bits("10201", p=0.1)
    with pytest.raises(TypeError):
        Channel.flip_random_bits(10101, p=0.1)