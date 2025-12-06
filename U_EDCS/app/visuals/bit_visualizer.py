import matplotlib.pyplot as plt

def visualize_bits(bits: str):
    """
    Visualize a binary string as blocks.
    """
    fig, ax = plt.subplots(figsize=(len(bits)*0.5, 1))
    ax.set_axis_off()

    for i, b in enumerate(bits):
        color = "lightblue" if b == "0" else "lightcoral"
        ax.text(i, 0, b, ha="center", va="center", fontsize=14,
                bbox=dict(boxstyle="circle,pad=0.3", fc=color, ec="black"))

    ax.set_xlim(-1, len(bits))
    return fig