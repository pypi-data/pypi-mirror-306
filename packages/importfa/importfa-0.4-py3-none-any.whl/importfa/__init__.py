import os
import sys

fa = os.path.abspath("/".join([sys.argv[0] + "/.."] + [".."] * 1))
sys.path.append(fa)


def importfa_set(x):
    if sys.argv[0].split("/")[-1] == "ipykernel_launcher.py":
        base = os.getcwd()  # Jupyter
    else:
        base = sys.argv[0] + "/.."
    fa = os.path.abspath("/".join([base] + [".."] * x))
    sys.path.append(fa)
