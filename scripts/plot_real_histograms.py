import matplotlib.pyplot as plt

def load(file):
    values = []
    with open(file) as f:
        for line in f:
            line = line.strip()
            if line:
                values.append(int(line))
    return values

# Load ONLY real data
real_breast = load("../data/full/real_breast_counts.txt")
real_prostate = load("../data/full/real_prostate_counts.txt")

# OPTIONAL: filter extreme outliers for better visualization
real_breast_filtered = [x for x in real_breast if x <= 150]
real_prostate_filtered = [x for x in real_prostate if x <= 150]

# Breast histogram
plt.hist(real_breast_filtered, bins=30)
plt.xlim(0, 150)
plt.title("Real Breast Mutation Burden")
plt.xlabel("Mutation Count")
plt.ylabel("Number of Samples")
plt.tight_layout()
plt.savefig("real_breast_histogram.png")
plt.clf()

# Prostate histogram
plt.hist(real_prostate_filtered, bins=30)
plt.xlim(0, 150)
plt.title("Real Prostate Mutation Burden")
plt.xlabel("Mutation Count")
plt.ylabel("Number of Samples")
plt.tight_layout()
plt.savefig("real_prostate_histogram.png")
