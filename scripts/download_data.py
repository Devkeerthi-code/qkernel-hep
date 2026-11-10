"""Download the ATLAS Higgs Boson Machine Learning Challenge 2014 dataset and verify it.

    python scripts/download_data.py            # -> data/atlas-higgs-challenge-2014-v2.csv.gz
    python scripts/download_data.py --out DIR

Source: CERN Open Data Portal, record 328 (doi:10.7483/OPENDATA.ATLAS.ZBP2.M5T8). The file is
65,630,848 bytes with Adler-32 checksum e4717bbe (as recorded in results/data_summary.json).
An existing file with the right size and checksum is left alone.
"""
from __future__ import annotations

import argparse
import sys
import urllib.request
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME = "atlas-higgs-challenge-2014-v2.csv.gz"
URL = f"https://opendata.cern.ch/record/328/files/{NAME}"
SIZE = 65_630_848
ADLER32 = "e4717bbe"


def adler32(path: Path) -> str:
    a = 1
    with path.open("rb") as f:
        while chunk := f.read(1 << 20):
            a = zlib.adler32(chunk, a)
    return f"{a & 0xffffffff:08x}"


def ok(path: Path) -> bool:
    return path.is_file() and path.stat().st_size == SIZE and adler32(path) == ADLER32


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, default=ROOT / "data", help="directory to save into (default: data/)")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    dest = args.out / NAME
    if ok(dest):
        print(f"{dest} already present and verified (adler32 {ADLER32})")
        return
    part = dest.with_suffix(dest.suffix + ".part")
    print(f"downloading {URL}")
    req = urllib.request.Request(URL, headers={"User-Agent": "qkernel-hep-download/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r, part.open("wb") as f:
        done = 0
        while chunk := r.read(1 << 20):
            f.write(chunk)
            done += len(chunk)
            print(f"\r  {done / 1e6:6.1f} / {SIZE / 1e6:.1f} MB", end="", flush=True)
    print()
    if not ok(part):
        got = f"{part.stat().st_size} bytes, adler32 {adler32(part)}"
        part.unlink()
        sys.exit(f"verification failed: expected {SIZE} bytes, adler32 {ADLER32}; got {got}")
    part.replace(dest)
    print(f"saved and verified {dest}")


if __name__ == "__main__":
    main()
