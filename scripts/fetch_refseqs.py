
import argparse
from Bio import SeqIO
import pandas as pd
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="fetch refseqs for chosen species"
    )

    parser.add_argument("--species", help="species")
    parser.add_argument("--segment", help="segment")
    parser.add_argument("--output", help="Output directory")

    return parser.parse_args()


def main():
    args = parse_args()

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    clean_species = args.species.replace('_', ' ')
    df = pd.read_csv("config/refseqs.csv")
    print(df)
    filtered_df = df[
        (df["Virus Name"] == clean_species) &
        (df["Segment"] == args.segment.upper())
        ]

    records = []
    for accession in filtered_df["Accession"]:
        record = SeqIO.read(
            f"data/fasta_sequences/{accession}.fasta",
            "fasta"
        )
        records.append(record)

    SeqIO.write(records[0], args.output, "fasta")


if __name__ == "__main__":
    main()
