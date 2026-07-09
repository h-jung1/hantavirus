
from Bio import SeqIO
from Bio.SeqRecord import Seq, SeqRecord
import argparse
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="extract protein sequences out of genbank files"
    )
    parser.add_argument("--input", help="Path to input file")
    parser.add_argument("--output", help="Path to output file")

    return parser.parse_args()


def main():
    args = parse_args()

    record = SeqIO.read(args.input, "genbank")

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    largest_record = None
    for feature in record.features:
        if feature.type == "CDS":
            translation = feature.qualifiers.get("translation")
            if translation:
                protein_id = feature.qualifiers.get("protein_id", ["unknown"])[0]
                product = feature.qualifiers.get("product", ["unknown"])[0]
                accession = record.annotations.get("accessions", ["unknown"])[0]
                source = record.annotations.get("source", "unknown")
                source = source.replace(" ", "_")
                protein_record = SeqRecord(
                        seq=Seq(translation[0]),
                        id='|' + accession + '|' + source,
                        description=product,
                    )

                if largest_record is None or len(protein_record.seq) > len(largest_record.seq):
                    largest_record = protein_record

    if largest_record is None:
        open(args.output, "w").close()

        with open("data/refseqs/proteins/missing.txt", "a") as file:
            file.write(f"{args.input} \n")
    else:
        SeqIO.write(largest_record, args.output, "fasta")


if __name__ == "__main__":
    main()