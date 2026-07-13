configfile: "config/config.yaml"

import pandas as pd
meta = pd.read_csv("config/refseqs.csv")
ref_acc = meta["Accession"].to_list()
segment = ["m", "l", "s"]
species= ["Hantavirus Z10", "Orthohantavirus hantanense", "Orthohantavirus puumalaense",
            "Orthohantavirus seoulense", "Orthohantavirus tulaense"]

include: "rules/download.smk"
include: "rules/species_tree.smk"
include: "rules/diamond_sort.smk"

rule all:
    input:
        expand("data/refseqs/proteins/{acc}.fasta", acc=ref_acc),
        expand("results/species_tree/aligned_{segment}.fasta", segment=segment),
        expand("results/species_tree/aligned_{segment}.fasta.treefile", segment=segment),
        expand("results/species_tree/rooted_ladder_{segment}.pdf", segment=segment),
        "data/diamond_db/refseq_segments.fasta",
        "data/diamond_db/diamond.dmnd",
        "results/diamond_alignments.tsv",
        "data/ncbi_dataset_seq_assigned.tsv",
        rules.add_missing_translations.output,
        rules.graph_seq_assignment.output

    

# include: "rules/prepare_seq.smk"