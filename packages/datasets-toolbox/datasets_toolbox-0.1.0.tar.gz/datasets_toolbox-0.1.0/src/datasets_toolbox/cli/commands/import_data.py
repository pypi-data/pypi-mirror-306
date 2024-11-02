import click
import glob
import json
import os
import shutil
from pathlib import Path
from tqdm import tqdm


@click.command(name="import")
@click.argument("sources", nargs=-1)
@click.option("--config", default="default", help="Configuration name (e.g. language)")
@click.option("--split", default="train", help="Split name (train/validation/test)")
def import_data(sources, config: str, split: str):
    """Import data into datasets structure"""
    click.echo(f"Importing data into {config}/{split} from {sources}")

    # Create config/split directory if it doesn't exist
    target_dir = Path(f"{config}/{split}")
    target_dir.mkdir(parents=True, exist_ok=True)

    # Create or load existing metadata file
    metadata_file = target_dir / "metadata.jsonl"
    existing_files = set()
    if metadata_file.exists():
        with open(metadata_file, "r") as f:
            for line in f:
                entry = json.loads(line)
                existing_files.add(entry["file_name"])

    # Process source files
    with open(metadata_file, "a") as f:
        all_files = []
        for source in sources:
            all_files.extend(glob.glob(source))

        for file_path in tqdm(all_files, desc="Importing files"):
            file_name = os.path.basename(file_path)

            if file_name in existing_files:
                continue

            # Copy file to target directory
            shutil.copy2(file_path, target_dir / file_name)

            # Add metadata entry with id (filename without extension)
            metadata = {
                "id": os.path.splitext(file_name)[0],
                "file_name": file_name,
            }
            f.write(json.dumps(metadata) + "\n")
            existing_files.add(file_name)
