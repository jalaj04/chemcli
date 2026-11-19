from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import json
from pathlib import Path
console = Console()

def load_elements():
    data = Path(__file__).parent / "elements.json"
    with open (data, mode="r", encoding="utf-8") as read_file:
        elements_data = json.load(read_file)
    return elements_data

def find_elements(query, elements):
    cleanq = query.lower().strip()

    for element in elements:
        if cleanq.isdigit() and element["number"] == int(cleanq):
            return element

        if element["symbol"].lower() == cleanq or element["name"].lower() == cleanq:
            return element

    return None

def display_elements(element):
    table = Table(show_header=False, box=None)
    table.add_column("Property", style="bold cyan")
    table.add_column("Value", style="bold red")

    table.add_row("Atomic Number", str(element["number"]))
    table.add_row("Atomic Mass", f"{element["atomic_mass"]} u")
    table.add_row("Category", element["category"])
    table.add_row("Block / Group / Period", f"{element["block"]}-block | Group {element["group"]} | Period {element["period"]}")
    table.add_row("Electronic Configuration", element["electronic_configuration"])

    panel = Panel(
        table,
        title=f"[bold yellow]{element["name"]} ({element["symbol"]}) [/]",
        expand=False
    )
    console.print(panel)

if __name__ == "__main__":
    all_elements = load_elements()
    user_input = input("Enter a symbol, name or atomic number: ")
    match = find_elements(user_input, all_elements)
    if match:
        display_elements(match)
    else:
        console.print(f"[bold red] Element {user_input} not found[/]")

