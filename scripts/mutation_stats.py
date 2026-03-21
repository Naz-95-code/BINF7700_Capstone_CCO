import scipy.stats as stats

# load mutation counts
breast = [int(x.strip()) for x in open("../results/breast_counts.txt")]
prostate = [int(x.strip()) for x in open("../results/prostate_counts.txt")]

# Mann-Whitney U test
stat, p = stats.mannwhitneyu(breast, prostate)

print("Breast samples:", len(breast))
print("Prostate samples:", len(prostate))
print("Statistic:", stat)
print("P-value:", p)

if p < 0.05:
    print("Result: Significant difference in mutation burden")
else:
    print("Result: No significant difference")
