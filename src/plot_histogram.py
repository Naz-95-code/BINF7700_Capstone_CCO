import sys
import os
import matplotlib.pyplot as plt


def load_counts(file_path):
    values = []
    with open(file_path) as f:
        for line in f:
            line = line.strip()
            if line.isdigit():
                values.append(int(line))
    return values


def plot_histogram(input_path, output_path, title):
    data = load_counts(input_path)

    # Limit TCGA range for better visualization
    if "TCGA" in title:
        data = [x for x in data if x <= 150]

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    plt.figure(figsize=(6, 4))
    plt.hist(data, bins=30, edgecolor="black")
    plt.xlabel("Mutation Count (raw)")
    plt.ylabel("Number of Samples")
    plt.title(title)
    plt.tight_layout()

    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Saved: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python plot_histogram.py <input_txt> <output_png> <title>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    plot_title = sys.argv[3]

    plot_histogram(input_file, output_file, plot_title)
