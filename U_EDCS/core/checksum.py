"""
core/checksum.py

Implements Internet-style checksum (1's complement addition)
Supports:
- 8-bit blocks
- 16-bit blocks
- 32-bit blocks

Functions:
- compute_checksum(bits, block_size)
- verify(bits, block_size)
- visualize_addition_process()

All inputs/outputs are binary strings.
Author: Ahmed Hossam Mohamed Fekry
"""

class Checksum:
    @staticmethod
    def _validate_bits(bits: str):
        if not isinstance(bits, str):
            raise TypeError("Input must be a binary string.")
        if any(c not in "01" for c in bits):
            raise ValueError("Binary string must contain only 0 and 1.")

    @staticmethod
    def _pad_bits(bits: str, block_size: int):
        """Pad with leading zeros to make length a multiple of block_size."""
        remainder = len(bits) % block_size
        if remainder != 0:
            bits = ("0" * (block_size - remainder)) + bits
        return bits

    @staticmethod
    def _split_blocks(bits: str, block_size: int):
        """Return list of blocks of size block_size."""
        return [bits[i:i+block_size] for i in range(0, len(bits), block_size)]

    @staticmethod
    def _ones_complement_add(a: str, b: str):
        """
        1's complement addition of two binary strings of equal length.
        If overflow occurs, wrap around the carry.
        """
        n = len(a)
        total = int(a, 2) + int(b, 2)
        # Wrap around the carry (end-around carry)
        if total >= (1 << n):
            total = (total + 1) & ((1 << n) - 1)
        return format(total, f"0{n}b")

    @staticmethod
    def compute_checksum(bits: str, block_size: int = 16):
        """
        Compute the Internet checksum for the given bits (binary string).
        block_size can be 8, 16, or 32 bits.
        Returns the checksum as a binary string.
        """
        Checksum._validate_bits(bits)
        if block_size not in (8, 16, 32):
            raise ValueError("block_size must be 8, 16, or 32.")

        bits = Checksum._pad_bits(bits, block_size)
        blocks = Checksum._split_blocks(bits, block_size)

        # Start with first block
        acc = blocks[0]
        # Add remaining blocks with 1's complement add
        for blk in blocks[1:]:
            acc = Checksum._ones_complement_add(acc, blk)

        # Final checksum = 1's complement
        checksum = "".join("1" if c == "0" else "0" for c in acc)
        return checksum

    @staticmethod
    def verify(bits_with_checksum: str, block_size: int = 16):
        """
        Verify the checksum by recomputing sum including checksum block.
        Returns True if valid.
        """
        Checksum._validate_bits(bits_with_checksum)
        bits = Checksum._pad_bits(bits_with_checksum, block_size)
        blocks = Checksum._split_blocks(bits, block_size)

        acc = blocks[0]
        for blk in blocks[1:]:
            acc = Checksum._ones_complement_add(acc, blk)

        # Valid if result is all 1's
        return all(c == "1" for c in acc)

    @staticmethod
    def visualize_addition(bits: str, block_size: int = 16):
        """
        Returns a detailed process of block additions for UI visualization.
        """
        Checksum._validate_bits(bits)
        bits = Checksum._pad_bits(bits, block_size)
        blocks = Checksum._split_blocks(bits, block_size)

        steps = []
        acc = blocks[0]

        for blk in blocks[1:]:
            before = acc
            after = Checksum._ones_complement_add(acc, blk)
            steps.append({
                "acc_before": before,
                "block": blk,
                "acc_after": after
            })
            acc = after

        checksum = "".join("1" if c == "0" else "0" for c in acc)

        return {
            "steps": steps,
            "final_sum": acc,
            "checksum": checksum
        }
    
    @staticmethod
    def compute_normal(bits: str, block_size: int = 16) -> str:
        """
        Compute a simple checksum (straight sum, no one's complement).
        Returns the FULL binary sum string (not truncated).
        """
        Checksum._validate_bits(bits)
        bits = Checksum._pad_bits(bits, block_size)
        blocks = Checksum._split_blocks(bits, block_size)

        total = sum(int(b, 2) for b in blocks)
        # Return full binary string (no truncation)
        return bin(total)[2:]
    
    @staticmethod
    def verify_normal(bits: str, checksum: str, block_size: int = 16) -> bool:
        """
        Verify simple checksum by recomputing sum and comparing.
        """
        Checksum._validate_bits(bits)
        Checksum._validate_bits(checksum)
        expected = Checksum.compute_normal(bits, block_size)
        return expected == checksum
