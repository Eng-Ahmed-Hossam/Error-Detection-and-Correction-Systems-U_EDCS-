import matplotlib.pyplot as plt

def visualize_hamming_code(codeword: str):
    """
    Visualize Hamming code bits, highlighting parity positions.
    """
    fig, ax = plt.subplots(figsize=(10, 1))
    ax.set_axis_off()

    for i, b in enumerate(codeword, start=1):
        is_parity = (i & (i - 1)) == 0  # power of 2 positions
        color = "lightgreen" if is_parity else "lightblue"
        label = f"P{i}" if is_parity else f"D{i}"
        ax.text(i, 0, f"{label}:{b}", ha="center", va="center", fontsize=12,
                bbox=dict(boxstyle="round,pad=0.3", fc=color, ec="black"))

    ax.set_xlim(0, len(codeword)+1)
    return fig