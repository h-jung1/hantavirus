
rule extract_proteins:
    input: 
        rules.download_gbk.output,
    output:
        "data/refseqs/proteins/{acc}.fasta",
    conda:
       "../config/conda_envs/bioinformatics.yaml"
    shell:
        """
        python scripts/extract_proteins.py \
        --input {input} \
        --output {output}
        """

rule find_protein_length:
    input: 
        expand("data/refseqs/proteins/{acc}.fasta", acc=ref_acc),
    output:
        "data/refseqs/protein_length.csv"
    conda:
       "../config/conda_envs/bioinformatics.yaml"
    shell:
        """
        python scripts/find_protein_length.py \
        --input {input} \
        --output {output}
        """


rule combine_proteins:
    input:
        expand("data/refseqs/proteins/{acc}.fasta", acc=ref_acc),
    output:
        "data/refseqs/combined/all_proteins.fasta"
    conda:
        "../config/conda_envs/bioinformatics.yaml"
    shell:
        """
        cat {input} > {output}
        """

rule sort_by_length:
    input:
        rules.combine_proteins.output,
    output:
        s="data/refseqs/combined/segment_s.fasta",
        m="data/refseqs/combined/segment_m.fasta",
        l="data/refseqs/combined/segment_l.fasta",
    conda:
        "../config/conda_envs/bioinformatics.yaml",
    shell:
        """
        python scripts/sort_by_length.py \
        --input {input} \
        --output_s {output.s} \
        --output_m {output.m} \
        --output_l {output.l}
        """


rule align_proteins:
    input:
        "data/refseqs/combined/segment_{segment}.fasta"
    output:
        "results/species_tree/aligned_{segment}.fasta",
    conda:
        "../config/conda_envs/bioinformatics.yaml"
    shell:
        """
        mafft --auto {input} > {output}
      """

rule produce_tree:
    input:
        rules.align_proteins.output,
    output:
        "results/species_tree/aligned_{segment}.fasta.treefile",
    conda:
        "../config/conda_envs/bioinformatics.yaml",
    shell:
        """
        iqtree -s {input} -m JTT -redo
        """

rule root_ladder_tree:
    input:
        rules.produce_trees.output,
    output:
        "results/species_tree/rooted"