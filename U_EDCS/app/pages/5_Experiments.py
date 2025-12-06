import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from core.experiments import ExperimentRunner

st.set_page_config(page_title="Experiments", page_icon="🔹", layout="wide")

st.title("🔹 Experiments & Benchmarking")
st.markdown("### Run Monte Carlo simulations and compare error detection methods under noisy channels.")

# --- Parameters ---
block_size = st.slider("Data block size (bits):", min_value=4, max_value=64, value=8)
n_trials = st.number_input("Number of trials:", min_value=100, max_value=10000, value=1000)
p = st.slider("Random bit flip probability (p):", min_value=0.0, max_value=0.2, value=0.01, step=0.01)
burst_prob = st.slider("Burst error probability:", min_value=0.0, max_value=0.5, value=0.1, step=0.05)
max_burst_len = st.slider("Max burst length:", min_value=1, max_value=10, value=3)

runner = ExperimentRunner(
    block_size=block_size,
    n_trials=n_trials,
    channel_params={"p": p, "burst_prob": burst_prob, "max_burst_len": max_burst_len}
)

# --- Monte Carlo ---
st.subheader("Monte Carlo Simulation")
scheme = st.selectbox("Choose scheme:", ["parity", "parity2d", "hamming", "crc", "checksum"])

if st.button("Run Monte Carlo"):
    st.info(f"Running {n_trials} trials for {scheme}...")
    result = runner.monte_carlo(scheme)
    st.json(result)

    # Simple bar chart
    fig, ax = plt.subplots()
    ax.bar(["Detection Rate", "Correction Rate"],
           [result["detection_rate"], result["correction_rate"]],
           color=["skyblue", "lightgreen"])
    ax.set_ylim(0, 1)
    ax.set_ylabel("Rate")
    ax.set_title(f"Monte Carlo Results for {scheme}")
    st.pyplot(fig)

# --- Benchmarking ---
st.subheader("Benchmark Multiple Schemes")
schemes = st.multiselect("Select schemes:", ["parity", "parity2d", "hamming", "crc", "checksum"],
                         default=["parity", "hamming", "crc"])

if st.button("Run Benchmark"):
    st.info(f"Running benchmark ({n_trials} trials each)...")
    results = runner.benchmark(schemes)
    df = pd.DataFrame(results)

    st.write("### Benchmark Results")
    st.dataframe(df)

    # Plot detection rates
    fig, ax = plt.subplots()
    ax.bar(df["scheme"], df["detection_rate"], color="coral")
    ax.set_ylim(0, 1)
    ax.set_ylabel("Detection Rate")
    ax.set_title("Benchmark Detection Rates")
    st.pyplot(fig)

    # Plot correction rates
    fig, ax = plt.subplots()
    ax.bar(df["scheme"], df["correction_rate"], color="seagreen")
    ax.set_ylim(0, 1)
    ax.set_ylabel("Correction Rate")
    ax.set_title("Benchmark Correction Rates")
    st.pyplot(fig)