import click
import numpy as np
import shutil
import librosa
import soundfile
import click
import json
from pathlib import Path
from ...utils import get_configs_splits


# Adapted from https://github.com/openvpi/audio-slicer/blob/main/slicer2.py
def get_rms(
    y,
    *,
    frame_length=2048,
    hop_length=512,
    pad_mode="constant",
):
    padding = (int(frame_length // 2), int(frame_length // 2))
    y = np.pad(y, padding, mode=pad_mode)

    axis = -1
    # put our new within-frame axis at the end for now
    out_strides = y.strides + tuple([y.strides[axis]])
    # Reduce the shape on the framing axis
    x_shape_trimmed = list(y.shape)
    x_shape_trimmed[axis] -= frame_length - 1
    out_shape = tuple(x_shape_trimmed) + tuple([frame_length])
    xw = np.lib.stride_tricks.as_strided(y, shape=out_shape, strides=out_strides)
    if axis < 0:
        target_axis = axis - 1
    else:
        target_axis = axis + 1
    xw = np.moveaxis(xw, -1, target_axis)
    # Downsample along the target axis
    slices = [slice(None)] * xw.ndim
    slices[axis] = slice(0, None, hop_length)
    x = xw[tuple(slices)]

    # Calculate power
    power = np.mean(np.abs(x) ** 2, axis=-2, keepdims=True)

    return np.sqrt(power)


class Slicer:
    def __init__(
        self,
        sr: int,
        threshold: float = -40.0,
        min_length: int = 5000,
        min_interval: int = 300,
        hop_size: int = 20,
        max_sil_kept: int = 5000,
    ):
        if not min_length >= min_interval >= hop_size:
            raise ValueError(
                "The following condition must be satisfied: min_length >= min_interval >= hop_size"
            )
        if not max_sil_kept >= hop_size:
            raise ValueError(
                "The following condition must be satisfied: max_sil_kept >= hop_size"
            )
        min_interval = sr * min_interval / 1000
        self.threshold = 10 ** (threshold / 20.0)
        self.hop_size = round(sr * hop_size / 1000)
        self.win_size = min(round(min_interval), 4 * self.hop_size)
        self.min_length = round(sr * min_length / 1000 / self.hop_size)
        self.min_interval = round(min_interval / self.hop_size)
        self.max_sil_kept = round(sr * max_sil_kept / 1000 / self.hop_size)

    def _apply_slice(self, waveform, begin, end):
        if len(waveform.shape) > 1:
            return waveform[
                :, begin * self.hop_size : min(waveform.shape[1], end * self.hop_size)
            ]
        else:
            return waveform[
                begin * self.hop_size : min(waveform.shape[0], end * self.hop_size)
            ]

    # @timeit
    def slice(self, waveform):
        if len(waveform.shape) > 1:
            samples = waveform.mean(axis=0)
        else:
            samples = waveform
        if (samples.shape[0] + self.hop_size - 1) // self.hop_size <= self.min_length:
            return [waveform]
        rms_list = get_rms(
            y=samples, frame_length=self.win_size, hop_length=self.hop_size
        ).squeeze(0)
        sil_tags = []
        silence_start = None
        clip_start = 0
        for i, rms in enumerate(rms_list):
            # Keep looping while frame is silent.
            if rms < self.threshold:
                # Record start of silent frames.
                if silence_start is None:
                    silence_start = i
                continue
            # Keep looping while frame is not silent and silence start has not been recorded.
            if silence_start is None:
                continue
            # Clear recorded silence start if interval is not enough or clip is too short
            is_leading_silence = silence_start == 0 and i > self.max_sil_kept
            need_slice_middle = (
                i - silence_start >= self.min_interval
                and i - clip_start >= self.min_length
            )
            if not is_leading_silence and not need_slice_middle:
                silence_start = None
                continue
            # Need slicing. Record the range of silent frames to be removed.
            if i - silence_start <= self.max_sil_kept:
                pos = rms_list[silence_start : i + 1].argmin() + silence_start
                if silence_start == 0:
                    sil_tags.append((0, pos))
                else:
                    sil_tags.append((pos, pos))
                clip_start = pos
            elif i - silence_start <= self.max_sil_kept * 2:
                pos = rms_list[
                    i - self.max_sil_kept : silence_start + self.max_sil_kept + 1
                ].argmin()
                pos += i - self.max_sil_kept
                pos_l = (
                    rms_list[
                        silence_start : silence_start + self.max_sil_kept + 1
                    ].argmin()
                    + silence_start
                )
                pos_r = (
                    rms_list[i - self.max_sil_kept : i + 1].argmin()
                    + i
                    - self.max_sil_kept
                )
                if silence_start == 0:
                    sil_tags.append((0, pos_r))
                    clip_start = pos_r
                else:
                    sil_tags.append((min(pos_l, pos), max(pos_r, pos)))
                    clip_start = max(pos_r, pos)
            else:
                pos_l = (
                    rms_list[
                        silence_start : silence_start + self.max_sil_kept + 1
                    ].argmin()
                    + silence_start
                )
                pos_r = (
                    rms_list[i - self.max_sil_kept : i + 1].argmin()
                    + i
                    - self.max_sil_kept
                )
                if silence_start == 0:
                    sil_tags.append((0, pos_r))
                else:
                    sil_tags.append((pos_l, pos_r))
                clip_start = pos_r
            silence_start = None
        # Deal with trailing silence.
        total_frames = rms_list.shape[0]
        if (
            silence_start is not None
            and total_frames - silence_start >= self.min_interval
        ):
            silence_end = min(total_frames, silence_start + self.max_sil_kept)
            pos = rms_list[silence_start : silence_end + 1].argmin() + silence_start
            sil_tags.append((pos, total_frames + 1))
        # Apply and return slices.
        if len(sil_tags) == 0:
            return [waveform]
        else:
            chunks = []
            if sil_tags[0][0] > 0:
                chunks.append(self._apply_slice(waveform, 0, sil_tags[0][0]))
            for i in range(len(sil_tags) - 1):
                chunks.append(
                    self._apply_slice(waveform, sil_tags[i][1], sil_tags[i + 1][0])
                )
            if sil_tags[-1][1] < total_frames:
                chunks.append(
                    self._apply_slice(waveform, sil_tags[-1][1], total_frames)
                )
            return chunks


def slicer(
    config: str,
    split: str,
    min_length: int,
    hop_size: int,
    db_thresh: float,
    min_interval: int,
    max_sil_kept: int,
):
    """Slice audio files in the dataset"""
    # Get dataset directory
    dataset_dir = Path(f"{config}/{split}")
    if not dataset_dir.exists():
        click.echo(f"Error: Dataset directory {dataset_dir} does not exist")
        return

    # Load metadata
    metadata_file = dataset_dir / "metadata.jsonl"
    if not metadata_file.exists():
        click.echo(f"Error: Metadata file {metadata_file} does not exist")
        return

    # Read existing metadata
    existing_files = []
    with open(metadata_file, "r") as f:
        for line in f:
            existing_files.append(json.loads(line))

    # Create temporary directory for new files
    temp_dir = dataset_dir / "temp_sliced"
    temp_dir.mkdir(exist_ok=True)

    # Process each file
    new_metadata = []
    try:
        for entry in existing_files:
            file_path = dataset_dir / entry["file_name"]
            if not file_path.exists():
                click.echo(f"Warning: File {file_path} not found, skipping")
                continue

            click.echo(f"Processing {file_path}")

            # Load audio
            audio, sr = librosa.load(str(file_path), sr=None, mono=False)

            # Create slicer
            slicer = Slicer(
                sr=sr,
                threshold=db_thresh,
                min_length=min_length,
                min_interval=min_interval,
                hop_size=hop_size,
                max_sil_kept=max_sil_kept,
            )

            # Slice audio
            chunks = slicer.slice(audio)

            # Save chunks
            base_name = file_path.stem
            for i, chunk in enumerate(chunks):
                if len(chunk.shape) > 1:
                    chunk = chunk.T
                new_file_name = f"{base_name}_{i}.wav"
                new_file_path = temp_dir / new_file_name

                soundfile.write(str(new_file_path), chunk, sr)
                new_metadata.append({"file_name": new_file_name})

        # Remove old files
        for entry in existing_files:
            (dataset_dir / entry["file_name"]).unlink(missing_ok=True)

        # Move new files to dataset directory
        for file in temp_dir.glob("*"):
            shutil.move(str(file), dataset_dir / file.name)

        # Update metadata file
        with open(metadata_file, "w") as f:
            for entry in new_metadata:
                f.write(json.dumps(entry) + "\n")

        click.echo(
            f"Successfully sliced {len(existing_files)} files into {len(new_metadata)} chunks"
        )

    finally:
        # Cleanup
        if temp_dir.exists():
            shutil.rmtree(temp_dir)


@click.command()
@click.option(
    "--min-length", type=int, default=5000, help="Minimum length in milliseconds"
)
@click.option("--hop-size", type=int, default=10, help="Hop size for slicing")
@click.option(
    "--db-thresh",
    type=float,
    default=-40,
    help="The dB threshold for silence detection",
)
@click.option(
    "--min-interval",
    type=int,
    default=300,
    help="Minimum silence interval in milliseconds",
)
@click.option(
    "--max-sil-kept",
    type=int,
    default=500,
    help="Maximum silence length kept in milliseconds",
)
@click.pass_context
def slice(
    ctx,
    min_length: int,
    hop_size: int,
    db_thresh: float,
    min_interval: int,
    max_sil_kept: int,
):
    """Slice audio files in the dataset"""
    config = ctx.parent.params["config"]
    split = ctx.parent.params["split"]

    targets = get_configs_splits(config, split)
    if not targets:
        click.echo("No valid config/split combinations found")
        return

    for cfg, spl in targets:
        click.echo(f"Slicing {cfg}/{spl}")
        slicer(cfg, spl, min_length, hop_size, db_thresh, min_interval, max_sil_kept)
