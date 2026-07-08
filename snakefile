configfile: "config/config.yaml"

import pandas as pd
meta = pd.read_csv("config/refseqs.csv")
ref_acc = meta["Accession"].to_list()

rule all:
    input:
        expand("data/refseqs/proteins/{acc}.fasta", acc=ref_acc),

include: "rules/download.smk"
include: "rules/species_tree.smk"