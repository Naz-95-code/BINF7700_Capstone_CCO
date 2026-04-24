import pandas as pd
import plotly.express as px

# Paths
INPUT_FILE = "results/combined_spectra.tsv"
OUTPUT_FILE = "results/figures/mutation_spectrum.png"

# Load data
spectra = pd.read_csv(INPUT_FILE, sep="\t")

sub_col = "Mutation"
freq_col = "Frequency"
sample_col = "Sample"

sub_types = ["C>A", "C>G", "C>T", "T>A", "T>C", "T>G"]

colors = {
    "C>A": "#1f77b4",
    "C>G": "#ff7f0e",
    "C>T": "#d62728",
    "T>A": "#2ca02c",
    "T>C": "#9467bd",
    "T>G": "#8c564b"
}

# Assign cancer type
spectra["Cancer Type"] = spectra[sample_col].apply(
    lambda x: "Breast" if "breast" in str(x).lower() else "Prostate"
)

# Filter valid substitutions
spectra = spectra[spectra[sub_col].isin(sub_types)]

# Aggregate
grouped = (
    spectra.groupby(["Cancer Type", sub_col])[freq_col]
    .mean()
    .reset_index()
)

grouped.columns = ["Cancer Type", "Substitution", "Mean Frequency"]

# Plot
fig = px.bar(
    grouped,
    x="Substitution",
    y="Mean Frequency",
    color="Substitution",
    facet_col="Cancer Type",
    color_discrete_map=colors,
    text="Mean Frequency"
)

fig.update_traces(
    texttemplate="%{text:.3f}",   # format to 3 decimal places
    textposition="outside"        # place above bars
)

fig.update_layout(
    yaxis=dict(range=[0, grouped["Mean Frequency"].max() * 1.2])
)

fig.update_layout(
    font=dict(size=18),
    width=1200,
    height=500,
    showlegend=False,
    margin=dict(l=80, r=40, t=60, b=60)
)

fig.update_yaxes(title_text="Mean Relative Frequency", col=1)
fig.update_yaxes(title_text="", col=2)

fig.update_xaxes(title_text="Substitution Type")
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
# Save
fig.write_image(OUTPUT_FILE, scale=3)

print(f"Saved: {OUTPUT_FILE}")
