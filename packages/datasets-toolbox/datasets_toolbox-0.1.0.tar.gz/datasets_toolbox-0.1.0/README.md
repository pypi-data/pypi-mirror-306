# Datasets Toolbox

A toolbox for creating, processing and inspecting audio/image datasets through a simple CLI interface.

## Installation

```sh
pip install datasets-toolbox
```

## Usage

The goal of datasets-toolbox is to build audio/image datasets with CLI.

All the commands support `--config [config-name]` and `--split [split-name]` options to specified the target. Where `config-name` is the configuration name (e.g. language) and `split-name` is something like `train`, `validation`, `test`.

### Add More Data

`datasets import --config [data] --split [train] <sources>`

Import data into datasets structure.

If the configuration/split is not configured, will defaults to `default` configuration and `train` split.

### Modify Dataset

`datasets modify <action> --config [data] --split [train] --other-params`

If the configuration/split is not configured, will defaults to recursively run on all configurations and all splits.

#### Audio Slicer

`datasets modify slice --config [data] --split [train] --min-length [ms] --hop-size [n]`

#### Audio Resample

`datasets modify resample --config [data] --split [train] --sr [16000] --mono`

#### Audio Transcription

`datasets modify transcribe --model [openai/whisper-large-v3-turbo]'`

### Inspect Dataset

`datasets inspect --config [data] --split [train] --other-params`

If the configuration/split is not configured, will defaults to recursively run on all configurations and all splits.

#### Audio Hours

`datasets inspect hours --config [data] --split [train]`
