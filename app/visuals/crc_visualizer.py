import matplotlib.pyplot as plt

def visualize_crc_division(steps):
    """
    Visualize CRC division steps.
    """
    fig, ax = plt.subplots(figsize=(10, len(steps)*0.5))
    ax.axis("off")

    for idx, step in enumerate(steps):
        text = f"Step {step['step_index']}: {step['working_bits']}"
        if step["xor_mask"]:
            text += f" ⟶ XOR {step['xor_mask']} at {step['divided_at']}"
        ax.text(0, -idx, text, fontsize=10, va="top", family="monospace")

    return fig