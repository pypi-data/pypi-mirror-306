import click
from .slice import slice
from .resample import resample
from .transcribe import transcribe
from .sync import sync


@click.group()
@click.option("--config", help="Configuration name (e.g. language)")
@click.option("--split", help="Split name (train/validation/test)")
def modify(config: str, split: str):
    """Modify dataset with various actions"""
    pass


modify.add_command(slice)
modify.add_command(resample)
modify.add_command(transcribe)
modify.add_command(sync)

__all__ = ["modify"]
