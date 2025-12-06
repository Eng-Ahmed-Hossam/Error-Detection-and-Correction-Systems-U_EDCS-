"""
General Hamming Code implementation.
Supports arbitrary Hamming(n, k) codes where n = 2^r - 1 and k = n - r.

Features:
- encode(data_bits) -> codeword
- decode(received_bits) -> (corrected_data_bits, error_position)
- syndrome calculation
- single-bit error correction

Input/Output: binary strings (e.g. "1011")

Author: Ahmed Hossam Mohamed Fekry
"""

from typing import Tuple

class Hamming:
    @staticmethod
    def _validate_bits(bits: str):
        if not isinstance(bits, str):
            raise TypeError("Input must be a binary string.")
        if any(c not in "01" for c in bits):
            raise ValueError("Binary string must contain only 0 and 1.")

    @staticmethod
    def _calculate_r(k: int) -> int:
        """
        Find number of parity bits r such that 2^r >= k + r + 1.
        """
        r = 1
        while (2**r) < (k + r + 1):
            r += 1
        return r

    @staticmethod
    def encode(data_bits: str) -> str:
        """
        Encode data_bits using Hamming code.
        Returns codeword with parity bits inserted at positions 1,2,4,8,...
        """
        Hamming._validate_bits(data_bits)
        k = len(data_bits)
        r = Hamming._calculate_r(k)
        n = k + r

        # Place data bits into codeword (skip parity positions)
        codeword = ["0"] * (n + 1)  # 1-indexed for clarity
        j = 0
        for i in range(1, n+1):
            if (i & (i-1)) == 0:  # power of 2 → parity position
                continue
            codeword[i] = data_bits[j]
            j += 1

        # Calculate parity bits
        for p in range(r):
            pos = 2**p
            parity = 0
            for i in range(1, n+1):
                if i & pos:
                    parity ^= int(codeword[i])
            codeword[pos] = str(parity)

        return "".join(codeword[1:])  # drop index 0

    @staticmethod
    def decode(received_bits: str) -> Tuple[str, int]:
        """
        Decode received_bits, correct single-bit error if present.
        Returns (corrected_data_bits, error_position).
        error_position = 0 if no error, else index of corrected bit.
        """
        Hamming._validate_bits(received_bits)
        n = len(received_bits)
        r = 0
        while (2**r) <= n:
            r += 1
        r -= 1
        codeword = ["0"] + list(received_bits)  # 1-indexed

        # Compute syndrome
        syndrome = 0
        for p in range(r):
            pos = 2**p
            parity = 0
            for i in range(1, n+1):
                if i & pos:
                    parity ^= int(codeword[i])
            if parity != 0:
                syndrome += pos

        # Correct error if syndrome != 0
        if syndrome != 0 and syndrome <= n:
            codeword[syndrome] = "1" if codeword[syndrome] == "0" else "0"

        # Extract data bits (skip parity positions)
        data_bits = []
        for i in range(1, n+1):
            if (i & (i-1)) == 0:  # parity positions
                continue
            data_bits.append(codeword[i])

        return "".join(data_bits), syndrome