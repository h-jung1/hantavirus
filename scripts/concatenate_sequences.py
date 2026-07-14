
import argparse
import pandas as pd
from Bio import SeqIO

def parse_args():
    parser = argparse.ArgumentParser(
        description="concatenate fasta sequences"
    )
    
    parser.add_argument("--input", help="Path to CSV file containing Accessions")
    parser.add_argument("--output", help="Path to output file")

    return parser.parse_args()

def main():
    args = parse_args()

    metadata = pd.read_csv(args.input, sep='\t')
    records = []
    for accession_version in metadata["accession_version"]:
        record = SeqIO.read(f"data/fasta_sequences/{accession_version}.fasta", "fasta")
        records.append(record)
    SeqIO.write(records, args.output, "fasta")

if __name__ == "__main__":
    main()
        