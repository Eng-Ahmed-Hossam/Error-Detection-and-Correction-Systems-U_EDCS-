"""
Channel simulation utilities.
Simulates random errors, burst errors, and noise models for testing error detection/correction codes.

Features:
- flip_random_bits(bits, p) -> flips each bit with probability p
- inject_burst_error(bits, start, length) -> flips a contiguous block of bits
- random_burst(bits, max_len) -> injects a burst of random length/location
- simulate(bits, p, burst_prob, max_burst_len) -> combined noise model

Input/Output: binary strings (e.g. "1011001")

Author: Ahmed Hossam Mohamed Fekry
"""

import random
from typing import Tuple

class Channel:
    @staticmethod
    def _validate_bits(bits: str):
        if not isinstance(bits, str):
            raise TypeError("Input must be a binary string.")
        if any(c not in "01" for c in bits):
            raise ValueError("Binary string must contain only 0 and 1.")

    @staticmethod
    def flip_random_bits(bits: str, p: float = 0.01) -> str:
        """
        Flip each bit with independent probability p.
        """
        Channel._validate_bits(bits)
        out = []
        for b in bits:
            if random.random() < p:
                out.append("1" if b == "0" else "0")
            else:
                out.append(b)
        return "".join(out)

    @staticmethod
    def inject_burst_error(bits: str, start: int, length: int) -> str:
        """
        Flip a contiguous block of bits starting at 'start' of given 'length'.
        """
        Channel._validate_bits(bits)
        if start < 0 or start >= len(bits):
            raise ValueError("Invalid start index.")
        if length <= 0:
            raise ValueError("Length must be positive.")
        end = min(start + length, len(bits))
        out = list(bits)
        for i in range(start, end):
            out[i] = "1" if out[i] == "0" else "0"
        return "".join(out)

    @staticmethod
    def random_burst(bits: str, max_len: int = 5) -> Tuple[str, int, int]:
        """
        Inject a burst error of random length (1..max_len) at a random position.
        Returns (corrupted_bits, start, length).
        """
        Channel._validate_bits(bits)
        if max_len <= 0:
            raise ValueError("max_len must be positive.")
        length = random.randint(1, max_len)
        start = random.randint(0, len(bits) - length)
        corrupted = Channel.inject_burst_error(bits, start, length)
        return corrupted, start, length

    @staticmethod
    def simulate(bits: str, p: float = 0.01, burst_prob: float = 0.1, max_burst_len: int = 5) -> str:
        """
        Combined noise model:
        - Flip random bits with probability p
        - With probability burst_prob, inject a random burst error
        """
        Channel._validate_bits(bits)
        corrupted = Channel.flip_random_bits(bits, p)
        if random.random() < burst_prob:
            corrupted, _, _ = Channel.random_burst(corrupted, max_burst_len)
        return corrupted