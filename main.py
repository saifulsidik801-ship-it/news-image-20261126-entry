# A working news-image-daily entry (Python 3.13, standard library only): its image is the
# entry.png beside this file, and the program copies it to /output/entry.png.
# The image was drawn by draw.py in this repository (Pillow, DejaVu fonts, no network):
# a 1024x1024 newspaper front page summing up Thursday 26 November 2026 — 26 stories,
# all of which happened or were first reported on that day, with a DATE CHECK box listing
# the 25 November stories that were checked and left out.
#
# Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import os
import shutil

out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
os.makedirs(out_dir, exist_ok=True)
src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
shutil.copyfile(src, os.path.join(out_dir, "entry.png"))
