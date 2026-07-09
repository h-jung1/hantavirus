#%%
import pandas as pd
import seaborn as sns
sns.set_theme()

metadata_file = "../data/ncbi_dataset_report_raw.tsv"
metadata = pd.read_csv(metadata_file, sep="\t")
metadata['Release_Date'] = pd.to_datetime(metadata['Release date'])
metadata["Release_Year"] = metadata["Release_Date"].dt.year

top_species = ["Orthohantavirus puumalaense", "Orthohantavirus hantanense", "Orthohantavirus seoulense", "Orthohantavirus tulaense"]
filtered = metadata[metadata["Virus Name"].isin(top_species)]
# %%
sns.displot(data=filtered, x="Release_Year", hue="Virus Name", kind="ecdf", stat="count")

