#%%
from Bio import Phylo
import argparse
from pathlib import Path
import copy
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
# %%
def parse_args():
    parser = argparse.ArgumentParser(
        description ="root tree at midpoint and ladderize")
    
    parser.add_argument("--input", help="Path to input file")
    parser.add_argument("--output", help="Path to output file")

    return parser.parse_args()
#%%

def main():
    args = parse_args()

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    tree = Phylo.read(args.input, "newick")
    newtree = copy.deepcopy(tree)
    newtree.root_at_midpoint()
    newtree.ladderize()

    fig = plt.figure(figsize=(18, 8))
    ax = fig.add_subplot(1, 1, 1)
    Phylo.draw(newtree, axes=ax, do_show=False)
    plt.setp(ax.texts, fontsize=8)
    fig.savefig(args.output, bbox_inches="tight")

#%%
if __name__ == "__main__":
    main()

