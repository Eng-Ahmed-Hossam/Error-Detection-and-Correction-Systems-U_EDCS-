"""
core/crc.py

Cyclic Redundancy Check utilities (class-based).

Features:
- Parse generator polynomials from binary string or polynomial notation.
- Compute CRC remainder via bitwise polynomial long division.
- Encode and verify codewords.
- Visualize division steps for UI animation.
- Includes common standard polynomials.

Input/output: binary strings (e.g. "1011001")

Author: Ahmed Hossam Mohamed Fekry
"""

from typing import List, Dict
import re

class CRC:
    # ----- Standard generator polynomials (binary string form) -----
    STANDARD_POLYNOMIALS: Dict[str, str] = {
        "crc-8":       "100000111",   # x^8 + x^2 + x + 1
        "crc-16-ccitt":"10001000000100001",  # x^16 + x^12 + x^5 + 1
        "crc-16":      "11000000000000101",  # placeholder
        "crc-32":      "100000100110000010001110110110111"  # IEEE 802.3
    }

    def __init__(self, generator: str):
        """Initialize CRC with a generator (binary string, polynomial string, or named)."""
        self.generator = self.normalize_gen(generator)
        self.gen_bits = self.bits_from_str(self.generator)
        self.n = len(self.generator)

    # -------------------------
    # Utilities
    # -------------------------
    @staticmethod
    def gen_bits_from_poly_string(poly: str) -> str:
        poly = poly.replace(" ", "").lower()
        exps = []
        for m in re.finditer(r"x\^(\d+)", poly):
            exps.append(int(m.group(1)))
        if re.search(r"(^|[+\-])x($|[+\-])", poly):
            exps.append(1)
        if re.search(r"(^|[+\-])1($|[+\-])", poly):
            exps.append(0)
        if not exps:
            raise ValueError(f"Could not parse polynomial string: {poly}")
        max_deg = max(exps)
        bits = ["1" if d in exps else "0" for d in range(max_deg, -1, -1)]
        return "".join(bits)

    @classmethod
    def normalize_gen(cls, gen: str) -> str:
        if not isinstance(gen, str):
            raise TypeError("Generator must be a string.")
        g = gen.strip().lower()
        if g in cls.STANDARD_POLYNOMIALS:
            return cls.STANDARD_POLYNOMIALS[g]
        if "x" in g or "^" in g:
            return cls.gen_bits_from_poly_string(g)
        if all(c in "01" for c in g):
            if len(g) < 2:
                raise ValueError("Generator binary string must be at least length 2")
            return g
        raise ValueError(f"Unrecognized generator format: {gen}")

    @staticmethod
    def bits_from_str(s: str) -> List[int]:
        return [1 if c == "1" else 0 for c in s]

    @staticmethod
    def str_from_bits(bits: List[int]) -> str:
        return "".join("1" if b else "0" for b in bits)

    @staticmethod
    def _xor_slice(a: List[int], b: List[int], start: int) -> None:
        for i in range(len(b)):
            a[start + i] ^= b[i]

    # -------------------------
    # Core CRC algorithms
    # -------------------------
    def compute_remainder(self, data_bits: str) -> str:
        if any(c not in "01" for c in data_bits):
            raise ValueError("data_bits must be binary string")
        data = self.bits_from_str(data_bits) + [0] * (self.n - 1)
        for i in range(len(data_bits)):
            if data[i] == 1:
                self._xor_slice(data, self.gen_bits, i)
        remainder = data[-(self.n - 1):] if self.n > 1 else []
        return self.str_from_bits(remainder)

    def encode(self, data_bits: str) -> str:
        rem = self.compute_remainder(data_bits)
        return data_bits + rem

    def verify(self, received_bits: str) -> bool:
        if any(c not in "01" for c in received_bits):
            raise ValueError("received_bits must be binary string")
        data = self.bits_from_str(received_bits)
        for i in range(len(received_bits) - (self.n - 1)):
            if data[i] == 1:
                self._xor_slice(data, self.gen_bits, i)
        rem = data[-(self.n - 1):] if self.n > 1 else []
        return all(b == 0 for b in rem)

    def visualize_division(self, data_bits: str) -> List[dict]:
        if any(c not in "01" for c in data_bits):
            raise ValueError("data_bits must be binary string")
        data = self.bits_from_str(data_bits) + [0] * (self.n - 1)
        steps = []
        for i in range(len(data_bits)):
            step = {
                "step_index": i,
                "working_bits": self.str_from_bits(data),
                "divided_at": None,
                "xor_mask": None
            }
            if data[i] == 1:
                step["divided_at"] = i
                step["xor_mask"] = self.generator
                self._xor_slice(data, self.gen_bits, i)
            steps.append(step)
        steps.append({
            "step_index": len(data_bits),
            "working_bits": self.str_from_bits(data),
            "divided_at": None,
            "xor_mask": None
        })
        return steps


if __name__ == "__main__":
    # Quick demo
    crc = CRC("x^3 + x + 1")  # generator polynomial
    data = "11010011101100"
    print("data:", data)
    print("generator:", crc.generator)
    rem = crc.compute_remainder(data)
    print("remainder:", rem)
    cw = crc.encode(data)
    print("codeword:", cw)
    print("verify(codeword):", crc.verify(cw))