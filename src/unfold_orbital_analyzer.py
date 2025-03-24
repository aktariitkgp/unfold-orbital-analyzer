import argparse
import re

def parse_orbital_info(out_filename):
    orbitals = []
    current_atom_number = None
    current_element = None
    found_header = False

    with open(out_filename, 'r') as f:
        for line in f:
            # Search for the header line
            if "The sequence for the orbital weights in System.Name.unfold_orbup(dn)" in line:
                found_header = True
                continue  # Skip the header line itself

            # Only start parsing after the header is found
            if not found_header:
                continue

            line = line.strip()
            if not line:
                continue

            tokens = line.split()
            if not tokens:
                continue

            # Skip lines that don't start with a number (e.g., headers or comments)
            if not tokens[0].isdigit():
                continue

            # Extract orbital index
            try:
                orbital_index = int(tokens[0])
            except ValueError:
                continue  # Skip lines where the first token isn't an integer

            # Check if this line starts a new atom
            # Ensure tokens[1] is a valid atom number and tokens[2] is an element symbol
            if (
                len(tokens) >= 3 
                and tokens[1].isdigit() 
                and re.fullmatch(r'^[A-Z][a-z]?$', tokens[2])
            ):
                current_atom_number = int(tokens[1])
                current_element = tokens[2]
                orbital_info = tokens[3:]
            else:
                orbital_info = tokens[1:]

            if not orbital_info:
                continue

            n = orbital_info[0]
            orbital_type = ' '.join(orbital_info[1:]).strip()  # Trim extra spaces
            orbitals.append({
                'index': orbital_index,
                'atom_number': current_atom_number,
                'element': current_element,
                'n': n,
                'orbital_type': orbital_type
            })

    return orbitals


def main():
    parser = argparse.ArgumentParser(description='Sum orbital weights from unfolding calculation.')
    parser.add_argument('out_file', help='The .out file containing orbital indices')
    parser.add_argument('orb_file', help='The .unfold_orbup/dn file with weights')
    parser.add_argument('--atoms', type=int, nargs='+', help='Atom numbers to select (e.g., 1 2). Use with --element.')
    parser.add_argument('--element', type=str, required=True, help='Element symbol (e.g., Cu)')
    parser.add_argument('--orbital', type=str, nargs='+', help='Orbital type(s) to select (e.g., s, p, d, px, dxy)')
    parser.add_argument('--all_atoms', action='store_true', help='Select all atoms of the specified element')
    parser.add_argument('--all_orbitals', action='store_true', help='Select all orbitals of the specified atoms/element')
    parser.add_argument('--output', type=str, default='output.dat', help='Output .dat file name (default: output.dat)')
    args = parser.parse_args()

    # Validate arguments
    if not args.all_orbitals and not args.orbital:
        print("Error: Either specify --orbital or use --all_orbitals to select all orbitals.")
        return
    if not args.all_atoms and not args.atoms:
        print("Error: Either specify --atoms or use --all_atoms to select all atoms of the element.")
        return

    orbitals = parse_orbital_info(args.out_file)

    # Determine selected atoms
    if args.all_atoms:
        # Get all unique atom numbers for the specified element
        selected_atoms = list({orb['atom_number'] for orb in orbitals if orb['element'] == args.element})
        if not selected_atoms:
            print(f"No atoms found for element {args.element}.")
            return
    else:
        selected_atoms = args.atoms

    # Collect selected orbital indices
    selected_indices = []
    for orb in orbitals:
        if (orb['element'] == args.element and
            orb['atom_number'] in selected_atoms):
            if args.all_orbitals:
                # Select all orbitals for the specified atoms
                selected_indices.append(orb['index'])
            else:
                # Select orbitals based on the --orbital argument (flexible matching)
                for orbital_arg in args.orbital:
                    if orbital_arg.lower() in orb['orbital_type'].lower():  # Case-insensitive matching
                        selected_indices.append(orb['index'])
                        break  # Avoid duplicates

    if not selected_indices:
        print("No orbitals matched the criteria.")
        return

    # Write results to output file
    with open(args.output, 'w') as outfile:
        with open(args.orb_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                parts = line.split()
                if len(parts) < 3:
                    continue
                k, energy = parts[0], parts[1]
                weights = parts[2:]
                total = 0.0
                for idx in selected_indices:
                    if idx - 1 < len(weights):
                        total += float(weights[idx - 1])
                outfile.write(f"{k} {energy} {total:.6f}\n")

    print(f"Results written to {args.output}")

if __name__ == "__main__":
    main()
