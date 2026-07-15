
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
    parser.add_argument("--output", help="Path to output fasta files")

    return parser.parse_args()


def main():
    args = parse_args()

    records = SeqIO.parse(args.input, "genbank")

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
                            id= accession + '|' + source,
                            description=product,
                        )

                    if largest_record is None or len(protein_record.seq) > len(largest_record.seq):
                        largest_record = protein_record

        if largest_record is None:
            outfile = Path(args.output) / f"{record.id}.fasta"
            open(outfile, "w").close()

        else:
            outfile = Path(args.output) / f"{record.id}.fasta"
            outfile.parent.mkdir(parents=True, exist_ok=True)
            SeqIO.write(largest_record, outfile, "fasta")


if __name__ == "__main__":
    main()