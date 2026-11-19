import argparse
from chemcli.lookup import load_elements, find_elements, display_elements
from chemcli.parser import calculate_molarmass, display_molar_mass
from rich.console import Console

console = Console()

def main():
    parser = argparse.ArgumentParser(prog="chemcli", description="Periodic table lookup and molar mass calculator")
    subparsers = parser.add_subparsers(dest="command", required=True)
    lookup_parser = subparsers.add_parser("lookup", help="Look up and element by name, symbol or atomic mass")
    lookup_parser.add_argument("query", help="Name, symbol or atomic mass")
    mass_parser = subparsers.add_parser("mass", help="Calculate molar mass and percentage composition of a given formula")
    mass_parser.add_argument("formula", help="Chemical formula (eg. H2SO4)")
    args = parser.parse_args()
    elements = load_elements()

    try:
        if args.command == "lookup":
            element=find_elements(args.query, elements)
            if element is None:
                console.print(f"[bold red]Error: [/] No element found matching '{args.query}")
            else:
                display_elements(element)

        elif args.command == "mass":
            total_mass, breakdown = calculate_molarmass(args.formula, elements)
            display_molar_mass(args.formula, total_mass, breakdown)
    except ValueError as e:
        console.print(f"[bold red] Error: [/] {e}")


if __name__ == "__main__":
    main()
