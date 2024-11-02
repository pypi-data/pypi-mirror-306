import click
import json
import os
from pathlib import Path
from ...utils import get_configs_splits


@click.command()
@click.pass_context
def sync(ctx):
    """Sync dataset metadata and file consistency"""
    config = ctx.parent.params["config"]
    split = ctx.parent.params["split"]

    targets = get_configs_splits(config, split)
    if not targets:
        click.echo("No valid config/split combinations found")
        return

    for cfg, spl in targets:
        click.echo(f"Syncing {cfg}/{spl}")
        dataset_dir = Path(f"{cfg}/{spl}")
        metadata_file = dataset_dir / "metadata.jsonl"

        if not metadata_file.exists():
            click.echo(f"No metadata file found in {cfg}/{spl}, skipping")
            continue

        # Load existing metadata
        entries = []
        with open(metadata_file, "r") as f:
            for line in f:
                entry = json.loads(line)
                file_path = dataset_dir / entry["file_name"]

                # Skip entries with missing files
                if not file_path.exists():
                    click.echo(
                        f"Removing metadata for missing file: {entry['file_name']}"
                    )
                    continue

                # Add id field if missing
                if "id" not in entry:
                    entry["id"] = os.path.splitext(entry["file_name"])[0]
                    click.echo(f"Added missing id field for: {entry['file_name']}")

                entries.append(entry)

        # Save updated metadata
        with open(metadata_file, "w") as f:
            for entry in entries:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        click.echo(f"Synced {cfg}/{spl}: {len(entries)} valid entries remaining")
