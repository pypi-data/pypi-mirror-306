import click
import json
import librosa
from pathlib import Path
from transformers import pipeline
from accelerate.utils import is_cuda_available, is_mps_available
from tqdm import tqdm
from ...utils import get_configs_splits


@click.command()
@click.option(
    "--model",
    type=str,
    default="openai/whisper-large-v3-turbo",
    help="Model to use for transcription",
)
@click.option(
    "--device",
    type=str,
    default="",
    help="Device to run inference on",
)
@click.option("--batch-size", type=int, default=4, help="Batch size for inference")
@click.option(
    "--column",
    type=str,
    default="transcription",
    help="The column name to put transcription in",
)
@click.pass_context
def transcribe(ctx, model: str, device: str, batch_size: int, column: str):
    """Transcribe audio files using ASR model"""
    config = ctx.parent.params["config"]
    split = ctx.parent.params["split"]

    if device == "":
        device = (
            "cuda" if is_cuda_available() else "mps" if is_mps_available() else "cpu"
        )

    targets = get_configs_splits(config, split)
    if not targets:
        click.echo("No valid config/split combinations found")
        return

    # Initialize ASR pipeline
    click.echo(f"Loading ASR model {model} on {device}")
    pipe = pipeline("automatic-speech-recognition", model=model, device=device)

    for cfg, spl in targets:
        click.echo(f"Transcribing {cfg}/{spl}")
        dataset_dir = Path(f"{cfg}/{spl}")
        metadata_file = dataset_dir / "metadata.jsonl"

        # Load existing metadata
        entries = []
        with open(metadata_file, "r") as f:
            for line in f:
                entries.append(json.loads(line))

        # Process in batches with progress bar
        progress = tqdm(total=len(entries), desc="Transcribing files")
        for i in range(0, len(entries), batch_size):
            batch = entries[i : i + batch_size]
            audio_paths = [str(dataset_dir / entry["file_name"]) for entry in batch]

            # Load audio batch
            audios = []
            for path in audio_paths:
                y, sr = librosa.load(path, sr=16000)
                audios.append({"raw": y, "sampling_rate": sr})

            # Run inference
            results = pipe(audios)

            # Update metadata
            for entry, result in zip(batch, results):
                entry[column] = result["text"]

            progress.update(len(batch))
        progress.close()

        # Save updated metadata
        with open(metadata_file, "w") as f:
            for entry in entries:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
