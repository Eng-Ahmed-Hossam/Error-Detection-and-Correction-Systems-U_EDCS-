import streamlit as st

# --- Global config ---
st.set_page_config(
    page_title="U_EDCS Suite",
    page_icon="🔹",
    layout="wide"
)

# --- Sidebar navigation ---
st.sidebar.title("🔹 Error Detection & Correction Suite")
st.sidebar.markdown("Navigate through the methods using the Pages menu:")

st.sidebar.success("""
Available modules:
- Parity
- Hamming
- CRC
- Checksum
- Experiments
""")

# --- Landing page content ---
st.title("🔹 Unified Error Detection & Correction System (U_EDCS)")
st.markdown("""
Welcome to the **U_EDCS app**.  
This suite lets you explore and compare different error detection and correction techniques interactively:

- **Parity**: Single-bit and two-dimensional parity checks  
- **Hamming**: General Hamming codes with error correction  
- **CRC**: Cyclic Redundancy Check with polynomial division visualization  
- **Checksum**: Internet and normal checksum methods  
- **Experiments**: Monte Carlo simulations and benchmarking across methods  

Use the sidebar to navigate between modules.
""")

# --- Custom CSS theme ---
st.markdown("""
<style>
    /* Buttons */
    .stButton>button {
        background-color: #0066cc;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #004c99;
    }

    /* Text inputs */
    .stTextInput>div>input, .stTextArea>div>textarea {
        border-radius: 6px;
        border: 1px solid #0066cc;
    }

    /* Headings */
    h1, h2, h3 {
        color: #004c99;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f0f8ff;
    }
</style>
""", unsafe_allow_html=True)