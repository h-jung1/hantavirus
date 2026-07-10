
rule get_diamond_proteins:
    input:
       s=rules.sort_by_length.output.s,
       m=rules.sort_by_length.output.m,
       l=rules.sort_by_length.output.l,
    output:
        "data/diamond_db/refseq_segments.fasta",
    conda:
        "../config/conda_envs/bioinformatics.yaml",
    shell:
        """
        python scripts/get_diamond_proteins.py \
        --input_s {input.s} \
        --input_m {input.m} \
        --input_l {input.l} \
        --output {output}
        """

rule make_diamond_db:
    input:
        rules.get_diamond_proteins.output,
    output:
        "data/diamond_db/diamond.dmnd",
    conda:
        "../config/conda_envs/bioinformatics.yaml",
    shell:
        """
        diamond makedb \
            --in {input} \
            -d {output}
        """

rule diamond_align:
    input:
        fasta_seq = "data/ncbi_dataset_sequences.fasta",
        diamond_db = rules.make_diamond_db.output,
    output:
        diamond_tsv = "results/diamond_alignments.tsv",
    conda:
        "../config/conda_envs/bioinformatics.yaml",
    threads: 8
    shell:
        """
        diamond blastx \
            --query {input.fasta_seq} \
            --threads {threads} \
            --max-target-seqs 1 \
            --db {input.diamond_db} \
            --out {output.diamond_tsv} \
            --outfmt 6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore
        """
