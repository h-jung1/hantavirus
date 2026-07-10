configfile: "config/config.yaml"

import pandas as pd
meta = pd.read_csv("config/refseqs.csv")
ref_acc = meta["Accession"].to_list()
segment = ["m", "l", "s"]

rule all:
    input:
        expand("data/refseqs/proteins/{acc}.fasta", acc=ref_acc),
        expand("results/species_tree/aligned_{segment}.fasta", segment = segment),
        expand("results/species_tree/aligned_{segment}.fasta.treefile", segment = segment),
        expand("results/species_tree/rooted_ladder_{segment}.pdf", segment = segment)

include: "rules/download.smk"
include: "rules/species_tree.smk"