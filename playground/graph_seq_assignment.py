#%%
import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt
#%%
# Create matrix of species vs assigned species
metadata=pd.read_csv("../data/ncbi_dataset_seq_assigned.tsv", sep='\t')
confusion = pd.crosstab(metadata["Virus Name"], metadata["assigned_species"])

annot_labels = confusion.astype(str)
annot_labels[confusion < 20] = ""

plt.figure(figsize=(15,15))
sns.heatmap(confusion, annot=annot_labels, cmap="crest", fmt="", linewidth=0.7)
plt.savefig("../results/graphics/species_matrix.png", bbox_inches="tight")

#%%
# Create matrix of segments vs assigned segments
metadata=pd.read_csv("../data/ncbi_dataset_seq_assigned.tsv", sep='\t')

confusion = pd.crosstab(metadata["Segment"], metadata["assigned_segment"])
plt.figure(figsize=(10,12))
sns.heatmap(confusion, annot=True, cmap="crest")
plt.savefig("../results/graphics/segment_matrix.png")

# %%
# Create histogramm of pident    
diamond_tsv=pd.read_csv("../results/diamond_alignments.tsv", sep='\t', header = None)
diamond_tsv.columns=["Accession", "sseqid", "pident", "length", "mismatch",
                        "gapopen", "qstart", "qend", "sstart", "send",
                        "evalue", "bitscore"]
plt.figure(figsize=(10,12))
sns.displot(diamond_tsv, x="pident")
plt.savefig("../results/graphics/pident_distribution.png")
