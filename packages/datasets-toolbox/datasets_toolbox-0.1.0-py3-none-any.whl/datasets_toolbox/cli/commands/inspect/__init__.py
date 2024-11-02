import click
import tqdm
from pathlib import Path
from ...utils import get_configs_splits, load_metadata, calculate_audio_duration


@click.group()
@click.option("--config", help="Configuration name (e.g. language)")
@click.option("--split", help="Split name (train/validation/test)")
def inspect(config: str, split: str):
    """Inspect dataset with various metrics"""
    pass


@click.command()
@click.pass_context
def hours(ctx):
    """Calculate total hours of audio in dataset"""
    config = ctx.parent.params["config"]
    split = ctx.parent.params["split"]

    targets = get_configs_splits(config, split)

    total_hours = 0.0
    for cfg, spl in targets:
        hours = 0.0
        entries = load_metadata(Path(f"{cfg}/{spl}/metadata.jsonl"))

        for entry in tqdm(entries, desc=f"Calculating duration for {cfg}/{spl}"):
            file_path = f"{cfg}/{spl}/{entry['file_name']}"
            hours += calculate_audio_duration(file_path)

        click.echo(f"{cfg}/{spl}: {hours:.2f} hours")
        total_hours += hours

    click.echo(f"Total: {total_hours:.2f} hours")


inspect.add_command(hours)

__all__ = ["inspect"]
