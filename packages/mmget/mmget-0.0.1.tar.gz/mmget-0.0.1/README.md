# mmget - Multi Model Get

mmget is a Python library that simplifies downloading files from various sources including regular URLs, Hugging Face, and CivitAI. It provides a unified interface for managing model downloads with support for authentication tokens and customizable download paths.

# Features

- Download files from regular URLs
- Download models from Hugging Face using access tokens
- Download models from CivitAI using access tokens
  - Interactive version selection when multiple versions are available (Jupyter only)
  - Customizable download paths for different software (A1111, ComfyUI) based on model types
- Jupyter notebook integration with GUI interface
- Works in console environment

[Screenshot coming soon]

## Installation

You can install mmget using pip:

```
pip install mmget
```

## Usage

```python
from mmget import mmget

mmget(
  hf_token = "" # Hugging Face Access Token [Optional]
  civitai_token = "" # CivitAI Access Token [Optional]
).dl(
  # Download FLUX-1 Dev Model (Access Token Required) to "Download Paths"
  "https://huggingface.co/black-forest-labs/FLUX.1-dev/blob/main/flux1-dev.safetensors",
  "downloads"
).dl(
  # Download CivitaAI Model to ComfyUI that will be saved to downloads/comfyui/models/loras
  "https://civitai.com/models/7525/1-mb-lora-trained-in-5-mins-that-does-the-same-thing-as-25-gb-model-but-better",
  "downloads/comfyui",
  dest_type="comfyui"
).run()
```

### CivitAI

When downloading models from CivitAI, you may encounter multiple available versions. In Jupyter notebooks, mmget will display an interactive interface allowing you to choose from the available versions. When running from the console, it will display the available versions and pause the download process until you specify a version.

Moreover, if you set the dest_type is either of "a1111" or "comfyui" , it will find check the type of the model and determine the subfolder to be used.

```python
from mmget import mmget

mget(
  civitai_token = "" # It is needed if the author require download to have a civitai account
).dl(
  "https://civitai.com/models/257749/pony-diffusion-v6-xl",
  version="V6 (start with this one)",
  dest_type="comfyui"
).run()
```

### Hugging Face

Finding the URL of a file inside hugging face is easy. Open the "Files and versions" tab, and choose the file, right click and copy link address.

TBD: Screenshot

```python
mmget(
  hf_token = "" # Hugging Face Access Token [Optional]
).dl(
  # Download FLUX-1 Dev Model (Access Token Required) to "Download Paths"
  "https://huggingface.co/black-forest-labs/FLUX.1-dev/blob/main/flux1-dev.safetensors",
  "downloads"
).run()
```

### Environment Variables

mmget reads several environment variables:

- MMGET_CIVITAI_TOKEN - CivitAI access token for downloading models that require authentication
- MMGET_HF_TOKEN - Hugging Face access token for downloading models that require authentication
- MMGET_DEST_PATH - The default distribution path for all downloads if not specified
- MMGET_DEST_TYPE - The default distribution type (e.g. "a1111" or "comfyui") for all downloads if not specified

```python
from dotenv import load_dotenv
from mmget import mmget
load_dotenv() # Load environment variable from .env

mmget(
).dl( 
  # URL
).run()
```