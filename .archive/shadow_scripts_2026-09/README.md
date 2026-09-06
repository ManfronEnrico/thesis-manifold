# Shadow script archived 2026-09-06

`utility_scripts/scripts/generate_systemB_diagram.py` was a byte-identical copy
of the tier-05 generator (P0046 F8, md5 `cc6f393695...`). Two copies of one
generator means two places to fix and no rule about which is authoritative.

The live copy is now `05_thesis_results/generate_systemB_diagram.py`, repointed
through `PATHS.py`.

Note the script itself is under a staleness review (P0046 F25): it diagrams the
abandoned multi-agent writing system, and no chapter cites its output.
