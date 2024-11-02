import click
import shutil
import librosa
import soundfile as sf
from pathlib import Path
from tqdm import tqdm
from ...utils import get_configs_splits, load_metadata


@click.command()
@click.option("--sr", type=int, default=16000, help="Target sample rate in Hz")
@click.option("--mono", is_flag=True, default=False, help="Convert to mono")
@click.pass_context
def resample(ctx, sr: int, mono: bool):
    """Resample audio files to target sample rate"""
    config = ctx.parent.params["config"]
    split = ctx.parent.params["split"]

    targets = get_configs_splits(config, split)
    if not targets:
        click.echo("No valid config/split combinations found")
        return

    for cfg, spl in targets:
        click.echo(f"Resampling {cfg}/{spl} to {sr}Hz{' (mono)' if mono else ''}")
        dataset_dir = Path(f"{cfg}/{spl}")
        temp_dir = dataset_dir / "temp_resampled"
        temp_dir.mkdir(exist_ok=True)

        try:
            # Load metadata
            entries = load_metadata(dataset_dir / "metadata.jsonl")

            # Process each file with progress bar
            for entry in tqdm(entries, desc="Resampling files"):
                file_path = dataset_dir / entry["file_name"]

                if not file_path.exists():
                    click.echo(f"Warning: File {file_path} not found, skipping")
                    continue

                # Load and resample
                y, orig_sr = librosa.load(str(file_path), sr=None, mono=mono)
                if orig_sr != sr:
                    y = librosa.resample(y, orig_sr=orig_sr, target_sr=sr)

                # Save to temp directory
                temp_path = temp_dir / entry["file_name"]
                if mono:
                    sf.write(str(temp_path), y, sr)
                else:
                    if len(y.shape) > 1:
                        y = y.T
                    sf.write(str(temp_path), y, sr)

            # Replace old files with new ones
            for file_path in dataset_dir.glob("*.wav"):
                file_path.unlink()

            for file_path in temp_dir.glob("*.wav"):
                shutil.move(str(file_path), dataset_dir / file_path.name)

        finally:
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
