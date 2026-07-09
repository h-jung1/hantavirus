from Bio import SeqIO
import argparse
from pathlib import Path
import pandas as pd
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser(
        description="Sort proteins by length"
    )
    parser.add_argument("--input", help="Path to input file")
    parser.add_argument("--output_s", help = "Path to output for S segment")
    parser.add_argument("--output_m", help = "Path to output for M segment")
    parser.add_argument("--output_l", help = "Path to output for L segment")

    return parser.parse_args()

def main():
    args = parse_args()

    Path(args.output_s).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_m).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_l).parent.mkdir(parents=True, exist_ok=True)

    s_records = []
    m_records = []
    l_records = []

    for record in SeqIO.parse(args.input, "fasta"):
        if np.abs(len(record.seq)-450) < 100:
            s_records.append(record)
        elif np.abs(len(record.seq)-1200) < 100:
            m_records.append(record)
        elif np.abs(len(record.seq) - 2000) < 300:
            l_records.append(record)
                

    SeqIO.write(s_records, args.output_s, "fasta")
    SeqIO.write(m_records, args.output_m, "fasta")
    SeqIO.write(l_records, args.output_l, "fasta")


if __name__ == "__main__":
    main()   
    



