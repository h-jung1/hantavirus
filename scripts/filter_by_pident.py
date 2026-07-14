
import argparse
import pandas as pd
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(
        description="extract protein sequences out of genbank files"
    )
    parser.add_argument("--metadata", help="Path to input file")
    parser.add_argument("--species", help="Species")
    parser.add_argument("--segment", help="Segment")
    parser.add_argument("--pident",type=float , help="cutoff pident value")
    parser.add_argument("--output_dir", help="Path to output directory")

    return parser.parse_args()

def main():
    args=parse_args()
    
    metadata=pd.read_csv(args.metadata, sep='\t')

    new_df = metadata[(metadata["assigned_species"] == args.species)
            & (metadata["pident"] > args.pident)
            & (metadata["assigned_segment"] == args.segment.upper())]
    new_df.to_csv(args.output_dir, sep='\t', index=False)

    
if __name__ == "__main__":
    main()

# later concatenate all accession number fasta files of that list into one large file
# also make one metadata file (per segment and species)



