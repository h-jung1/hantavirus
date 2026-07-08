#%%
import pandas as pd
import seaborn as sns
sns.set_theme()
#%%
metadata_file = "../data/ncbi_dataset_report_raw.tsv"
metadata = pd.read_csv(metadata_file, sep="\t")
#%%
top_species = metadata["Virus Name"].value_counts().head(9).index
metadata["Virus_refined"] = metadata["Virus Name"].where(
    metadata["Virus Name"].isin(top_species), "Others")
# %%
sns.catplot(data=metadata, y="Virus_refined", hue="Virus_refined", kind="count")

# %%
