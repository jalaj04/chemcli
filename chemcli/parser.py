from rich.console import Console
from rich.table import Table
from chemcli.lookup import load_elements, find_elements

console = Console()

def parse_formula(formula):
    i = 0
    stack=[{}]
    while i < len(formula):
    
        if formula[i] == "(":
            stack.append({})
            i+=1

        elif formula[i]==")":
            i+=1
            num_str=""
            while i < len(formula) and formula[i].isdigit():
                num_str+=str(formula[i])
                i+=1
            if num_str:
                multiplier=int(num_str)
            else:
                multiplier=1

            if len(stack) == 1:
                raise ValueError("Missing a bracket.")

            group = stack.pop()
            for symbol, count in group.items():
                stack[-1][symbol] = stack[-1].get(symbol, 0) + (count * multiplier)
            

        elif formula[i].isupper():
            symbol=formula[i]
            i+=1
            while i < len(formula) and formula[i].islower():
                symbol+=formula[i]
                i+=1
            num_str=""
            while i < len(formula) and formula[i].isdigit():
                num_str+=str(formula[i])
                i+=1
                
            if num_str:
                count = int(num_str)
            else:
                count = 1
            stack[-1][symbol] = stack[-1].get(symbol, 0) + count

        else:
            raise ValueError(f"Invalid character: {formula[i]}")

    if len(stack) != 1:
        raise ValueError("Unclosed Bracket.")
            
            
        
    return stack[0]
    

def calculate_molarmass(formula, elements):
    atom_counts = parse_formula(formula)
    if not atom_counts:
        raise ValueError("Formula cannot be empty.")
    breakdown=[]
    total_mass=0.0
    for symbol, count in atom_counts.items():
        element = find_elements(symbol, elements)
        if element == None:
            raise ValueError("Unknown elements symbol")
        subtotal = element["atomic_mass"]  * count
        total_mass+=subtotal
        breakdown.append({
            "symbol": element["symbol"],
            "name": element["name"],
            "count": count,
            "atomic_mass": element["atomic_mass"],
            "subtotal": subtotal
        })

    for item in breakdown:
        item["percent"] = (item["subtotal"] / total_mass) *100

    return total_mass, breakdown


def display_molar_mass(formula, total_mass, breakdown):
    table = Table(title=f"Molar Mass Breakdown: [bold cyan]{formula}[/]")
    table.add_column("Elements")
    table.add_column("Count")
    table.add_column("Atomic Mass (u)")
    table.add_column("Subtotal (g/mol)")
    table.add_column("Composition")

    for item in breakdown:
        table.add_row(
            f"{item["name"]} ({item["symbol"]})",
            str({item["count"]}),
            f"{item["atomic_mass"]:.3f}",
            f"{item["subtotal"]:.3f}",
            f"{item["percent"]:.2f}%"
        )


    console.print(table)
    console.print(f"[bold green]Total mass:[/] [bold white]{total_mass:.3f} g/mol[/]")


if __name__ == "__main__":
    all_elements = load_elements()
    user_input = input("Enter a formula: ").strip()
    try:
        total_mass, breakdown = calculate_molarmass(user_input, all_elements)
        display_molar_mass(user_input, total_mass, breakdown)
    except ValueError as e:
        console.print("[bold red] Error: {e}")