
rule filter_by_pident:
    input:
        metadata=rules.add_to_metadata.output,
    params:
        species="{species}",
        segment="{segment}",
        pident=PIDENT,
    output:
        "results/curated_seq/{species}/{species}_{segment}_metadata.csv",
    shell:
        """
        python scripts/filter_by_pident.py \
        --metadata {input.metadata} \
        --species {params.species} \
        --segment {params.segment} \
        --pident {params.pident} \
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

def format_field_map(field_map: dict[str, str]) -> list[str]:
    """
    Format entries to the format expected by `augur curate --field-map`.

    When used in a Snakemake shell block, the list is automatically expanded and
    spaces are handled by quoted interpolation.
    """
    return  [f'{key}={value}' for key, value in field_map.items()]

rule curate:
    input:
        sequences_ndjson=rules.format_ncbi_datasets_ndjson.output,
        local_geolocation_rules=config["curate"]["local_geolocation_rules"],
    output:
        metadata="data/curated_metadata/{species}_{segment}.tsv",
        sequences="data/curated_sequences/{species}_{segment}.fasta",
    params:
        field_map=format_field_map(config["curate"]["field_map"]),
        strain_regex=config["curate"]["strain_regex"],
        strain_backup_fields=config["curate"]["strain_backup_fields"],
        date_fields=config["curate"]["date_fields"],
        expected_date_formats=config["curate"]["expected_date_formats"],
        genbank_location_field=config["curate"]["genbank_location_field"],
        articles=config["curate"]["titlecase"]["articles"],
        abbreviations=config["curate"]["titlecase"]["abbreviations"],
        titlecase_fields=config["curate"]["titlecase"]["fields"],
        authors_field=config["curate"]["authors_field"],
        authors_default_value=config["curate"]["authors_default_value"],
        # abbr_authors_field=config["curate"]["abbr_authors_field"],
        # annotations_id=config["curate"]["annotations_id"],
        id_field=config["curate"]["output_id_field"],
        sequence_field=config["curate"]["output_sequence_field"],
    conda:
        "../config/conda_envs/nextstrain.yaml"
    shell:
        """
        cat {input.sequences_ndjson} \
            | augur curate rename \
                --field-map {params.field_map:q} \
            | augur curate normalize-strings \
            | augur curate transform-strain-name \
                --strain-regex {params.strain_regex} \
                --backup-fields {params.strain_backup_fields} \
            | augur curate format-dates \
                --date-fields {params.date_fields} \
                --expected-date-formats {params.expected_date_formats} \
            | augur curate parse-genbank-location \
                --location-field {params.genbank_location_field} \
            | augur curate titlecase \
                --titlecase-fields {params.titlecase_fields} \
                --articles {params.articles} \
                --abbreviations {params.abbreviations} \
            | augur curate abbreviate-authors \
                --authors-field {params.authors_field} \
                --default-value {params.authors_default_value} \
            | augur curate apply-geolocation-rules \
                --geolocation-rules {input.local_geolocation_rules} \
                --output-metadata {output.metadata} \
                --output-fasta {output.sequences} \
                --output-id-field {params.id_field} \
                --output-seq-field {params.sequence_field}
        """

# rule subset_curated_metadata_columns:
#     input:
#         metadata=rules.curate.output,
#     output:
#         metadata="data/metadata_subset.tsv",
#     params:
#         metadata_fields=",".join(config["curate"]["metadata_columns"]),
#     shell:
#         r"""
#         exec &> >(tee {log:q})

#         csvtk cut -t -f {params.metadata_fields} \
#           {input.metadata} \
#         > {output.metadata}
#         """
