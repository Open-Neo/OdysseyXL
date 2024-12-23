from diffusers import DiffusionPipeline
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import os
import sys

# Initialize the console
console = Console()

# Display a welcome banner
def display_banner():
    banner = """
 ██████╗ ██████╗ ██╗   ██╗███████╗███████╗███████╗██╗   ██╗██╗  ██╗██╗     
██╔═══██╗██╔══██╗╚██╗ ██╔╝██╔════╝██╔════╝██╔════╝╚██╗ ██╔╝╚██╗██╔╝██║     
██║   ██║██║  ██║ ╚████╔╝ ███████╗███████╗█████╗   ╚████╔╝  ╚███╔╝ ██║     
██║   ██║██║  ██║  ╚██╔╝  ╚════██║╚════██║██╔══╝    ╚██╔╝   ██╔██╗ ██║     
╚██████╔╝██████╔╝   ██║   ███████║███████║███████╗   ██║   ██╔╝ ██╗███████╗
 ╚═════╝ ╚═════╝    ╚═╝   ╚══════╝╚══════╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝
                                                                           
    OdysseyXL Model Inference Script
    """
    console.print(Panel(banner, style="bold cyan"))

def choose_model():
    table = Table(title="Available OdysseyXL Models", style="bold green")
    table.add_column("Option", justify="center")
    table.add_column("Model Name", justify="left")

    models = {
        1: "Spestly/OdysseyXL-1.0",
        2: "Spestly/OdysseyXL-2.0",
        3: "Spestly/OdysseyXL-3.0",
        4: "Spestly/OdysseyXL-4.0 (New!)",
    }

    for option, model in models.items():
        table.add_row(str(option), model)

    console.print(table)

    choice = console.input("[bold yellow]Select a model by entering its option number:[/] ")

    try:
        choice = int(choice)
        if choice in models:
            return models[choice]
        else:
            raise ValueError
    except ValueError:
        console.print("[bold red]Invalid choice. Please try again.[/]")
        return choose_model()

def download_and_infer(model_name):
    console.print(f"\n[bold blue]Downloading model: [cyan]{model_name}[/cyan]...[/bold blue]")
    try:
        pipe = DiffusionPipeline.from_pretrained(model_name)
        console.print(f"[bold green]Successfully downloaded {model_name}![/bold green]\n")

        # Prompt for inference
        prompt = console.input("[bold yellow]Enter your text prompt for inference:[/] ")
        console.print("[bold blue]Generating image...[/bold blue]")

        # Perform inference
        image = pipe(prompt).images[0]

        # Save the result
        output_path = os.path.join(os.getcwd(), f"{model_name.split('/')[-1]}_output.png")
        image.save(output_path)
        console.print(f"[bold green]Image generated and saved at: {output_path}[/bold green]")

    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")

def main():
    display_banner()
    model_name = choose_model()
    download_and_infer(model_name)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Exiting... Goodbye![/bold red]")
        sys.exit(0)
