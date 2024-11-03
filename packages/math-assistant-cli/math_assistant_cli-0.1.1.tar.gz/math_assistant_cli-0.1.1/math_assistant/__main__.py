from .cli import main


def run_cli():
    """Entry point for the command-line interface."""
    main(prog_name="math_assistant")


if __name__ == "__main__":
    run_cli()
