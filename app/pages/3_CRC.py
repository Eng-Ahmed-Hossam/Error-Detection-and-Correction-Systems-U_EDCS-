import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


import streamlit as st
from core.crc import CRC
from app.visuals.crc_visualizer import visualize_crc_division

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

st.set_page_config(page_title="CRC Error Detection", page_icon="🔹", layout="wide")

st.title("🔹 Cyclic Redundancy Check (CRC)")
st.markdown("### Encode, verify, and visualize CRC with binary or polynomial generators.")

# --- Input section ---
col1, col2 = st.columns([2,1])

with col1:
    data_bits = st.text_input("Enter binary data:", "11010011101100")
    gen_input = st.text_input("Enter generator (binary, polynomial string, or name):", "x^3 + x + 1")

    if st.button("Compute CRC"):
        try:
            crc = CRC(gen_input)
            remainder = crc.compute_remainder(data_bits)
            codeword = crc.encode(data_bits)

            st.write(f"**Generator normalized:** `{crc.generator}`")
            st.write(f"**Remainder:** `{remainder}`")
            st.write(f"**Codeword:** `{codeword}`")

            if crc.verify(codeword):
                st.success("✅ Codeword verified successfully.")
            else:
                st.error("❌ Verification failed.")

            # Visualizer integration
            steps = crc.visualize_division(data_bits)
            fig = visualize_crc_division(steps)
            st.pyplot(fig)

        except Exception as e:
            st.error(f"Error: {e}")

with col2:
    st.info("CRC is widely used in networking and storage systems for robust error detection.")