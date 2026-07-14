configfile: "config/config.yaml"

import pandas as pd
meta = pd.read_csv("config/refseqs.csv")
ref_acc = meta["Accession"].to_list()
segment = ["m", "l", "s"]
species= ["Hantavirus_Z10", "Orthohantavirus_hantanense", "Orthohantavirus_puumalaense",
            "Orthohantavirus_seoulense", "Orthohantavirus_tulaense"]

include: "rules/fetch_from_ncbi.smk"
include: "rules/create_species_tree.smk"
include: "rules/diamond_sort.smk"
include: "rules/augur_curate.smk"

rule all:
    input:
        "data/ncbi_dataset_report_raw.tsv",
        "data/ncbi_dataset.zip",
        "data/ncbi_dataset_sequences.fasta",
        expand("data/refseqs/proteins/{acc}.fasta", acc=ref_acc),
        expand("results/species_tree/aligned_{segment}.fasta", segment=segment),
        expand("results/species_tree/aligned_{segment}.fasta.treefile", segment=segment),
        expand("results/species_tree/rooted_ladder_{segment}.pdf", segment=segment),
        "data/diamond_db/refseq_segments.fasta",
        "data/diamond_db/diamond.dmnd",
        "results/diamond_alignments.tsv",
        "data/ncbi_dataset_seq_assigned.tsv",
        rules.add_missing_translations.output,
        rules.graph_seq_assignment.output,
        expand("results/curated_seq/{species}/{species}_{segment}_metadata.csv",
        species=species, segment=segment),
        expand("results/curated_seq/{species}/{species}_{segment}_seq.fasta", species=species, segment=segment),
        expand("results/ncbi.ndjson/{species}/{species}_{segment}.ndjson", species=species, segment=segment)

    

