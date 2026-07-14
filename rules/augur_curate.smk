
rule filter_by_pident:
    input:
        metadata=rules.add_to_metadata.output,
    params:
        species="{species}",
        segment="{segment}",
    output:
        "results/curated_seq/{species}/{species}_{segment}_metadata.csv",
    shell:
        """
        python scripts/filter_by_pident.py \
        --metadata {input.metadata} \
        --species {params.species} \
        --segment {params.segment} \
        --pident 90 \
        --output_dir {output}
        """

rule concatenate_sequences:
    input:
        metadata=rules.filter_by_pident.output,
    output:
        "results/curated_seq/{species}/{species}_{segment}_seq.fasta",
    shell: 
        """
        python scripts/concatenate_sequences.py \
        --input {input} \
        --output {output}
        """

rule format_ncbi_datasets_ndjson:
    input:
        ncbi_dataset_sequences=rules.concatenate_sequences.output,
        ncbi_dataset_tsv=rules.filter_by_pident.output,
    output:
        ndjson="results/ncbi.ndjson/{species}/{species}_{segment}.ndjson",
    conda:
        "../config/conda_envs/nextstrain.yaml"
    shell:
        """
        augur curate passthru \
            --metadata {input.ncbi_dataset_tsv} \
            --fasta {input.ncbi_dataset_sequences} \
            --seq-id-column accession_version \
            --seq-field sequence \
            --unmatched-reporting warn \
            --duplicate-reporting warn \
            > {output.ndjson}
        """
