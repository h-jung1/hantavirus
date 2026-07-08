

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
    protein_records = []

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    for feature in record.features:
            if feature.type == "CDS":
                translation = feature.qualifiers.get("translation")
                if translation:
                    protein_id = feature.qualifiers.get("protein_id", ["unknown"])[0]
                    product = feature.qualifiers.get("product", ["unknown"])[0]
                    protein_records.append(
                        SeqRecord(
                            seq=Seq(translation[0]),
                            id= protein_id,
                            description=product,
                        )
                    )
    SeqIO.write(protein_records, args.output, "fasta")

if __name__=="__main__":
    main()