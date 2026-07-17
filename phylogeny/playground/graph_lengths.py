
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
    parser.add_argument(
        "--min_length", type=float, help="Minimum length cutoff value"
        )
    parser.add_argument(
        "--max_length", type=float, help="Maximum length cutoff value"
        )

    return parser.parse_args()


def main():
    args = parse_args()

    Path(args.output_dir).parent.mkdir(parents=True, exist_ok=True)

    records = SeqIO.parse(args.input, "fasta")
    length_dict = {}

    for record in records:
        length = len(record.seq)
        seq_id = record.id
        length_dict[seq_id] = length

    ncbi_report = pd.read_csv("../data/ncbi_dataset_report.tsv", sep='\t')
    accession_data = {}
    for index, row in ncbi_report.iterrows():
        accession = row["accession"]
        if accession in length_dict.keys():
            clean_country = str(row["geo-location"]).split(":")[0]
            accession_data[accession] = {
                "length": length_dict[accession],
                "country": clean_country
            }

    df = pd.DataFrame.from_dict(accession_data, orient="index")
    df.index.name = "accession"
    df = df.reset_index()

    fig, axes = plt.subplots(2, 1, figsize=(12, 10))
    sns.histplot(
        df, x="length", hue="country", multiple="stack", bins=100, ax=axes[0]
    )
    sns.ecdfplot(
        df, x="length", log_scale=True, stat="count", ax=axes[1]
        )

    axes[0].axvline(x=args.min_length, color="blue", linewidth=0.5)
    axes[0].axvline(x=args.max_length, color="blue", linewidth=0.5)
    axes[1].axvline(x=args.min_length, color="blue", linewidth=0.5)
    axes[1].axvline(x=args.max_length, color="blue", linewidth=0.5)

    plt.savefig(args.output_dir, bbox_inches="tight")


if __name__ == "__main__":
    main()
