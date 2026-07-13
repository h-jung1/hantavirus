import os 
from pathlib import Path
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="find empty protein files"
    )
    parser.add_argument("--input", help="Path to input file", nargs="+")
    parser.add_argument("--gbk_dir", help="Path to corresponding gbk files")
    parser.add_argument("--output", help="Path to output file")

    return parser.parse_args()

def main():
    args=parse_args()
    
    missing=[]
    for file in args.input:
        if os.path.getsize(file) == 0:
            missing.append(file)
    
    with open(args.output, "w") as output_file:
        for file in missing:
            accession = Path(file).stem
            gbk_path = Path(args.gbk_dir/f"{accession}.gbk")
            output_file.write(f"{gbk_path}\n")

    if __name__ == "__main__":
        main()