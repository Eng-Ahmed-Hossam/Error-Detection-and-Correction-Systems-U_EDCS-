import streamlit as st
from core.hamming import Hamming
from app.visuals.hamming_visualizer import visualize_hamming_code

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

st.set_page_config(page_title="Hamming Code", page_icon="🔹", layout="wide")

st.title("🔹 General Hamming Code")
st.markdown("### Encode data into Hamming code, detect and correct single-bit errors interactively.")

# --- Input section ---
data_bits = st.text_input("Enter data bits (e.g. 1011):", "1011")

if st.button("Encode"):
    try:
        encoded = Hamming.encode(data_bits)
        st.write(f"**Encoded codeword:** `{encoded}`")

        # Visualizer integration
        fig = visualize_hamming_code(encoded)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Encoding error: {e}")

# --- Error simulation ---
st.subheader("Simulate Transmission Errors")

error_pos = st.number_input("Enter error position (1-based index):", min_value=1, max_value=len(data_bits)+Hamming._calculate_r(len(data_bits)), value=1)

if st.button("Inject Error"):
    try:
        encoded = Hamming.encode(data_bits)
        corrupted = list(encoded)
        corrupted[error_pos-1] = "1" if corrupted[error_pos-1] == "0" else "0"
        corrupted = "".join(corrupted)

        st.write(f"**Corrupted codeword:** `{corrupted}`")

        corrected_data, syndrome = Hamming.decode(corrupted)

        if syndrome == 0:
            st.success(f"✅ No error detected. Data bits: `{corrected_data}`")
        else:
            st.warning(f"⚠️ Error detected at position {syndrome}. Corrected data bits: `{corrected_data}`")

        # Visualizer integration for corrupted codeword
        fig = visualize_hamming_code(corrupted)
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error simulation failed: {e}")