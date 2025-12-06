import streamlit as st
from core.parity import Parity
from core.parity2d import Parity2D
from app.visuals.parity_visualizer import visualize_parity_bits

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

st.set_page_config(page_title="Parity Error Detection", page_icon="🔹", layout="wide")

st.title("🔹 Parity Error Detection")
st.markdown("### Explore single-bit and two-dimensional parity with interactive visuals.")

# --- Single-bit parity section ---
st.header("Single-bit Parity")

bits = st.text_input("Enter binary data:", "1010101")
mode = st.radio("Parity mode:", ["even", "odd"], horizontal=True)

if st.button("Compute Parity"):
    try:
        if mode == "even":
            parity_bit = Parity.even_parity_bit(bits)
            encoded = Parity.encode_even(bits)
            valid = Parity.validate_even(encoded)
        else:
            parity_bit = Parity.odd_parity_bit(bits)
            encoded = Parity.encode_odd(bits)
            valid = Parity.validate_odd(encoded)

        st.write(f"**Parity bit:** `{parity_bit}`")
        st.write(f"**Encoded data:** `{encoded}`")

        if valid:
            st.success("✅ Data is valid with correct parity.")
        else:
            st.error("❌ Data failed parity check.")

        # Visualizer integration
        fig = visualize_parity_bits(bits, mode)
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error: {e}")

# --- 2D parity section ---
st.header("Two-Dimensional Parity")

st.write("Enter a matrix of bits (rows separated by commas, bits separated by spaces). Example: `1 0 1, 0 1 1, 1 1 0`")

matrix_input = st.text_area("Matrix input:", "1 0 1, 0 1 1, 1 1 0")

if st.button("Encode 2D Parity"):
    try:
        matrix = [row.strip().replace(" ", "") for row in matrix_input.split(",")]
        encoded_matrix = Parity2D.encode(matrix, mode=mode, add_overall=True)
        check_result = Parity2D.check(encoded_matrix, mode=mode, has_overall=True)

        st.write("### Encoded Matrix with Parity")
        st.table(encoded_matrix)

        if check_result["valid"]:
            st.success("✅ Matrix is valid.")
        elif check_result["correctable"]:
            st.warning(f"⚠️ Single-bit error detected at row {check_result['error_row']}, col {check_result['error_col']}. Attempting correction...")
            corrected, info, success = Parity2D.correct(encoded_matrix, mode=mode)
            if success:
                st.success("✅ Error corrected successfully.")
                st.table(corrected)
            else:
                st.error("❌ Correction failed.")
        else:
            st.error("❌ Multiple or uncorrectable errors detected.")

    except Exception as e:
        st.error(f"Error parsing matrix: {e}")