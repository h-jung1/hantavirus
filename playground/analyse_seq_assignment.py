#%%
import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt
#%%
diamond_tsv=pd.read_csv("../results/diamond_alignments.tsv", sep='\t', header = None)
diamond_tsv.columns=["Accession", "sseqid", "pident", "length", "mismatch",
                        "gapopen", "qstart", "qend", "sstart", "send",
                        "evalue", "bitscore"]
split_sseqid = diamond_tsv["sseqid"].str.split('|', expand=True)
diamond_tsv["assigned_species_id"]=split_sseqid[0]
diamond_tsv["assigned_species"]=split_sseqid[1]
diamond_tsv["assigned_segment"]=split_sseqid[2]
diamond_m = diamond_tsv[diamond_tsv["assigned_segment"] == "M"]
diamond_s = diamond_tsv[diamond_tsv["assigned_segment"] == "S"]
diamond_l = diamond_tsv[diamond_tsv["assigned_segment"] == "L"]
#%%
# This code plots all the M segments
plot = sns.catplot(diamond_m, x="assigned_species", y="pident", kind="box", height=8, aspect=2)
plot.set_xticklabels(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("../results/graphics/pident_segment_s.png")
# %%
# This code plots all the S segments
plot = sns.catplot(diamond_s, x="assigned_species", y="pident", kind="box", height=8, aspect=2)
plot.set_xticklabels(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("../results/graphics/pident_segment_m.png")
#%%
# This code plots all the L segments
plot = sns.catplot(diamond_l, x="assigned_species", y="pident",kind="box", height=8, aspect=2)
plot.set_xticklabels(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("../results/graphics/pident_segment_l.png")
# %%
