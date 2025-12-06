"""
core/parity.py

Implements Even and Odd Parity Encoding + Validation.
Input/Output format: binary string "101011"

Author: Ahmed Hossam Mohamed Fekry
"""

class Parity:
    @staticmethod
    def _validate_bits(bits: str):
        if not isinstance(bits, str):
            raise TypeError("Input must be a binary string.")
        if any(c not in "01" for c in bits):
            raise ValueError("Binary string must contain only 0 and 1.")

    @staticmethod
    def even_parity_bit(bits: str) -> str:
        """
        Returns the even parity bit for the given data bits.
        """
        Parity._validate_bits(bits)
        ones = bits.count("1")
        return "0" if ones % 2 == 0 else "1"

    @staticmethod
    def odd_parity_bit(bits: str) -> str:
        """
        Returns the odd parity bit for the given data bits.
        """
        Parity._validate_bits(bits)
        ones = bits.count("1")
        return "1" if ones % 2 == 0 else "0"

    @staticmethod
    def encode_even(bits: str) -> str:
        """
        Returns bits + even parity bit.
        """
        p = Parity.even_parity_bit(bits)
        return bits + p

    @staticmethod
    def encode_odd(bits: str) -> str:
        """
        Returns bits + odd parity bit.
        """
        p = Parity.odd_parity_bit(bits)
        return bits + p

    @staticmethod
    def validate_even(received: str) -> bool:
        """
        Returns True if even parity is valid.
        """
        Parity._validate_bits(received)
        ones = received.count("1")
        return ones % 2 == 0  # valid if even

    @staticmethod
    def validate_odd(received: str) -> bool:
        """
        Returns True if odd parity is valid.
        """
        Parity._validate_bits(received)
        ones = received.count("1")
        return ones % 2 == 1  # valid if odd
