#%%
import pandas as pd
import seaborn as sns
sns.set_theme()
#%%
file = "../data/refseqs/protein_length.csv"
metadata = pd.read_csv(file)

# %%
sns.displot(data=metadata, x="seq_len", bins = 100)
# %%
