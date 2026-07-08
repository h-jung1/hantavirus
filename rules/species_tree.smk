
rule extract_proteins:
    input: 
        rules.download_gbk.output,
    output:
        "data/refseqs/proteins/{acc}.fasta",
    shell:
        """
        python scripts/extract_proteins.py \
        --input {input} \
        --output {output}
        """
