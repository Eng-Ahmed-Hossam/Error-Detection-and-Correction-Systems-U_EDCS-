# U_EDCS – Unified Error Detection & Correction System

A Python toolkit with **Streamlit UI** for exploring and benchmarking **error detection and correction techniques**.  
Includes **Parity (1D & 2D)**, **Hamming codes**, **CRC**, **Checksums**, and **channel simulation** for random & burst errors. Also features an **Experiments module** for Monte Carlo simulations and performance benchmarking.

---
---
## ✨ Features

- **Parity**
  - Even & odd parity encoding/validation
  - 2D parity for row/column checks and single-bit correction
- **Hamming Codes**
  - General Hamming(n, k) codes
  - Syndrome calculation & single-bit error correction
- **CRC**
  - Supports binary, polynomial, and standard generators (CRC-8, CRC-16, CRC-32)
  - Step-by-step polynomial division visualization
- **Checksums**
  - 1’s complement and standard addition checksums
  - Supports 8, 16, 32-bit blocks
- **Channel Simulation**
  - Random bit flips & burst errors
- **Experiments**
  - Monte Carlo simulations
  - Detection/correction rate charts
  - Benchmarking across schemes

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- [Streamlit](https://streamlit.io)

### Installation
```bash
git clone https://github.com/ahmed/U_EDCS.git
cd U_EDCS
pip install -r requirements.txt

---

## 🎨 Visualizations

- **Parity bits** highlighted in encoded data
- **Hamming code layouts** showing error positions
- **CRC division steps** showing XOR masks
- **Checksum calculations** with intermediate sums

---

## 👨‍💻 Author

**Ahmed Hossam Mohamed Fekry**  
Focused on clarity, reproducibility, and portfolio-grade polish.

---

## 📜 License

MIT License — free to use, modify, and distribute.

---

## 📂 Project Structure

```text
U_EDCS/
│
├── core/                # Core modules
│   ├── parity.py
│   ├── parity2d.py
│   ├── hamming.py
│   ├── crc.py
│   ├── checksum.py
│   └── channel.py
│
├── app/                 # Streamlit app
│   ├── pages/
│   │   ├── 1_Parity.py
│   │   ├── 2_Hamming.py
│   │   ├── 3_CRC.py
│   │   ├── 4_Checksum.py
│   │   └── 5_Experiments.py
│   └── visuals/         # Visualization utilities
│
├── README.md
└── requirements.txt

---
