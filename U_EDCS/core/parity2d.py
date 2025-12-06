"""
core/parity2d.py

Implements Two-Dimensional Parity (2D Parity) for block error detection.
Supports:
- Row parity generation
- Column parity generation
- Optional overall parity bit
- Checking & locating errors
- Single-bit correction

Input/Output:
A matrix of bits is represented as a list of strings, e.g.:
[
    "10101",
    "11000",
    "00111"
]
"""

class Parity2D:
    @staticmethod
    def _validate_matrix(matrix):
        if not isinstance(matrix, list) or not matrix:
            raise ValueError("Matrix must be a non-empty list of bit-strings.")

        width = len(matrix[0])
        for row in matrix:
            if len(row) != width:
                raise ValueError("All rows must be the same length.")
            if any(c not in "01" for c in row):
                raise ValueError("Matrix contains invalid characters (only 0/1 allowed).")

    @staticmethod
    def _parity_bit(bits, mode="even"):
        ones = bits.count("1")
        if mode == "even":
            return "0" if ones % 2 == 0 else "1"
        else:
            return "1" if ones % 2 == 0 else "0"

    @staticmethod
    def encode(matrix, mode="even", add_overall=True):
        """
        Returns the encoded 2D parity matrix including:
        - Row parity bits appended to each row
        - Final row containing column parity bits (+ overall parity)
        """
        Parity2D._validate_matrix(matrix)

        rows = len(matrix)
        cols = len(matrix[0])

        # Add row parity
        encoded = []
        for row in matrix:
            p = Parity2D._parity_bit(row, mode)
            encoded.append(row + p)

        # Compute column parities (including row parity bits column)
        total_cols = cols + 1
        col_parity_row = ""
        for c in range(total_cols):
            col_bits = "".join(encoded[r][c] for r in range(rows))
            col_parity_row += Parity2D._parity_bit(col_bits, mode)

        # Add overall parity (optional)
        if add_overall:
            flattened = "".join(encoded) + col_parity_row
            p_overall = Parity2D._parity_bit(flattened, mode)
            col_parity_row += p_overall

        encoded.append(col_parity_row)
        return encoded

    @staticmethod
    def check(encoded, mode="even", has_overall=True):
        """
        Checks a received 2D parity matrix.
        Returns:
        {
            "valid": bool,
            "error_row": index or None,
            "error_col": index or None,
            "correctable": bool
        }
        """
        Parity2D._validate_matrix(encoded[:-1])  # except final row

        rows = len(encoded) - 1
        cols = len(encoded[0])

        # Check row parity
        row_errors = []
        for r in range(rows):
            row = encoded[r]
            p_expected = Parity2D._parity_bit(row[:-1], mode)
            if p_expected != row[-1]:
                row_errors.append(r)

        # Check column parity
        col_errors = []
        total_cols = cols if has_overall else cols - 1
        for c in range(total_cols - 1):  # exclude overall bit column
            col_bits = "".join(encoded[r][c] for r in range(rows))
            expected = Parity2D._parity_bit(col_bits, mode)
            if expected != encoded[rows][c]:
                col_errors.append(c)

        # Determine if correctable single-bit error
        if len(row_errors) == 1 and len(col_errors) == 1:
            return {
                "valid": False,
                "error_row": row_errors[0],
                "error_col": col_errors[0],
                "correctable": True
            }

        # No errors
        if not row_errors and not col_errors:
            return {
                "valid": True,
                "error_row": None,
                "error_col": None,
                "correctable": False
            }

        # Multiple or uncorrectable errors
        return {
            "valid": False,
            "error_row": None,
            "error_col": None,
            "correctable": False
        }

    @staticmethod
    def correct(encoded, mode="even"):
        """
        Attempts to correct a single-bit error.
        Returns the corrected matrix and info.
        """
        check_result = Parity2D.check(encoded, mode)

        if not check_result["correctable"]:
            return encoded, check_result, False

        r = check_result["error_row"]
        c = check_result["error_col"]

        corrected = [list(row) for row in encoded]
        corrected[r][c] = "1" if corrected[r][c] == "0" else "0"
        corrected = ["".join(row) for row in corrected]

        return corrected, check_result, True
