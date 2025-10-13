#!/usr/bin/env python3
import os, sys, unicodedata, argparse
from collections import defaultdict

def normalize_name(name: str) -> str:
    # Accent-insensitive + case-insensitive + light punctuation/space normalization
    n = unicodedata.normalize("NFKD", name)
    n = "".join(c for c in n if not unicodedata.combining(c))  # strip diacritics
    n = n.casefold()
    n = n.replace("_", " ").replace("-", " ")
    n = " ".join(n.split())
    return n

def main():
    p = argparse.ArgumentParser(description="Find duplicate directories by accent-insensitive, case-insensitive matching.")
    p.add_argument("root", nargs="?", default="/mnt/sushifm", help="Root directory to scan (default: /mnt/sushifm)")
    args = p.parse_args()
    root = args.root

    if not os.path.isdir(root):
        print(f"ERROR: {root!r} is not a directory.")
        sys.exit(1)

    # Maps for duplicates
    by_parent_and_key = defaultdict(list)
    by_key_global = defaultdict(list)

    # Walk the tree
    for dirpath, dirnames, _ in os.walk(root, topdown=True, followlinks=False):
        for dn in dirnames:
            full = os.path.join(dirpath, dn)
            key = normalize_name(dn)
            by_parent_and_key[(dirpath, key)].append(full)
            by_key_global[key].append(full)

    # Prepare report
    lines = []
    lines.append(f"Duplicate directory report (accent/case-insensitive)\nRoot: {root}\n")

    # Section 1: duplicates within the same parent
    within_parent = []
    for (parent, key), paths in sorted(by_parent_and_key.items()):
        if len(paths) > 1:
            real_names = {os.path.basename(p) for p in paths}
            if len(real_names) > 1:
                within_parent.append((parent, key, sorted(paths)))

    if within_parent:
        lines.append("=== Duplicates within the SAME parent directory ===")
        for parent, key, paths in within_parent:
            lines.append(f"\nParent: {parent}\nNormalized name: {key}\nMatches:")
            for p in paths:
                lines.append(f"  - {p}")
    else:
        lines.append("=== Duplicates within the SAME parent directory ===\nNone found.")

    # Section 2: cross-parent duplicates
    cross_parent = []
    for key, paths in sorted(by_key_global.items()):
        parents = {os.path.dirname(p) for p in paths}
        real_names = {os.path.basename(p) for p in paths}
        if len(parents) > 1 and len(real_names) > 1:
            cross_parent.append((key, sorted(paths)))

    if cross_parent:
        lines.append("\n=== Cross-parent duplicates (same normalized name in different parents) ===")
        for key, paths in cross_parent:
            lines.append(f"\nNormalized name: {key}\nOccurrences:")
            for p in paths:
                lines.append(f"  - {p}")
    else:
        lines.append("\n=== Cross-parent duplicates ===\nNone found.")

    report_path = "/tmp/dupe_dirs_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("\n".join(lines[:200]))
    print(f"\n---\nFull report saved to: {report_path}")
    print("Tip: open it with `less -R /tmp/dupe_dirs_report.txt`")

if __name__ == "__main__":
    main()
