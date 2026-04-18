import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import mannwhitneyu

st.set_page_config(page_title="OncoGAN Dashboard", layout="wide")

st.title("OncoGAN Mutation Analysis Dashboard")
st.write("Exploration of synthetic vs real cancer mutation patterns")

# Sidebar selection
cancer_type = st.sidebar.selectbox(
    "Cancer Type",
    ["Breast", "Prostate"]
)

# File paths
synthetic_map = {
    "Breast": "results/synthetic_breast_counts.txt",
    "Prostate": "results/synthetic_prostate_counts.txt"
}

real_map = {
    "Breast": "results/real_breast_counts.txt",
    "Prostate": "results/real_prostate_counts.txt"
}

# Load data
synthetic = np.loadtxt(synthetic_map[cancer_type])
real = np.loadtxt(real_map[cancer_type])

# Create tabs
tab1, tab2, tab3 = st.tabs([
    "Mutation Burden",
    "Statistical Comparison",
    "Signature Heatmap"
])

# Mutation burden tab
with tab1:
    st.subheader(f"{cancer_type} Mutation Burden Distribution")

    fig, ax = plt.subplots()

    ax.hist(synthetic, bins=30, alpha=0.6, label="Synthetic")
    ax.hist(real, bins=30, alpha=0.6, label="TCGA")

    ax.set_xlabel("Mutation Count")
    ax.set_ylabel("Number of Samples")
    ax.set_title(f"{cancer_type}: Synthetic vs Real")
    ax.legend()

    st.pyplot(fig)

    st.subheader("Summary Statistics")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Synthetic Data**")
        st.write(f"Mean: {np.mean(synthetic):.2f}")
        st.write(f"Median: {np.median(synthetic):.2f}")
        st.write(f"Variance: {np.var(synthetic):.2f}")

    with col2:
        st.markdown("**TCGA Data**")
        st.write(f"Mean: {np.mean(real):.2f}")
        st.write(f"Median: {np.median(real):.2f}")
        st.write(f"Variance: {np.var(real):.2f}")

# Statistical test tab
with tab2:
    st.subheader("Mann–Whitney U Test")

    stat, p_value = mannwhitneyu(synthetic, real, alternative='two-sided')

    st.write(f"U Statistic: {stat}")
    st.write(f"P-value: {p_value:.2e}")

    if p_value < 0.05:
        st.error("Distributions are significantly different")
    else:
        st.success("No significant difference")

    st.subheader("Interpretation")

    st.write(
        "The Mann–Whitney U test evaluates whether the mutation burden distributions differ "
        "between synthetic and real datasets. A significant result indicates that the synthetic "
        "data does not fully capture the variability observed in real cancer samples."
    )

# Heatmap tab
with tab3:
    st.subheader("COSMIC Signature Heatmap")

    try:
        data = pd.read_csv("results/signature_exposures.tsv", sep="\t", index_col=0)

        data = data.loc[:, (data != 0).any(axis=0)]
        data_log = np.log1p(data)
        data_norm = data_log.div(data_log.sum(axis=1), axis=0)

        fig, ax = plt.subplots(figsize=(12, 6))

        sns.heatmap(
            data_norm,
            cmap="viridis",
            cbar_kws={'label': 'Normalized Contribution'},
            yticklabels=False
        )

        ax.set_title("Signature Contributions")

        st.pyplot(fig)

    except:
        st.warning("Signature data not found. Ensure signature_exposures.tsv exists.")

# Footer
st.markdown("---")
st.caption("Built for mutation pattern analysis using OncoGAN synthetic data")
