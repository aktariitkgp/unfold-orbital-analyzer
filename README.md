# Unfold Orbital Analyzer

A Python script to analyze orbital weights from unfolding calculations.

## Features
- Extract orbital weights for specific atoms and elements.
- Supports s, p, d, and f orbitals.
- Flexible selection of orbitals (e.g., `px`, `dxy`, `f5z^2-3r^2`).
- Output results to a `.dat` file.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/aktariitkgp/unfold-orbital-analyzer.git
   cd unfold-orbital-analyzer

## User Guideline

1. python3 script.py System.out System.unfold_orb --element [element name] --all_atoms --all_orbitals --output output.dat

2. python3 script.py System.out System.unfold_orb --element [element name] --atoms 1 2 --all_orbitals --output output.dat

3. python3 script.py System.out System.unfold_orb --element [element name] --all_atoms --orbital px py --output output.dat

4. python3 script.py System.out System.unfold_orb --element [element name] --atoms 3 4 --orbital dxy dxz --output output.dat
