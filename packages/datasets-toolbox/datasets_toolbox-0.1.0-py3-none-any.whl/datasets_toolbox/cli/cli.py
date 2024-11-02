import click
from .commands.modify import modify
from .commands.inspect import inspect
from .commands.import_data import import_data


@click.group()
def cli():
    """Datasets CLI"""
    pass


cli.add_command(import_data)
cli.add_command(modify)
cli.add_command(inspect)

if __name__ == "__main__":
    cli()
