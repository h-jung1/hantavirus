
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import pandas as pd
from Bio import SeqIO
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="graph lengths of assigned sequences"
    )

    parser.add_argument("--input", help="Input file containing sequences")
    parser.add_argument("--output_dir", help="Output directory")

    return parser.parse_args()


def main():
    args = parse_args()

    Path(args.output_dir).parent.mkdir(parents=True, exist_ok=True)

    records = SeqIO.parse(args.input, "fasta")
    length_list = []

    for record in records:
        length = len(record.seq)
        length_list.append(length)

    df = pd.DataFrame(data=length_list)

    sns.displot(df, kind="hist")
    plt.savefig(args.output_dir, bbox_inches="tight")


if __name__ == "__main__":
    main()
