"""Entrypoint: copy the shipped front-page image to the output path."""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGE = "entry.png"

def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, IMAGE)
    dst = os.path.join(out_dir, IMAGE)
    shutil.copyfile(src, dst)
    return 0

if __name__ == "__main__":
    sys.exit(main())
