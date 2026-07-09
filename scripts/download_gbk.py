
from Bio import Entrez, SeqIO
import argparse

Entrez.email = "hello@nextstrain.org"


def parse_args():
    parser = argparse.ArgumentParser(
        description="download genbank records for list of accession ids"
    )
    parser.add_argument("--acc", help="accession ids")
    parser.add_argument("--out", help="Path to output file")

    return parser.parse_args()


def main():
    args = parse_args()
    
    handle = Entrez.efetch(db="nucleotide", id=args.acc, rettype="gb", retmode="text")
    record = SeqIO.read(handle, "genbank")
    handle.close()

    SeqIO.write(record, args.out, "genbank")


if __name__ == "__main__":
    main()