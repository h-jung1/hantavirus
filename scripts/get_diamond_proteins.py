#%%
import argparse
from Bio import SeqIO
from pathlib import Path
#%%
def parse_args():
    parser = argparse.ArgumentParser(
        description="get protein sequences for diamond"
    )

    parser.add_argument("--input_s", help="Path to input file with S segments")
    parser.add_argument("--input_m", help="Path to input file with M segments")
    parser.add_argument("--input_l", help="Path to input file with L segments")
    parser.add_argument("--output", help="Path to output file")

    return parser.parse_args()
#%%
def main():
    args = parse_args()

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    clean_records=[]
    for segment_name, argument in [("S", args.input_s), ("M", args.input_m), ("L", args.input_l)]:
        for record in SeqIO.parse(argument, "fasta"):
            record.id = record.id + "|" + segment_name
            record.description = ""
            clean_records.append(record)

    SeqIO.write(clean_records, args.output, "fasta")
#%%
if __name__ == "__main__":
    main()

       