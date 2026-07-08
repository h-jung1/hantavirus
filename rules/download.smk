
rule fetch_ncbi_dataset_package:
    params:
        ncbi_taxon_id=config["ncbi_taxon_id"],
    output:
        dataset_package="../data/ncbi_dataset.zip",
    # Allow retries in case of network errors
    retries: 5
    conda:
        "../config/conda_envs/ncbi.yaml"
    shell:
        """
        datasets download virus genome taxon {params.ncbi_taxon_id:q} \
            --no-progressbar \
            --filename {output.dataset_package}
        """

rule dump_ncbi_dataset_report:
    input:
        dataset_package=rules.fetch_ncbi_dataset_package.output.dataset_package,
    output:
        ncbi_dataset_tsv="../data/ncbi_dataset_report_raw.tsv",
    conda:
        "../config/conda_envs/ncbi.yaml"
    shell:
        """
        dataformat tsv virus-genome \
            --package {input.dataset_package} > {output.ncbi_dataset_tsv}
        """

rule extract_ncbi_dataset_sequences:
    input:
        dataset_package=rules.fetch_ncbi_dataset_package.output.dataset_package,
    output:
        ncbi_dataset_sequences="../data/ncbi_dataset_sequences.fasta",
    conda:
        "../config/conda_envs/ncbi.yaml"
    shell:
        """
        unzip -jp {input.dataset_package} \
            ncbi_dataset/data/genomic.fna > {output.ncbi_dataset_sequences}
        """


rule download_gbk:
    output:
        "data/refseqs/gbk/{acc}.gbk",
    shell:
        """
        python scripts/download_gbk.py \
        --acc {wildcards.acc} \
        --out {output}
        """
