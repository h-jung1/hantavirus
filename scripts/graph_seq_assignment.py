
import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt
import argparse
from pathlib import Path


def parse_args():
    parser=argparse.ArgumentParser(
        description="graph results of sequence assignment")

    parser.add_argument("--assigned_set", help="Path to CSV file with assigned species and segment")
    parser.add_argument("--diamond_tsv", help="Path to diamond alignment")
    parser.add_argument("--output_dir", help="Output directory")

    return parser.parse_args()


def main():
    args = parse_args()

    Path(args.output_dir).mkdir(parents=True, exist_ok=True)

    # Create matrix of species and assigned species
    metadata=pd.read_csv(args.assigned_set, sep='\t')
    confusion_species = pd.crosstab(metadata["virus-name"], metadata["assigned_species"])

    annot_labels = confusion_species.astype(str)
    annot_labels[confusion_species < 20] = ""

    plt.figure(figsize=(15,15))
    sns.heatmap(confusion_species, annot=annot_labels, cmap="crest", fmt="", linewidth=0.7)
    plt.savefig(f"{args.output_dir}/species_matrix.png", bbox_inches="tight")

    # Create matrix of segments vs assigned segments
    confusion_segment = pd.crosstab(metadata["segment"], metadata["assigned_segment"])
    plt.figure(figsize=(10,12))
    sns.heatmap(confusion_segment, annot=True, cmap="crest", fmt="d")
    plt.savefig(f"{args.output_dir}/segment_matrix.png")

    # Create histogramm of pident    
    Path(f"{args.output_dir}/pident").mkdir(parents=True, exist_ok=True)
    diamond_tsv=pd.read_csv(args.diamond_tsv, sep='\t', header = None)
    diamond_tsv.columns=["accession", "sseqid", "pident", "length", "mismatch",
                        "gapopen", "qstart", "qend", "sstart", "send",
                        "evalue", "bitscore"]
    plt.figure(figsize=(10,12))
    sns.displot(diamond_tsv, x="pident")
    plt.savefig(f"{args.output_dir}/pident/pident_distribution.png")

    # The following code plots the pident per species and segment
    split_sseqid = diamond_tsv["sseqid"].str.split('|', expand=True)
    diamond_tsv["assigned_species_id"]=split_sseqid[0]
    diamond_tsv["assigned_species"]=split_sseqid[1]
    diamond_tsv["assigned_segment"]=split_sseqid[2]
    diamond_m = diamond_tsv[diamond_tsv["assigned_segment"] == "M"]
    diamond_s = diamond_tsv[diamond_tsv["assigned_segment"] == "S"]
    diamond_l = diamond_tsv[diamond_tsv["assigned_segment"] == "L"]

    # This code plots all the M segments
    plot = sns.catplot(diamond_m, x="assigned_species", y="pident", kind="box", height=8, aspect=2)
    plot.set_xticklabels(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(f"{args.output_dir}/pident/pident_segment_m.png")

    # This code plots all the S segments
    plot = sns.catplot(diamond_s, x="assigned_species", y="pident", kind="box", height=8, aspect=2)
    plot.set_xticklabels(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(f"{args.output_dir}/pident/pident_segment_s.png")
    
    # This code plots all the L segments
    plot = sns.catplot(diamond_l, x="assigned_species", y="pident",kind="box", height=8, aspect=2)
    plot.set_xticklabels(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(f"{args.output_dir}/pident/pident_segment_l.png")

    plt.close("all")

    # This code plots the counts of the top 5 most represented species per segment
    diamond_top5_species = diamond_tsv["assigned_species"].value_counts().head(5).index
    df = diamond_tsv[diamond_tsv["assigned_species"].isin(diamond_top5_species)]

    plot = sns.displot(df,
        x="assigned_segment",
        hue="assigned_species",
        height=8,
        aspect=2,
        multiple="stack")
    sns.move_legend(plot, "upper right", bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.savefig(f"{args.output_dir}/overall_distribution.png", bbox_inches="tight")

    # This code plots the pident distribution per segment and species
    for species in diamond_top5_species:
        df = diamond_tsv[diamond_tsv["assigned_species"]==species]
        for segment in diamond_tsv["assigned_segment"].unique():
            sub_df = df[df["assigned_segment"] == segment]
            plt.figure(figsize=(10,12))
            plot = sns.displot(sub_df, x="pident")
            

            Path(f"{args.output_dir}/top5_species/{species}").mkdir(parents=True, exist_ok=True)

            plot.savefig(f"{args.output_dir}/top5_species/{species}/{segment}_segment.png")
            plt.close(plot.figure)
        

if __name__ == "__main__":
    main()