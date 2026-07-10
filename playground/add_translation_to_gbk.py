#%%
from Bio import SeqIO
#%%
sequence = SeqIO.read("../data/fasta_sequences/NC_005225.1.fasta", "fasta")

# %%
translated = sequence.seq[36:].translate()
# %%
translation_length = translated.find("*")
# %%
protein_start = 36
protein_end = protein_start + translation_length*3
print(protein_end)
# %%
clean_translation = sequence.seq[protein_start:protein_end].translate()
print(clean_translation)
# %%
