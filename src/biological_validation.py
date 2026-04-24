import pandas as pd

# Load synthetic exposures
synthetic = pd.read_csv("../results/signature_exposures.tsv", sep="\t", index_col=0)

# BIOLOGICAL VALIDATION

# Split by cancer type
breast = synthetic[synthetic.index.str.contains("Breast")]
prostate = synthetic[synthetic.index.str.contains("Prost")]

# Mean signature contributions
breast_mean = breast.mean().sort_values(ascending=False)
prostate_mean = prostate.mean().sort_values(ascending=False)

print("\nTop Breast Signatures:")
print(breast_mean.head(5))

print("\nTop Prostate Signatures:")
print(prostate_mean.head(5))
