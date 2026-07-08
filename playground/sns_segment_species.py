#%%
import pandas as pd
import seaborn as sns
sns.set_theme()
#%%
metadata_file = "../data/ncbi_dataset_report_raw.tsv"
metadata = pd.read_csv(metadata_file, sep="\t")
segment_labels = ["S", "L", "M"]
metadata["Segment_clean"] = metadata["Segment"].where(
    metadata["Segment"].isin(segment_labels), "No Entry")

# %%
sns.displot(data=metadata, x="Length", hue = "Segment_clean", bins = 100)
