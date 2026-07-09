
from Bio import SeqIO
import argparse
from pathlib import Path
import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(
        description="Find length of proteins"
    )
    parser.add_argument("--input", help="Path to input file", nargs="+")
    parser.add_argument("--output", help = "Path to output file")

    return parser.parse_args()



def main():
    args = parse_args()

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    records = []

    for file in args.input:
        for record in SeqIO.parse(file, "fasta"):
            records.append({"seq_id": record.id, "seq_len": len(record.seq)})
    
    df = pd.DataFrame(records)
    df.to_csv(args.output, index = False)



if __name__ == "__main__":
    main()