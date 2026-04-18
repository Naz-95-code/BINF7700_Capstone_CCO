import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import spearmanr, ttest_ind

# Load data
data = pd.read_csv("../results/signature_exposures.tsv", sep="\t", index_col=0)

# Split groups
breast = data[data.index.str.contains("Breast")]
prostate = data[data.index.str.contains("Prost")]

# Mean profiles
breast_mean = breast.mean(axis=0).values.reshape(1, -1)
prostate_mean = prostate.mean(axis=0).values.reshape(1, -1)

# ---------------------------
# 1. Cosine Similarity
# ---------------------------
similarity = cosine_similarity(breast_mean, prostate_mean)
print("Cosine Similarity (Breast vs Prostate):", similarity[0][0])

# ---------------------------
# 2. Spearman Correlation
# ---------------------------
corr, pval = spearmanr(breast_mean.flatten(), prostate_mean.flatten())
print("Spearman Correlation:", corr)
print("Spearman p-value:", pval)

# ---------------------------
# 3. Mutation Burden T-test
# ---------------------------
t_stat, p_val = ttest_ind(
    breast.sum(axis=1),
    prostate.sum(axis=1)
)

print("T-test p-value (mutation burden):", p_val)
