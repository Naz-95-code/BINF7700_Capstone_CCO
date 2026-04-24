import pandas as pd
import plotly.express as px
from sklearn.metrics.pairwise import cosine_similarity

# Paths
INPUT_FILE = "results/signature_exposures.tsv"
OUTPUT_FILE = "results/figures/cosine_similarity.png"

# Load data
sig = pd.read_csv(INPUT_FILE, sep="\t", index_col=0)

# Normalize per sample
sig_norm = sig.div(sig.sum(axis=1), axis=0)

# Split samples
breast_samples = [i for i in sig_norm.index if "breast" in str(i).lower()]
prostate_samples = [i for i in sig_norm.index if "prost" in str(i).lower()]

# Mean signatures
breast_mean = sig_norm.loc[breast_samples].mean(axis=0).values.reshape(1, -1)
prostate_mean = sig_norm.loc[prostate_samples].mean(axis=0).values.reshape(1, -1)

# Compute cosine similarity
results = []

for sample in breast_samples:
    val = cosine_similarity(
        sig_norm.loc[sample].values.reshape(1, -1),
        breast_mean
    )[0][0]
    results.append([sample, "Breast", val])

for sample in prostate_samples:
    val = cosine_similarity(
        sig_norm.loc[sample].values.reshape(1, -1),
        prostate_mean
    )[0][0]
    results.append([sample, "Prostate", val])

cosine_df = pd.DataFrame(
    results,
    columns=["Sample", "Cancer Type", "Cosine Similarity"]
)

# Mean values (for reporting)
b_mean = cosine_df[cosine_df["Cancer Type"] == "Breast"]["Cosine Similarity"].mean()
p_mean = cosine_df[cosine_df["Cancer Type"] == "Prostate"]["Cosine Similarity"].mean()

print(f"Mean Breast Similarity: {b_mean:.3f}")
print(f"Mean Prostate Similarity: {p_mean:.3f}")

# Plot
fig = px.box(
    cosine_df,
    x="Cancer Type",
    y="Cosine Similarity",
    color="Cancer Type",
    points="all",
    color_discrete_map={
        "Breast": "#E91E8C",
        "Prostate": "#1565C0"
    }
)

# Add threshold line
fig.add_hline(
    y=0.8,
    line_dash="dash",
    line_color="red"
)

# Clean layout
fig.update_layout(
    title="Cosine Similarity to Mean Cancer-Type Signature",
    font=dict(size=18),
    width=900,
    height=500,
    showlegend=False
)

fig.update_yaxes(title="Cosine Similarity Score")
fig.update_xaxes(title="Cancer Type")

# Save
fig.write_image(OUTPUT_FILE, scale=3)

print(f"Saved: {OUTPUT_FILE}")
