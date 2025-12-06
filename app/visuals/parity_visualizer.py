import matplotlib.pyplot as plt

def visualize_parity_bits(bits: str, mode: str = "even"):
    """
    Visualize parity bit placement for a binary string.
    """
    fig, ax = plt.subplots(figsize=(8, 1))
    ax.set_axis_off()

    # Draw bits
    for i, b in enumerate(bits):
        ax.text(i, 0, b, ha="center", va="center", fontsize=14,
                bbox=dict(boxstyle="circle,pad=0.3", fc="lightblue", ec="black"))

    # Compute parity
    parity_bit = str((sum(int(b) for b in bits) % 2) ^ (mode == "odd"))
    ax.text(len(bits), 0, parity_bit, ha="center", va="center", fontsize=14,
            bbox=dict(boxstyle="circle,pad=0.3", fc="lightgreen", ec="black"))

    ax.set_xlim(-1, len(bits)+1)
    return fig