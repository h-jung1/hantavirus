
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import argparse
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="extract protein sequences out of genbank files"
    )
    parser.add_argument("--input", help="Path to input file")
    parser.add_argument("--missing", help="Path to file with accessions of missing proteins")
    parser.add_argument("--output", help="Path to output fasta file")

    return parser.parse_args()


def main():
    args = parse_args()

    Path(args.missing).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    records = SeqIO.parse(args.input, "genbank")
    records_to_write = []
    missing_records = []

    for record in records:
        largest_record = None
        for feature in record.features:
            if feature.type == "CDS":
                translation = feature.qualifiers.get("translation")
                if translation:
                    product = feature.qualifiers.get("product", ["unknown"])[0]
                    accession = record.annotations.get(
                        "accessions", ["unknown"]
                        )[0]
                    source = record.annotations.get("source", "unknown")
                    source = source.replace(" ", "_")
                    protein_record = SeqRecord(
                            seq=Seq(translation[0]),
                            id=accession + '|' + source,
                            description=product,
                        )

                    if largest_record is None or len(protein_record.seq) > len(largest_record.seq):
                        largest_record = protein_record

        if largest_record is None:
            missing_records.append(f"{record.id}\n")
        else:
            records_to_write.append(protein_record)

    with open(args.missing, "w") as handle:
        for missing_record in missing_records:
            handle.write(missing_record)

    SeqIO.write(records_to_write, args.output, "fasta")


if __name__ == "__main__":
    main()
