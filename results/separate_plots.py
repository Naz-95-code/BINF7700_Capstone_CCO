import matplotlib.pyplot as plt

def load(file):
    values = []
    with open(file) as f:
        for line in f:
            line = line.strip()
            if line:
                values.append(int(line))
    return values

breast = load("breast_counts.txt")
prostate = load("prostate_counts.txt")

# Breast plot
plt.figure(figsize=(6,4))
plt.hist(breast, bins=20)
plt.title("Synthetic Breast Mutation Burden")
plt.xlabel("Mutation Count")
plt.ylabel("Number of Samples")
plt.tight_layout()
plt.savefig("synthetic_breast.png", dpi=300)
plt.clf()

# Prostate plot
plt.figure(figsize=(6,4))
plt.hist(prostate, bins=20)
plt.title("Synthetic Prostate Mutation Burden")
plt.xlabel("Mutation Count")
plt.ylabel("Number of Samples")
plt.tight_layout()
plt.savefig("synthetic_prostate.png", dpi=300)
