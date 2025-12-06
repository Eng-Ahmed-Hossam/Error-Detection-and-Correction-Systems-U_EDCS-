import streamlit as st
from core.checksum import Checksum
from app.visuals.bit_visualizer import visualize_bits

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

st.set_page_config(page_title="Checksum Error Detection", page_icon="🔹", layout="wide")

st.title("🔹 Checksum Error Detection")
st.markdown("### Compute and verify checksums using Internet and normal methods with visual feedback.")

# --- Input section ---
col1, col2 = st.columns([2,1])

with col1:
    data_bits = st.text_input("Enter binary data:", "1010101010101010")
    method = st.radio("Checksum method:", ["internet", "normal"], horizontal=True)
    block_size = st.selectbox("Block size:", [8, 16, 32], index=1)

    if st.button("Compute Checksum"):
        try:
            if method == "internet":
                checksum = Checksum.compute_checksum(data_bits, block_size)
                valid = Checksum.verify(data_bits + checksum, block_size)
                st.write(f"**Internet checksum:** `{checksum}`")
            else:
                checksum = Checksum.compute_normal(data_bits, block_size)
                valid = Checksum.verify_normal(data_bits, checksum, block_size)
                st.write(f"**Normal checksum:** `{checksum}`")

            if valid:
                st.success("✅ Data verified successfully with checksum.")
            else:
                st.error("❌ Verification failed.")

            # Visualizer integration
            if method == "internet":
                steps_info = Checksum.visualize_addition(data_bits, block_size)
                st.write("### Addition Steps")
                for step in steps_info["steps"]:
                    st.write(f"Acc before: `{step['acc_before']}`, Block: `{step['block']}`, Acc after: `{step['acc_after']}`")
                st.write(f"**Final sum:** `{steps_info['final_sum']}`")
                st.write(f"**Checksum:** `{steps_info['checksum']}`")

            fig = visualize_bits(data_bits + checksum)
            st.pyplot(fig)

        except Exception as e:
            st.error(f"Error: {e}")

with col2:
    st.info("Checksums are widely used in networking (IP, TCP/UDP headers) and storage systems.")