from pathlib import Path
from typing import List, Dict
import click
import json
import librosa
from tqdm import tqdm


def get_configs_splits(config: str, split: str) -> List[tuple[str, str]]:
    """Get all available config/split combinations"""
    configs = set()
    splits = set()

    # Search for all directories that contain metadata.jsonl
    for path in Path(".").glob("**/metadata.jsonl"):
        # The parent directory is the split, its parent is the config
        split_dir = path.parent
        config_dir = split_dir.parent
        configs.add(config_dir.name)
        splits.add(split_dir.name)

    all = [(config, split) for config in configs for split in splits]

    if config:
        all = [x for x in all if x[0] == config]
    if split:
        all = [x for x in all if x[1] == split]

    return all


def load_metadata(metadata_file: Path) -> List[Dict]:
    """Load metadata from a JSONL file"""
    entries = []
    with open(metadata_file, "r") as f:
        for line in f:
            entries.append(json.loads(line))
    return entries


def calculate_audio_duration(file_path: str) -> float:
    """Calculate duration of audio file in hours"""
    y, sr = librosa.load(file_path, sr=None)
    return librosa.get_duration(y=y, sr=sr) / 3600
