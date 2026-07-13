#%%
from Bio import SeqIO
from Bio.SeqRecord import Seq,SeqRecord
from Bio.SeqFeature import FeatureLocation, SeqFeature
import argparse
from pathlib import Path
#%%
def parse_args():
    parser = argparse.ArgumentParser(
        description="add genbank protein records"
    )
    parser.add_argument("--acc", help="Path to file with missing accession ids")
    parser.add_argument("--gbk_output", help="Path to gbk file output")
    parser.add_argument("--protein_dir", help="Path to protein files")

    return parser.parse_args()

def main():
    args = parse_args()

    Path(args.output).mkdir(parents=True, exist_ok=True)

    with open(args.acc, "r") as file:
        for line in file:
            path=line.strip()
            record=SeqIO.read(path, "genbank")
            sequence=record.seq
            accession = record.id
            source = record.annotations.get("source", "unknown")
            source = source.replace(" ", "_")
            
            longest_translation = None
            for frame in range(3):
                length = 3 * ((len(sequence) - frame) // 3)  # Multiple of three
                
                aa_start = 0
                translation = str(sequence[frame : frame + length].translate())

                while aa_start < len(translation):
                    aa_end = translation.find("*", aa_start)
                    if aa_end == -1:
                        aa_end = len(translation)
                    
                    current_protein = translation[aa_start:aa_end]
                    m_index = current_protein.find("M")
                    if m_index != -1:
                        current_protein = current_protein[m_index:]

                    if longest_translation == None or len(current_protein) > len(longest_translation):
                        longest_translation = current_protein
                        nt_start = frame + aa_start*3
                        nt_end = frame + aa_end*3

                    aa_start = aa_end +1
                        
            feature = SeqFeature(
                FeatureLocation(nt_start, nt_end), 
                type="CDS", 
                qualifiers={"translation": [str(longest_translation)]}
                )

            record.features.append(feature)
            SeqIO.write(record, f"{args.gbk_output}/{record.id}_new.gbk", "genbank")

            protein_record = SeqRecord(seq=Seq(longest_translation),id= accession + '|' + source,
                            description="own translation")
            output_path = f"{args.protein_dir}/{accession}.fasta"
            SeqIO.write(protein_record, output_path, "fasta")


if __name__ == "__main__":
    main()

