"""
Experiments and benchmarking utilities.
Class-based design for Monte Carlo simulations comparing error detection/correction schemes.

Author: Ahmed Hossam Mohamed Fekry
"""

import random
from typing import Dict, List
from core.parity import Parity
from core.parity2d import Parity2D
from core.hamming import Hamming
from core.crc import CRC
from core.checksum import Checksum
from core.channel import Channel


class ExperimentRunner:
    def __init__(self, block_size: int = 8, n_trials: int = 1000, channel_params: Dict = None):
        """
        Initialize experiment runner with default parameters.
        """
        self.block_size = block_size
        self.n_trials = n_trials
        self.channel_params = channel_params or {"p": 0.01, "burst_prob": 0.1, "max_burst_len": 3}

    def run_trial(self, data_bits: str, scheme: str) -> Dict[str, bool]:
        """
        Run a single trial for a given scheme.
        Returns dict with {detected, corrected}.
        """
        corrupted = None
        detected = False
        corrected = False

        if scheme == "parity":
            codeword = Parity.encode_even(data_bits)
            corrupted = Channel.simulate(codeword, **self.channel_params)
            detected = not Parity.validate_even(corrupted)

        elif scheme == "parity2d":
            matrix = [data_bits]  # simple 1-row demo
            codeword_matrix = Parity2D.encode(matrix)
            corrupted_matrix = [Channel.simulate(row, **self.channel_params) for row in codeword_matrix]
            check_result = Parity2D.check(corrupted_matrix)
            detected = not check_result["valid"]
            corrected = check_result["correctable"]

        elif scheme == "hamming":
            codeword = Hamming.encode(data_bits)
            corrupted = Channel.simulate(codeword, **self.channel_params)
            decoded, error_pos = Hamming.decode(corrupted)
            detected = (error_pos != 0)
            corrected = (decoded == data_bits)

        elif scheme == "crc":
            gen = "1011"  # default generator x^3 + x + 1
            crc = CRC(gen)
            codeword = crc.encode(data_bits)
            corrupted = Channel.simulate(codeword, **self.channel_params)
            detected = not crc.verify(corrupted)

        elif scheme == "checksum":
            checksum = Checksum.compute_checksum(data_bits)
            packet = data_bits + checksum
            corrupted = Channel.simulate(packet, **self.channel_params)
            detected = not Checksum.verify(corrupted)

        return {"detected": detected, "corrected": corrected}

    def monte_carlo(self, scheme: str) -> Dict[str, float]:
        """
        Run n_trials for given scheme.
        Returns detection and correction rates.
        """
        detected_count = 0
        corrected_count = 0

        for _ in range(self.n_trials):
            data_bits = "".join(random.choice("01") for _ in range(self.block_size))
            result = self.run_trial(data_bits, scheme)
            if result["detected"]:
                detected_count += 1
            if result["corrected"]:
                corrected_count += 1

        return {
            "scheme": scheme,
            "trials": self.n_trials,
            "detection_rate": detected_count / self.n_trials,
            "correction_rate": corrected_count / self.n_trials,
        }

    def benchmark(self, schemes: List[str]) -> List[Dict[str, float]]:
        """
        Run monte_carlo for each scheme and return results list.
        """
        return [self.monte_carlo(s) for s in schemes]